from typing import Any, Dict, List

import pandas as pd

def transform_instacart(transactions: pd.DataFrame, products: pd.DataFrame) -> List[pd.DataFrame]:
    transactions['order_id'] = transactions.order_id.astype(str)
    transactions['product_id'] = transactions.product_id.astype(str)
    transactions['quantity'] = 1
    transactions['price'] = 1

    filtered_df = transactions[["order_id", "product_id", "price", "quantity"]]

    products['product_id'] = products.product_id.astype(str)
    products["description"] = products["product_name"]
    products = products[["product_id", "description"]]
    return [ filtered_df, products ]
