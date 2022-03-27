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

    user_counts = transactions[transactions['customer_id'] > 0] \
        .drop_duplicates(['customer_id', 'order_id']) \
        .groupby('customer_id')['order_id'] \
        .count() \
        .sort_values(ascending=False)

    user_df = user_counts \
        .reset_index() \
        .rename(columns={"customer_id":"Customer", "order_id":"Orders"})

    customer_table = wandb.Table(dataframe=user_df[:10])
    wandb.log({"top_10_customer_by_orders": customer_table})

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

    product_counts = transactions[transactions['product_id'] > 0] \
        .groupby(transactions.product_id)['quantity'] \
        .agg('sum'). \
        sort_values(ascending=False)

    product_df = product_counts \
        .reset_index() \
        .rename(columns={"product_id":"Product", "quantity":"Quantity"})

    product_table = wandb.Table(dataframe=product_df[:10])
    wandb.log({"top_10_products_by_orders": product_table})

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
