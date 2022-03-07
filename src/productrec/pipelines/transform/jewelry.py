from typing import Any, Dict, List

import pandas as pd

def transform_jewelry(transactions: pd.DataFrame) -> List[pd.DataFrame]:

    print('Total length is',len(transactions))
    transactions.isna().sum()

    transactions = transactions[(transactions.quantity > 0) & (transactions.price > 0)]

    transactions['order_id'] = transactions['order_id'].astype(str)
    transactions['product_id'] = transactions['product_id'].astype(str)
    transactions['user_id'] = transactions['user_id'].astype(str)

    item_lookup = transactions[['product_id', 'category_code']].drop_duplicates() # Only get unique item/description pairs
    item_lookup['product_id'] = item_lookup.product_id.astype(str) # Encode as strings for future lookup ease

    renamed_df = transactions.rename(columns={"user_id": "customer_id"})
    renamed_df = renamed_df[["order_id", "product_id", "customer_id", "quantity", "price"]]
    products_df = item_lookup.rename(columns={"StockCode":"product_id", "Description":"description"})

    return [renamed_df, products_df]
