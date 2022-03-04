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

    score = score_model(model, product_test, test_size=0.1, seed=seed)
    log.info("Score: {}".format(score))
    return score
    
def score_model(model, test_orders, test_size=0.1, seed=42):

    skipped = 0
    
    tplist = []
    tnlist = []
    fplist = []
    fnlist = []

    random.seed(seed) 

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