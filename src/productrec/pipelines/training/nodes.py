from typing import Any, Dict, List

import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt
import implicit
import scipy
from sklearn import metrics
from pandas.api.types import CategoricalDtype
import time
import wandb

def train_implicit(product_train: scipy.sparse.csr_matrix, params: Dict) -> Any:

    alpha = params['alpha']    
    factors = params['factors']
    regularization = params['regularization']
    iterations = params['iterations']
    seed = params.get("seed", 42)

    model = implicit.als.AlternatingLeastSquares(factors=factors,
                                        regularization=regularization,
                                        iterations=iterations, 
                                        random_state=seed )


    start = time.perf_counter()
    model.fit((product_train * alpha).astype('double'), show_progress=False)
    duration = time.perf_counter() - start

    wandb.log({"train_time": duration})
    
    if implicit.gpu.HAS_CUDA:
        model = model.to_cpu()
    
    user_vecs = model.user_factors
    item_vecs = model.item_factors

    return [user_vecs, item_vecs, product_train*alpha]