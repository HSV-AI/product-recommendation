from typing import Any, Dict, List

import pandas as pd
import numpy as np
import implicit
import scipy
from sklearn import metrics
import logging
from scipy.sparse import coo_matrix, csr_matrix
from tqdm.auto import tqdm

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

    log.info(params)
    log.info("Size of product_train: {}".format(product_train.shape))
    log.info("Size of product_test: {}".format(product_test.shape))
    log.info("Size of user_vecs: {}".format(len(user_vecs)))
    log.info("Size of item_vecs: {}".format(len(item_vecs)))

    model = implicit.als.AlternatingLeastSquares(factors=factors,
                                        regularization=regularization,
                                        iterations=iterations, use_gpu=False)

    start_new = len(user_vecs)

    model.user_factors = user_vecs
    model.item_factors = item_vecs

    total = scipy.sparse.vstack((product_train,product_test))  # NOT np.vstack
    popular_items = np.array(total.sum(axis = 0)).reshape(-1) # Get sum of item iteractions to find most popular

    transactions = product_test.shape[0]
    items = product_test.shape[1]

    log.info(transactions)
    log.info(items)

    # TODO - NEED TO FIND A BETTER WAY TO CALCULATE FOR NEW ORDERS
    for transaction in range(transactions):
        purchases = []
        for i in range(product_test.indptr[1], product_test.indptr[2]):
            purchases.append(product_test.indices[i])
        
        model.partial_fit_users([start_new], product_test.getrow(transaction))
        start_new += 1
                # model.recommend()
    # for i in range(users):
    #     log.info("Index: {} - Size: {}".format(i,product_test.indptr[i+1] - product_test.indptr[i]))


    return {
        "precision": 1
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

    results = ranking_metrics_at_k(model, product_train, product_test, K=10, show_progress=True, num_threads=1)

    log.info(results)

    return { 'test': results['auc'], 'popular': 1 }