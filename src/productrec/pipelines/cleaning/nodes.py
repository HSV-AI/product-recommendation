from typing import Any, Dict, List

import pandas as pd
import numpy as np

def clean_electronics(data: pd.DataFrame) -> List[pd.DataFrame]:

    filter_value = 100
    product_group = data.loc[:, ['order_id', 'product_id']].groupby('product_id').count()
 
    multi_product = product_group[product_group.order_id >= filter_value].count()
    single_product = product_group[product_group.order_id < filter_value].count()
    
    print('Products in at least',filter_value,'orders:',multi_product['order_id'])
    print('Products in less than',filter_value,'orders:',single_product['order_id'])
    
    # We can capture the list of mutiple product orders with this:
    product_filter = product_group[product_group.order_id >= filter_value].index.tolist()
    
    product_filtered_df = data[data['product_id'].isin(product_filter)].copy()
    minimum_order_size =   5#@param {type: "number"}
    maximum_order_size =   20#@param {type: "number"}

    order_group = product_filtered_df.loc[:, ['order_id', 'product_id']].groupby('order_id').count()
    
    multi_order = order_group[(order_group.product_id >= minimum_order_size) & (order_group.product_id <= maximum_order_size)].count()
    single_order = order_group[(order_group.product_id < minimum_order_size) | (order_group.product_id > maximum_order_size)].count()
    
    print('Orders with at least',minimum_order_size,'products:',multi_order['product_id'])
    print('Orders with less than',minimum_order_size,'products:',single_order['product_id'])
    
    # We can capture the list of mutiple product orders with this:
    order_filter = order_group[(order_group.product_id >= minimum_order_size) & (order_group.product_id <= maximum_order_size)].index.tolist()
    filtered_df = product_filtered_df[product_filtered_df['order_id'].isin(order_filter)].copy()
    print('Original dataframe length:', len(data))
    print('Filtered dataframe length:', len(filtered_df))

    product_counts = filtered_df['product_id'].value_counts().to_numpy()
    print('There are', len(product_counts), 'unique products\n')
    print('\nAnd a graph of what the curve looks like:')
    
    order_counts = filtered_df['order_id'].value_counts()
    num_orders = len(order_counts)
    num_items = len(product_counts)
    sparsity = 1 - len(data) / (num_orders * num_items)
    print(f'number of orders: {num_orders}, number of items: {num_items}')
    print(f'matrix sparsity: {sparsity:f}')

    filtered_df['product_id'] = filtered_df['product_id'].astype(str)
    filtered_df['quantity'] = 1
    filtered_df['description'] = filtered_df['brand'] + filtered_df['category_code']

    item_lookup = filtered_df[['product_id', 'description']].drop_duplicates() # Only get unique item/description pairs
    item_lookup['product_id'] = item_lookup.product_id.astype(str) # Encode as strings for future lookup ease

    return [filtered_df, item_lookup] 

def clean_brazillian(transactions: pd.DataFrame, products: pd.DataFrame, customers: pd.DataFrame) -> List[pd.DataFrame]:

    transactions['order_id'] = transactions.order_id.astype(str)
    transactions['product_id'] = transactions.product_id.astype(str)
    products['product_id'] = products.product_id.astype(str)

    customers = customers[["customer_id", "order_id", "order_purchase_timestamp"]].copy()
    customers['order_id'] = customers.order_id.astype(str)
    customers['customer_id'] = customers.customer_id.astype(str)

    transactions = transactions.merge(customers, on='order_id')
    minimum_order_size = 2
    order_group = transactions.loc[:, ['order_id', 'product_id']].groupby('order_id').count()
    
    multi_order = order_group[(order_group.product_id >= minimum_order_size)].count()
    single_order = order_group[(order_group.product_id < minimum_order_size)].count()
    
    print('Orders with at least',minimum_order_size,'products:',multi_order['product_id'])
    print('Orders with less than',minimum_order_size,'products:',single_order['product_id'])
    
    # We can capture the list of mutiple product orders with this:
    order_filter = order_group[(order_group.product_id >= minimum_order_size)].index.tolist()

    filtered_df = transactions[transactions['order_id'].isin(order_filter)].copy()

    print('Original dataframe length:', len(transactions))
    print('Filtered dataframe length:', len(filtered_df))

    filtered_df['quantity'] = 1

    products["description"] = products["product_category_name"] + str(products["product_description_lenght"])

    return [ 
        filtered_df[["order_id", "product_id", "price", "quantity"]],
        products[["product_id", "description"]]
    ]
