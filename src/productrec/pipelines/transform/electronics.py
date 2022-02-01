from typing import Any, Dict, List

import pandas as pd

#
# Incoming dataframe has the following columns:
#  - order_id
#  - product_id
#  - price
#  - user_id
#  - brand
#  - category_code
def transform_electronics(transactions: pd.DataFrame) -> List[pd.DataFrame]:
    
    transactions['order_id'] = transactions['order_id'].astype(str)
    transactions['product_id'] = transactions['product_id'].astype(str)
    transactions['quantity'] = 1
    transactions['description'] = transactions['brand'] + transactions['category_code']

    products = transactions[['product_id', 'description']].drop_duplicates() # Only get unique item/description pairs
    products['product_id'] = products.product_id.astype(str) # Encode as strings for future lookup ease

    return [transactions, products] 