from typing import Any, Dict, List

import pandas as pd
import numpy as np
import logging

def clean_data(transactions: pd.DataFrame, params: Dict) -> pd.DataFrame:

    log = logging.getLogger(__name__)

    filter_value = params.get("filter_value", 2)
    minimum_order_size = params.get("minimum_order_size", 5)
    maximum_order_size = params.get("maximum_order_size", 20)

    # Need to filter out products that didn't show up in more than some number of orders
    product_group = transactions.loc[:, ['order_id', 'product_id']].groupby('product_id').count()
 
    multi_product = product_group[product_group.order_id >= filter_value].count()
    single_product = product_group[product_group.order_id < filter_value].count()
    
    log.info("Products in at least {} orders: {}".format(filter_value, multi_product['order_id']))
    log.info("Products in less than {} orders: {}".format(filter_value, single_product['order_id']))

    product_filter = product_group[product_group.order_id >= filter_value].index.tolist()
    product_filtered_df = transactions[transactions['product_id'].isin(product_filter)].copy()

    # Need to filter out orders that didn't have at least a minimum number of products
    order_group = product_filtered_df.loc[:, ['order_id', 'product_id']].groupby('order_id').count()
    
    multi_order = order_group[(order_group.product_id >= minimum_order_size) & (order_group.product_id <= maximum_order_size)].count()
    single_order = order_group[(order_group.product_id < minimum_order_size) | (order_group.product_id > maximum_order_size)].count()
    
    log.info("Orders with at least {} products: {}".format(minimum_order_size, multi_order['product_id']))
    log.info("Orders with less than {} products: {}".format(minimum_order_size, single_order['product_id']))
    
    order_filter = order_group[(order_group.product_id >= minimum_order_size) & (order_group.product_id <= maximum_order_size)].index.tolist()
    filtered_df = product_filtered_df[product_filtered_df['order_id'].isin(order_filter)].copy()

    log.info("Original dataframe length: {}".format(len(transactions)))
    log.info("Filtered dataframe length: {}".format(len(filtered_df)))

    product_counts = filtered_df['product_id'].value_counts().to_numpy()
    print('There are', len(product_counts), 'unique products\n')
    
    order_counts = filtered_df['order_id'].value_counts()
    num_orders = len(order_counts)
    num_items = len(product_counts)
    sparsity = 1 - len(transactions) / (num_orders * num_items)
    log.info("Number of orders: {}, number of items: {}".format(num_orders, num_items))
    print(f'matrix sparsity: {sparsity:f}')
    log.info("Matrix sparsity: {}".format(sparsity))

    filtered_df['product_id'] = filtered_df['product_id'].astype(str)
    filtered_df['order_id'] = filtered_df['order_id'].astype(str)

    return filtered_df

