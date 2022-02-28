from typing import Any, Dict, List

import pandas as pd
import numpy as np
import implicit
import random
import scipy
from sklearn import metrics
import logging
from scipy.sparse import coo_matrix, csr_matrix
from tqdm.auto import tqdm

def mask_matrix(ratings, pct_test = 0.2, seed = 42):
    '''
    This function will take in the original user-item matrix and "mask" a percentage of the original ratings where a
    user-item interaction has taken place for use as a test set. The test set will contain all of the original ratings, 
    while the training set replaces the specified percentage of them with a zero in the original ratings matrix. 
    
    parameters: 
    
    ratings - the original ratings matrix from which you want to generate a train/test set. Test is just a complete
    copy of the original set. This is in the form of a sparse csr_matrix. 
    
    pct_test - The percentage of user-item interactions where an interaction took place that you want to mask in the 
    training set for later comparison to the test set, which contains all of the original ratings. 
    
    returns:
    
    training_set - The altered version of the original data with a certain percentage of the user-item pairs 
    that originally had interaction set back to zero.
    
    test_set - A copy of the original ratings matrix, unaltered, so it can be used to see how the rank order 
    compares with the actual interactions.
    
    user_inds - From the randomly selected user-item indices, which user rows were altered in the training data.
    This will be necessary later when evaluating the performance via AUC.
    '''
    test_set = ratings.copy() # Make a copy of the original set to be the test set. 
    # test_set[test_set != 0] = 1 # Store the test set as a binary preference matrix
    training_set = ratings.copy() # Make a copy of the original data we can alter as our training set. 
    nonzero_inds = training_set.nonzero() # Find the indices in the ratings data where an interaction exists
    nonzero_pairs = list(zip(nonzero_inds[0], nonzero_inds[1])) # Zip these pairs together of user,item index into list
    
    random.seed(seed) # Set the random seed to zero for reproducibility
    num_samples = int(np.ceil(pct_test*len(nonzero_pairs))) # Round the number of samples needed to the nearest integer
    samples = random.sample(nonzero_pairs, num_samples) # Sample a random number of user-item pairs without replacement
    user_inds = [index[0] for index in samples] # Get the user row indices
    item_inds = [index[1] for index in samples] # Get the item column indices
    training_set[user_inds, item_inds] = 0 # Assign all of the randomly chosen user-item pairs to zero
    training_set.eliminate_zeros() # Get rid of zeros in sparse array storage after update to save space
    return training_set, test_set, list(set(user_inds)), list(set(item_inds)) # Output the unique list of user rows that were altered  

def ranking_metrics_at_k(model, train_user_items, test_user_items, K=10, show_progress=True, num_threads=1):
    """ Calculates ranking metrics for a given trained model

    Parameters
    ----------
    model : RecommenderBase
        The fitted recommendation model to test
    train_user_items : csr_matrix
        Sparse matrix of user by item that contains elements that were used
            in training the model
    test_user_items : csr_matrix
        Sparse matrix of user by item that contains withheld elements to
        test on
    K : int
        Number of items to test on
    show_progress : bool, optional
        Whether to show a progress bar
    num_threads : int, optional
        The number of threads to use for testing. Specifying 0 means to default
        to the number of cores on the machine. Note: aside from the ALS and BPR
        models, setting this to more than 1 will likely hurt performance rather than
        help.

    Returns
    -------
    float
        the calculated p@k
    """

    if not isinstance(train_user_items, csr_matrix):
        train_user_items = train_user_items.tocsr()

    if not isinstance(test_user_items, csr_matrix):
        test_user_items = test_user_items.tocsr()

    total = scipy.sparse.vstack((train_user_items,test_user_items))  # NOT np.vstack
    popular_items = np.array(total.sum(axis = 0)).reshape(-1) # Get sum of item iteractions to find most popular

    users = test_user_items.shape[0]
    items = test_user_items.shape[1]

    # precision
    relevant = 0.0
    pr_div = 0.0
    total = 0.0

    # map
    mean_ap = 0.0
    ap = 0.0
    # ndcg
    cg = (1.0 / np.log2(np.arange(2, K + 2)))
    cg_sum = np.cumsum(cg)
    ndcg = 0, 
    # idcg
    # auc
    mean_auc = 0 #, auc, hit, miss, num_pos_items, num_neg_items
    mean_pop_auc = 0
    test_indptr = test_user_items.indptr
    test_indices = test_user_items.indices


    batch_size = 1000
    start_idx = 0

    # get an array of userids that have at least one item in the test set
    to_generate = np.arange(users, dtype="int32")
    to_generate = to_generate[np.ediff1d(test_user_items.indptr) > 0]

    progress = tqdm(total=len(to_generate), disable=not show_progress)

    while start_idx < len(to_generate):
        batch = to_generate[start_idx: start_idx + batch_size]
        ids, _ = model.recommend(batch, train_user_items[batch], N=K)
        start_idx += batch_size

        for batch_idx in range(len(batch)):
            u = batch[batch_idx]
            likes = []
            for i in range(test_indptr[u], test_indptr[u+1]):
                likes.append(test_indices[i])

            pr_div += min(K, len(likes))
            ap = 0
            pop_ap = 0
            hit = 0
            pop_hit = 0
            miss = 0
            pop_miss = 0
            auc = 0
            pop_auc = 0
            idcg = cg_sum[min(K, len(likes)) - 1]
            num_pos_items = len(likes)
            num_neg_items = items - num_pos_items

            likes = np.array(likes, dtype="int32")
            for i in range(K):
                if ids[batch_idx, i] in likes:
                    relevant += 1
                    hit += 1
                    ap += hit / (i + 1)
                    ndcg += cg[i] / idcg
                else:
                    miss += 1
                    auc += hit

                if popular_items[i] in likes:
                    pop_hit += 1
                    pop_ap += pop_hit / (i + 1)
                else:
                    pop_miss += 1
                    pop_auc += pop_hit

            auc += ((hit + num_pos_items) / 2.0) * (num_neg_items - miss)
            pop_auc += ((pop_hit + num_pos_items) / 2.0) * (num_neg_items - pop_miss)
            mean_ap += ap / min(K, len(likes))
            mean_auc += auc / (num_pos_items * num_neg_items)
            mean_pop_auc += pop_auc / (num_pos_items * num_neg_items)
            total += 1

        progress.update(len(batch))

    progress.close()
    return {
        "precision": relevant / pr_div,
        "map": mean_ap / total,
        # TODO - fiture out why this is not working with brazilian dataset
        # "ndcg": ndcg / total,
        "auc": mean_auc / total,
        "pop_auc": mean_pop_auc / total
    }


