from typing import Any, Dict, List

import pandas as pd

def transform_jewelry(transactions: pd.DataFrame) -> List[pd.DataFrame]:

    print('Total length is',len(transactions))
    transactions.isna().sum()

    transactions = transactions[(transactions.quantity > 0) & (transactions.price > 0)]

    item_lookup = transactions[['product_id', 'category_code']].drop_duplicates() # Only get unique item/description pairs
    item_lookup['product_id'] = item_lookup.product_id.astype(str) # Encode as strings for future lookup ease

    renamed_df = transactions[["order_id", "product_id","quantity", "price"]]
    products_df = item_lookup.rename(columns={"StockCode":"product_id", "Description":"description"})

    return [renamed_df, products_df]
