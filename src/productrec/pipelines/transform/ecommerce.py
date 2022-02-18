from typing import Any, Dict, List

import pandas as pd

def transform_ecommerce(transactions: pd.DataFrame) -> List[pd.DataFrame]:

    transactions = transactions[(transactions.UnitPrice > 0) & (transactions.Quantity > 0)]

    transactions['StockCode'] = transactions['StockCode'].astype(str)

    item_lookup = transactions[['StockCode', 'Description']].drop_duplicates() # Only get unique item/description pairs
    item_lookup['StockCode'] = item_lookup.StockCode.astype(str) # Encode as strings for future lookup ease

    price_lookup = transactions[['StockCode', 'UnitPrice']].drop_duplicates()
    price_lookup['StockCode'] = price_lookup.StockCode.astype(str)

    transactions = transactions[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice', 'Description']]

    renamed_df = transactions.rename(columns={"InvoiceNo": "order_id", 
                                "StockCode": "product_id", 
                                "Description":"description",
                                "Quantity":"quantity",
                                "UnitPrice":"price"})

    products_df = item_lookup.rename(columns={"StockCode":"product_id", "Description":"description"})

    return [renamed_df, products_df]
