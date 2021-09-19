from typing import Any, Dict, List

import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt
import implicit
import scipy
from sklearn import metrics
from pandas.api.types import CategoricalDtype

def train_implicit(product_train: scipy.sparse.csr_matrix, hyperparams: Dict) -> Any:

    alpha = hyperparams['alpha']    
    factors = hyperparams['factors']
    regularization = hyperparams['regularization']
    iterations = hyperparams['iterations']

    model = implicit.als.AlternatingLeastSquares(factors=factors,
                                        regularization=regularization,
                                        iterations=iterations)

    model.fit((product_train * alpha).astype('double'))

    user_vecs = model.user_factors
    item_vecs = model.item_factors

    return [user_vecs, item_vecs, product_train*alpha]