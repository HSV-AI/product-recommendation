from typing import Any, Dict, List

import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt
import implicit
import scipy
from sklearn import metrics
from sklearn.model_selection import train_test_split
from pandas.api.types import CategoricalDtype
import logging

def split_data(transactions: pd.DataFrame, params: Dict) -> Any:

    logging.getLogger(__name__)

    seed = params.get("seed", 42)
    test_size = params.get("test_size", 0.2)

    logging.info("Splitting data based on a seed of {} and test_size of {}".format(seed, test_size))

    transaction_list = list(np.sort(transactions.order_id.unique())) # Get our unique customers
    item_list = list(transactions.product_id.unique()) # Get our unique products that were purchased
    quantity_list = list(transactions.quantity) # All of our purchases

    cols = transactions.order_id.astype(CategoricalDtype(categories=transaction_list, ordered=True)).cat.codes 
    # Get the associated row indices
    rows = transactions.product_id.astype(CategoricalDtype(categories=item_list, ordered=True)).cat.codes 
    # Get the associated column indices
    purchases_sparse = scipy.sparse.csr_matrix((quantity_list, (rows, cols)), shape=(len(item_list), len(transaction_list)))

    train, test = train_test_split(purchases_sparse, test_size=0.2, random_state=seed) # Split the data into training and test sets

    return [train, test]