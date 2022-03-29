from typing import Any, Dict, List

import pandas as pd
import numpy as np
import logging
import wandb
from matplotlib import pyplot as plt

def report(transactions: pd.DataFrame, params: Dict) -> pd.DataFrame:

    log = logging.getLogger(__name__)

    wandb.init(
        project=params["wandb_project"],
        notes="implicit_pipeline",
        config=params,
    )

    # Log basic statistics for the transactions
    order_count = len(pd.unique(transactions['order_id']))
    customer_count = len(pd.unique(transactions['customer_id']))
    product_count = len(pd.unique(transactions["product_id"]))
    purchase_count = len(transactions)
    wandb.log({
        "order_count": order_count,
        "customer_count": customer_count,
        "product_count": product_count,
        "purchase_count": purchase_count
    })

    # Log some graphs for customers
    user_counts = transactions \
        .drop_duplicates(['customer_id', 'order_id']) \
        .groupby('customer_id')['order_id'] \
        .count() \
        .sort_values(ascending=False)

    user_df = user_counts \
        .reset_index() \
        .rename(columns={"customer_id":"Customer", "order_id":"Orders"})

    customer_table = wandb.Table(dataframe=user_df[:10])
    wandb.log({"top_10_customer_by_orders": customer_table})

    plt.plot(user_counts.values) 
    wandb.log({
        "orders_by_customers_plot": plt
    })

    # Log some graphs for products
    product_counts = transactions \
        .drop_duplicates(['product_id', 'order_id']) \
        .groupby('product_id')['order_id'] \
        .count() \
        .sort_values(ascending=False)

    product_df = product_counts \
        .reset_index() \
        .rename(columns={"product_id":"Product", "order_id":"Orders"})

    product_table = wandb.Table(dataframe=product_df[:10])
    wandb.log({"top_10_product_by_orders": product_table})

    plt.plot(product_counts.values) 
    wandb.log({
        "products_by_orders_plot": plt
    })

    # Break down users based on # orders vs total count of orders
    temp = (100. * user_counts / user_counts.sum()).sort_values(ascending=False)

    count = 0
    total = 0
    buckets=[]
    for val in temp:
        
        if total + val > 25:
            buckets.append(count)
            total = 0
            count = 0
            
        count+=1
        total+=val

    labels = ['Top 25%', '2nd 25%', '3rd 25%', '4th 25%']
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    plt.pie(buckets, labels=labels, autopct=lambda p: '{:.0f}'.format(p * len(temp) / 100))
    fig1.gca().set_title("Breakdown of customers by order count")
    wandb.log({"customer_breakdown": wandb.Image(plt)})

    product_counts = transactions \
        .groupby(transactions.product_id)['order_id'] \
        .count(). \
        sort_values(ascending=False)

    product_df = product_counts \
        .reset_index() \
        .rename(columns={"product_id":"Product", "quantity":"Quantity"})

    product_table = wandb.Table(dataframe=product_df[:10])
    wandb.log({"top_10_products_by_orders": product_table})

    # Break down products based on # orders vs total count of orders
    temp = (100. * product_counts / product_counts.sum()).sort_values(ascending=False)

    count = 0
    total = 0
    buckets=[]
    for val in temp:
        
        if total + val > 25:
            buckets.append(count)
            total = 0
            count = 0
            
        count+=1
        total+=val

    labels = ['Top 25%', '2nd 25%', '3rd 25%', '4th 25%']
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    plt.pie(buckets, labels=labels, autopct=lambda p: '{:.0f}'.format(p * len(temp) / 100))
    fig1.gca().set_title("Breakdown of products by order count")
    wandb.log({"product_breakdown": wandb.Image(plt)})

