from typing import Any, Dict, List

import pandas as pd
import numpy as np
import implicit
import scipy
from sklearn import metrics
import logging

def auc_score(predictions, test):
    '''
    This simple function will output the area under the curve using sklearn's metrics. 
    
    parameters:
    
    - predictions: your prediction output
    
    - test: the actual target result you are comparing to
    
    returns:
    
    - AUC (area under the Receiver Operating Characterisic curve)
    '''
    fpr, tpr, thresholds = metrics.roc_curve(test, predictions)
    return metrics.auc(fpr, tpr)   

def calc_mean_auc(training_set, altered_users, predictions, test_set):
    '''
    This function will calculate the mean AUC by user for any user that had their user-item matrix altered. 
    
    parameters:
    
    training_set - The training set resulting from make_train, where a certain percentage of the original
    user/item interactions are reset to zero to hide them from the model 
    
    predictions - The matrix of your predicted ratings for each user/item pair as output from the implicit MF.
    These should be stored in a list, with user vectors as item zero and item vectors as item one. 
    
    altered_users - The indices of the users where at least one user/item pair was altered from make_train function
    
    test_set - The test set constucted earlier from make_train function
    
    
    
    returns:
    
    The mean AUC (area under the Receiver Operator Characteristic curve) of the test set only on user-item interactions
    there were originally zero to test ranking ability in addition to the most popular items as a benchmark.
    '''
    log = logging.getLogger(__name__)

    
    store_auc = [] # An empty list to store the AUC for each user that had an item removed from the training set
    popularity_auc = [] # To store popular AUC scores
    pop_items = np.array(test_set.sum(axis = 0)).reshape(-1) # Get sum of item iteractions to find most popular
    item_vecs = predictions[1]
    for user in altered_users: # Iterate through each user that had an item altered
        training_row = training_set[user,:].toarray().reshape(-1) # Get the training set row
        zero_inds = np.where(training_row == 0) # Find where the interaction had not yet occurred
        # Get the predicted values based on our user/item vectors
        log.info(len(zero_inds))
        user_vec = predictions[0][user,:]
        pred = user_vec.dot(item_vecs).toarray()[0,zero_inds].reshape(-1)
        # Get only the items that were originally zero
        # Select all ratings from the MF prediction for this user that originally had no iteraction
        actual = test_set[user,:].toarray()[0,zero_inds].reshape(-1) 
        # Select the binarized yes/no interaction pairs from the original full data
        # that align with the same pairs in training 
        pop = pop_items[zero_inds] # Get the item popularity for our chosen items
        store_auc.append(auc_score(pred, actual)) # Calculate AUC for the given user and store
        popularity_auc.append(auc_score(pop, actual)) # Calculate AUC using most popular and score
    # End users iteration
    
    return np.mean(store_auc), np.mean(popularity_auc)  
   # Return the mean AUC rounded to three decimal places for both test and popularity benchmark

def score_auc(
                product_train: scipy.sparse.csr_matrix, 
                product_test: scipy.sparse.csr_matrix, 
                products_altered: List,
                user_vecs: List, 
                item_vecs: List, 
                params: Dict) -> Dict:

    log = logging.getLogger(__name__)

    factors = params['factors']
    regularization = params['regularization']
    iterations = params['iterations']

    log.info(params)
    log.info("Size of product_train: {}".format(product_train.shape))
    log.info("Size of product_test: {}".format(product_test.shape))
    log.info("Size of user_vecs: {}".format(len(user_vecs)))
    log.info("Size of item_vecs: {}".format(len(item_vecs)))

    model = implicit.als.AlternatingLeastSquares(factors=factors,
                                        regularization=regularization,
                                        iterations=iterations)

    model.user_factors = user_vecs
    model.item_factors = item_vecs

    test, popular = calc_mean_auc(product_train, products_altered, 
              [scipy.sparse.csr_matrix(item_vecs), scipy.sparse.csr_matrix(user_vecs.T)], product_test)


    print('Our model scored',test,'versus a score of',popular,'if we always recommended the most popular item.')

    return { 'test': test, 'popular': popular }