def score_confusion(
                product_train: scipy.sparse.csr_matrix, 
                product_test: scipy.sparse.csr_matrix, 
                user_vecs: List, 
                item_vecs: List, 
                params: Dict) -> Dict:

    log = logging.getLogger(__name__)

    factors = params['factors']
    regularization = params['regularization']
    iterations = params['iterations']
    seed = params['seed']

    log.info(params)
    log.info("Size of product_train: {}".format(product_train.shape))
    log.info("Size of product_test: {}".format(product_test.shape))
    log.info("Size of user_vecs: {}".format(len(user_vecs)))
    log.info("Size of item_vecs: {}".format(len(item_vecs)))

    model = implicit.als.AlternatingLeastSquares(factors=factors,
                                        regularization=regularization,
                                        iterations=iterations, use_gpu=False)


    model.user_factors = user_vecs
    model.item_factors = item_vecs

    score = score_model(model, product_test, test_size=0.1)
    log.info("Score: {}".format(score))
    return score
    
def score_model(model, test_orders, test_size=0.1):

    skipped = 0
    
    tplist = []
    tnlist = []
    fplist = []
    fnlist = []

    for row in test_orders:

        TP = FP = FN = TN = 0

        # Get the list of nonzero products
        nonzero = row.nonzero()[1]
        order_size = len(nonzero)
        
        # Need to skip if there aren't multiple products
        if order_size < 2:
            skipped+=1
            continue

        temp = row.copy()
        if test_size > 0:
            mask_count = max(1, int(order_size * test_size))
            mask_list = random.sample(list(nonzero), mask_count)
            temp[np.zeros(mask_count), mask_list] = 0
            temp.eliminate_zeros()

        new_id = model.user_factors.shape[0]
        model.partial_fit_users([new_id], temp.astype('double'))
        recs, prob = model.recommend(new_id, temp, N=order_size, filter_already_liked_items=False)
        for rec in recs:
            if rec in nonzero:
                TP+=1
            else:
                FP+=1

        for product in nonzero:
            if product not in recs:
                FN+=1

        TN = model.item_factors.shape[0] - TP - FP - FN
        
        tplist.append(TP)
        tnlist.append(TN)
        fplist.append(FP)
        fnlist.append(FN)
        
    count = test_orders.shape[0] - skipped
    
    true_positive = np.mean(tplist)
    false_positive = np.mean(fplist)
    false_negative = np.mean(fnlist)
    true_negative =  np.mean(tnlist)
    
    sensitivity = true_positive / (true_positive + false_negative)
    specificity = true_negative / (true_negative + false_positive)

    return {
        'true_positive':true_positive,
        'false_positive':false_positive,
        'false_negative':false_negative,
        'true_negative':true_negative,
        'sensitivity':sensitivity,
        'specificity':specificity
    }

def score_auc(
                product_train: scipy.sparse.csr_matrix, 
                product_test: scipy.sparse.csr_matrix, 
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
                                        iterations=iterations, use_gpu=False)

    model.user_factors = user_vecs
    model.item_factors = item_vecs

    results = score_model(model, product_test, test_size=0.1)

    log.info(results)

    return { 'test': results['auc'], 'popular': 1 }