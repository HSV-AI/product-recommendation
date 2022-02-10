from typing import Any, Dict, List

import pandas as pd

def transform_retailrocket(events: pd.DataFrame) -> List[pd.DataFrame]:
    transactions = events[events.event == "transaction"].copy()
    transactions['order_id'] = transactions.transactionid.astype(str)
    transactions['customer_id'] = transactions.visitorid.astype(str)
    transactions['product_id'] = transactions.itemid.astype(str)
    transactions['quantity'] = 1
    transactions['price'] = 1
    return transactions[["order_id", "product_id","quantity", "price"]]
