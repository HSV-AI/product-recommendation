from typing import Any, Dict, List

import pandas as pd

def transform_journey(transactions: pd.DataFrame, products: pd.DataFrame) -> List[pd.DataFrame]:

    products['DESC'] = products['COMMODITY_DESC'] + products['SUB_COMMODITY_DESC']
    
    filtered_df = transactions.rename(columns={"PRODUCT_ID": "product_id", "QUANTITY": "quantity", "BASKET_ID": "order_id", "SALES_VALUE": "price"})
    final_df = filtered_df[["order_id", "product_id", "quantity", "price"]]
    products = products.rename(columns={"PRODUCT_ID":"product_id", "DESC":"description"})[["product_id", "description"]]

    return [final_df, products]
