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

def clean_ecommerce(transactions: pd.DataFrame) -> List[pd.DataFrame]:

    print('Unique invoices', len(pd.unique(transactions['InvoiceNo'])))
    print('Unique products', len(pd.unique(transactions['StockCode'])))
    print('Total rows', len(transactions))

    transactions = transactions[(transactions.UnitPrice > 0) & (transactions.Quantity > 0)]

    minimum_order_size = 2
    order_group = transactions.loc[:, ['InvoiceNo', 'StockCode']].groupby('InvoiceNo').count()
    
    multi_order = order_group[(order_group.StockCode >= minimum_order_size)].count()
    single_order = order_group[(order_group.StockCode < minimum_order_size)].count()
    
    print('Orders with at least',minimum_order_size,'products:',multi_order['StockCode'])
    print('Orders with less than',minimum_order_size,'products:',single_order['StockCode'])
    
    # We can capture the list of mutiple product orders with this:
    order_filter = order_group[(order_group.StockCode >= minimum_order_size)].index.tolist()

    filtered_df = transactions[transactions['InvoiceNo'].isin(order_filter)].copy()

    print('Original dataframe length:', len(transactions))
    print('Filtered dataframe length:', len(filtered_df))

    filtered_df['StockCode'] = filtered_df['StockCode'].astype(str)

    item_lookup = filtered_df[['StockCode', 'Description']].drop_duplicates() # Only get unique item/description pairs
    item_lookup['StockCode'] = item_lookup.StockCode.astype(str) # Encode as strings for future lookup ease

    price_lookup = filtered_df[['StockCode', 'UnitPrice']].drop_duplicates()
    price_lookup['StockCode'] = price_lookup.StockCode.astype(str)

    selected_df = filtered_df[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice', 'Description']]
    selected_df.info()

    renamed_df = selected_df.rename(columns={"InvoiceNo": "order_id", 
                                "StockCode": "product_id", 
                                "Description":"description",
                                "Quantity":"quantity",
                                "UnitPrice":"price"})

    products_df = item_lookup.rename(columns={"StockCode":"product_id", "Description":"description"})

    return [renamed_df, products_df]

def clean_jewelry(transactions: pd.DataFrame) -> List[pd.DataFrame]:

    print('Total length is',len(transactions))
    transactions.isna().sum()

    transactions = transactions[(transactions.quantity > 0) & (transactions.price > 0)]

    minimum_purchaces = 2
    product_group = transactions.loc[:, ['order_id', 'product_id']].groupby('product_id').count()
    
    multi_purchase = product_group[(product_group.order_id >= minimum_purchaces)].count()
    single_purchase = product_group[(product_group.order_id < minimum_purchaces)].count()
    
    print('Products with at least',minimum_purchaces,'purchase:',multi_purchase['order_id'])
    print('Products with less than',minimum_purchaces,'purchase:',single_purchase['order_id'])
    
    # We can capture the list of mutiple product orders with this:
    product_filter = product_group[(product_group.order_id >= minimum_purchaces)].index.tolist()

    filtered_df = transactions[transactions['product_id'].isin(product_filter)].copy()

    print('Original dataframe length:', len(transactions))
    print('Filtered dataframe length:', len(filtered_df))

    minimum_order_size = 2
    order_group = filtered_df.loc[:, ['order_id', 'product_id']].groupby('order_id').count()
    
    multi_order = order_group[(order_group.product_id >= minimum_order_size)].count()
    single_order = order_group[(order_group.product_id < minimum_order_size)].count()
    
    print('Orders with at least',minimum_order_size,'products:',multi_order['product_id'])
    print('Orders with less than',minimum_order_size,'products:',single_order['product_id'])
    
    # We can capture the list of mutiple product orders with this:
    order_filter = order_group[(order_group.product_id >= minimum_order_size)].index.tolist()

    filtered_df = filtered_df[filtered_df['order_id'].isin(order_filter)].copy()

    print('Original dataframe length:', len(transactions))
    print('Filtered dataframe length:', len(filtered_df))

    minimum_purchaces = 2
    user_group = transactions.loc[:, ['order_id', 'user_id']].groupby('user_id').count()
    
    multi_purchase = user_group[(user_group.order_id >= minimum_purchaces)].count()
    single_purchase = user_group[(user_group.order_id < minimum_purchaces)].count()
    
    print('Users with at least',minimum_order_size,'purchase:',multi_purchase['order_id'])
    print('Users with less than',minimum_order_size,'purchase:',single_purchase['order_id'])
    
    # We can capture the list of mutiple product orders with this:
    user_filter = user_group[(user_group.order_id >= minimum_order_size)].index.tolist()

    filtered_df = filtered_df[filtered_df['user_id'].isin(user_filter)].copy()

    print('Original dataframe length:', len(transactions))
    print('Filtered dataframe length:', len(filtered_df))

    item_lookup = filtered_df[['product_id', 'category_code']].drop_duplicates() # Only get unique item/description pairs
    item_lookup['product_id'] = item_lookup.product_id.astype(str) # Encode as strings for future lookup ease

    renamed_df = filtered_df[["order_id", "product_id","quantity", "price"]]
    products_df = item_lookup.rename(columns={"StockCode":"product_id", "Description":"description"})

    return [renamed_df, products_df]

def clean_journey(transactions: pd.DataFrame, products: pd.DataFrame) -> List[pd.DataFrame]:

    products['DESC'] = products['COMMODITY_DESC'] + products['SUB_COMMODITY_DESC']
    
    minimum_purchaces = 2
    product_group = transactions.loc[:, ['BASKET_ID', 'PRODUCT_ID']].groupby('PRODUCT_ID').count()
    
    multi_purchase = product_group[(product_group.BASKET_ID >= minimum_purchaces)].count()
    single_purchase = product_group[(product_group.BASKET_ID < minimum_purchaces)].count()
    
    print('Products with at least',minimum_purchaces,'purchase:',multi_purchase['BASKET_ID'])
    print('Products with less than',minimum_purchaces,'purchase:',single_purchase['BASKET_ID'])
    
    # We can capture the list of mutiple product orders with this:
    product_filter = product_group[(product_group.BASKET_ID >= minimum_purchaces)].index.tolist()

    filtered_df = transactions[transactions['PRODUCT_ID'].isin(product_filter)].copy()

    print('Original dataframe length:', len(transactions))
    print('Filtered dataframe length:', len(filtered_df))

    minimum_order_size = 2
    order_group = filtered_df.loc[:, ['BASKET_ID', 'PRODUCT_ID']].groupby('BASKET_ID').count()
    
    multi_order = order_group[(order_group.PRODUCT_ID >= minimum_order_size)].count()
    single_order = order_group[(order_group.PRODUCT_ID < minimum_order_size)].count()
    
    print('Orders with at least',minimum_order_size,'products:',multi_order['PRODUCT_ID'])
    print('Orders with less than',minimum_order_size,'products:',single_order['PRODUCT_ID'])
    
    # We can capture the list of mutiple product orders with this:
    order_filter = order_group[(order_group.PRODUCT_ID >= minimum_order_size)].index.tolist()

    filtered_df = filtered_df[filtered_df['BASKET_ID'].isin(order_filter)].copy()

    print('Original dataframe length:', len(transactions))
    print('Filtered dataframe length:', len(filtered_df))

    minimum_purchaces = 2
    user_group = transactions.loc[:, ['BASKET_ID', 'household_key']].groupby('household_key').count()
    
    multi_purchase = user_group[(user_group.BASKET_ID >= minimum_purchaces)].count()
    single_purchase = user_group[(user_group.BASKET_ID < minimum_purchaces)].count()
    
    print('Users with at least',minimum_order_size,'purchase:',multi_purchase['BASKET_ID'])
    print('Users with less than',minimum_order_size,'purchase:',single_purchase['BASKET_ID'])
    
    # We can capture the list of mutiple product orders with this:
    user_filter = user_group[(user_group.BASKET_ID >= minimum_order_size)].index.tolist()

    filtered_df = filtered_df[filtered_df['household_key'].isin(user_filter)].copy()

    print('Original dataframe length:', len(transactions))
    print('Filtered dataframe length:', len(filtered_df))

    filtered_df = filtered_df.rename(columns={"PRODUCT_ID": "product_id", "QUANTITY": "quantity", "BASKET_ID": "order_id", "SALES_VALUE": "price"})
    final_df = filtered_df[["order_id", "product_id", "quantity", "price"]]
    products = products.rename(columns={"PRODUCT_ID":"product_id", "DESC":"description"})[["product_id", "description"]]

    return [final_df, products]

def clean_retailrocket(events: pd.DataFrame) -> List[pd.DataFrame]:
    transactions = events[events.event == "transaction"].copy()
    transactions['order_id'] = transactions.transactionid.astype(str)
    transactions['customer_id'] = transactions.visitorid.astype(str)
    transactions['product_id'] = transactions.itemid.astype(str)
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

    return filtered_df

def clean_vipin20(transactions: pd.DataFrame) -> List[pd.DataFrame]:
    transactions = transactions[(transactions.NumberOfItemsPurchased > 0) & (transactions.CostPerItem > 0)]
    q = transactions["CostPerItem"].quantile(0.98)
    transactions = transactions[transactions["CostPerItem"] < q]
    q = transactions["NumberOfItemsPurchased"].quantile(0.98)
    transactions = transactions[transactions["NumberOfItemsPurchased"] < q]
    
    minimum_order_size = 2

    order_group = transactions.loc[:, ['TransactionId', 'ItemCode']].groupby('TransactionId').count()
    
    multi_order = order_group[(order_group.ItemCode >= minimum_order_size)].count()
    single_order = order_group[(order_group.ItemCode < minimum_order_size)].count()
    
    print('Orders with at least',minimum_order_size,'products:',multi_order['ItemCode'])
    print('Orders with less than',minimum_order_size,'products:',single_order['ItemCode'])
    
    renamed_df = transactions.rename(columns={"TransactionId": "order_id", 
                            "ItemCode": "product_id", 
                            "ItemDescription":"description",
                            "NumberOfItemsPurchased":"quantity",
                            "CostPerItem":"price"})[['order_id', 'product_id', 'description', 'quantity']]


    item_lookup = transactions[['ItemCode', 'ItemDescription']].drop_duplicates() # Only get unique item/description pairs
    item_lookup['ItemCode'] = item_lookup.ItemCode.astype(str) # Encode as strings for future lookup ease

    products_df = item_lookup.rename(columns={"ItemCode":"product_id", "ItemDescription":"description"})

    return [renamed_df, products_df]

def clean_instacart(transactions: pd.DataFrame, products: pd.DataFrame) -> List[pd.DataFrame]:
    transactions['order_id'] = transactions.order_id.astype(str)
    transactions['product_id'] = transactions.product_id.astype(str)
    products['product_id'] = products.product_id.astype(str)

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
    filtered_df['price'] = 1

    filtered_df = filtered_df[["order_id", "product_id", "price", "quantity"]]
    products["description"] = products["product_name"]
    products = products[["product_id", "description"]]
    return [ filtered_df, products ]