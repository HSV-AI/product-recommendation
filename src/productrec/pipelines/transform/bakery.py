from typing import Any, Dict, List

import pandas as pd

def transform_bakery(transactions: pd.DataFrame) -> List[pd.DataFrame]:

    transactions['NumberOfItemsPurchased'] = 1
    transactions['Customer'] = transactions['Date']
    transactions['Description'] = 'none'
    transactions["Price"] = 0.0
    transactions['Item'] = transactions['Item'].astype(str)

    renamed_df = transactions.rename(columns={"Transaction": "order_id", 
                        "Item": "product_id",
                        "Customer": "customer_id",
                        "Description":"description",
                        "NumberOfItemsPurchased":"quantity",
                        "Price":"price"})[['order_id', 'product_id', 'customer_id', 'description', 'quantity', 'price']]

    return renamed_df
