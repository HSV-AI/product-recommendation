from typing import Any, Dict, List

import pandas as pd

def transform_vipin20(transactions: pd.DataFrame, params: Dict) -> List[pd.DataFrame]:

    # Remove transactions without a negative number, cost, or -1 identifier
    transactions = transactions[(transactions.NumberOfItemsPurchased > 0) & (transactions.CostPerItem > 0) & (transactions.ItemCode != -1)]
    
    renamed_df = transactions.rename(columns={"TransactionId": "order_id", 
                            "ItemCode": "product_id",
                            "UserId": "customer_id",
                            "ItemDescription":"description",
                            "NumberOfItemsPurchased":"quantity",
                            "CostPerItem":"price"})[['order_id', 'product_id', 'customer_id', 'description', 'quantity', 'price']]

    item_lookup = transactions[['ItemCode', 'ItemDescription']].drop_duplicates() # Only get unique item/description pairs
    item_lookup['ItemCode'] = item_lookup.ItemCode.astype(str) # Encode as strings for future lookup ease

    products_df = item_lookup.rename(columns={"ItemCode":"product_id", "ItemDescription":"description"})

    return [renamed_df, products_df]
