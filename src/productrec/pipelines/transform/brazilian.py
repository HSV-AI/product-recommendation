from typing import Any, Dict, List

import pandas as pd

def transform_brazilian(transactions: pd.DataFrame, products: pd.DataFrame, customers: pd.DataFrame) -> List[pd.DataFrame]:

    transactions['order_id'] = transactions.order_id.astype(str)
    transactions['product_id'] = transactions.product_id.astype(str)

    products['product_id'] = products.product_id.astype(str)

    customers = customers[["customer_id", "order_id", "order_purchase_timestamp"]].copy()
    customers['order_id'] = customers.order_id.astype(str)
    customers['customer_id'] = customers.customer_id.astype(str)

    transactions = transactions.merge(customers, on='order_id')
    transactions['quantity'] = 1

    products["description"] = products["product_category_name"] + str(products["product_description_lenght"])

    products = products[["product_id", "description"]].drop_duplicates()
    transactions = transactions[["order_id", "product_id", "price", "quantity"]]
    return [ transactions, products ]
