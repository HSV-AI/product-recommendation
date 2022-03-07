from typing import Any, Dict, List

import pandas as pd

def transform_journey(transactions: pd.DataFrame, products: pd.DataFrame) -> List[pd.DataFrame]:

    products['DESC'] = products['COMMODITY_DESC'] + products['SUB_COMMODITY_DESC']
    
    transactions['BASKET_ID'] = transactions['BASKET_ID'].astype(str)
    transactions['PRODUCT_ID'] = transactions['PRODUCT_ID'].astype(str)
    transactions['household_key'] = transactions['household_key'].astype(str)

    filtered_df = transactions.rename(columns={"PRODUCT_ID": "product_id", "QUANTITY": "quantity", "BASKET_ID": "order_id", "SALES_VALUE": "price", "household_key": "customer_id"})
    final_df = filtered_df[["order_id", "product_id", "customer_id", "quantity", "price"]]
    products = products.rename(columns={"PRODUCT_ID":"product_id", "DESC":"description"})[["product_id", "description"]]

    return [final_df, products]
