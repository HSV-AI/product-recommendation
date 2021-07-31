import streamlit as st
import pandas as pd
import numpy as np
import implicit

st.image("https://github.com/HSV-AI/hugo-website/blob/master/static/images/logo_v9.png?raw=true")

selected_df = pd.read_pickle('data/interim/selected_invoices.gz')
item_lookup = pd.read_pickle('data/interim/item_lookup.gz')

# Load the Implicit model factors
item_factors = np.load('data/interim/item_factors.npy')
user_factors = np.load('data/interim/user_factors.npy')

product_train = np.load('data/interim/product_train.npy', allow_pickle=True)

alpha = 29
factors = 64
regularization = 0.117
iterations = 73

model = implicit.als.AlternatingLeastSquares(factors=factors,
                                    regularization=regularization,
                                    iterations=iterations)

model.user_factors = user_factors
model.item_factors = item_factors

invoices = selected_df.InvoiceNo.unique()
products = selected_df.StockCode.unique()

selection = st.selectbox('Select an invoice', np.random.choice(invoices, 5))

invoice_df = selected_df[selected_df.InvoiceNo == selection]

display_df = invoice_df.merge(item_lookup, on='StockCode')

st.write("""
# Invoice Contents
""")

st.write("The invoice",selection,'containes',len(display_df.StockCode.unique()),'items, displayed below:')
st.table(display_df)

invoice_index = list(invoices).index(selection)
user_items = (product_train * 1).astype('double').T.tocsr()
recommendations = model.recommend(invoice_index, user_items)

st.write('Recommended items based on all other invoices:')

probabilities = []
stock_codes = []
descriptions = []
for rec in recommendations:
    index = rec[0]
    prob = rec[1]
    probabilities.append(prob)
    stock_code = products[index]
    stock_codes.append(stock_code)
    item = item_lookup[item_lookup.StockCode == stock_code].values
    description = item[0][1]
    descriptions.append(description)

recommendation_df = pd.DataFrame({'Probability':probabilities,'StockCode':stock_codes,'Description':descriptions})
st.table(recommendation_df)