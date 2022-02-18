![Training Pipeline](https://github.com/HSV-AI/product-recommendation/actions/workflows/python-app.yml/badge.svg)
![Docker Pipeline](https://github.com/HSV-AI/product-recommendation/actions/workflows/docker-build.yml/badge.svg)

# Product Recommendation

This project consists of investigations of product recommendation approaches and open datasets. The intent is to focus on implicit datasets with very limited knowledge of a user's past history or preferences.

The focus for this project is more application than theory. It uses existing libraries for the most part and attempts to tune the training of models based on the available datasets.

## Libraries

### [Surprise](https://github.com/NicolasHug/Surprise)

Surprise is a Python scikit for building and analyzing recommender systems that deal with explicit rating data.

*While the Surprise library is intented to be used only with explicit data, we attempted to make it work by setting all rationgs to the same value.*

### [Implicit](https://github.com/benfred/implicit)

Fast Python Collaborative Filtering for Implicit Datasets.

This project provides fast Python implementations of several different popular recommendation algorithms for implicit feedback datasets:

* Alternating Least Squares as described in the papers Collaborative Filtering for Implicit Feedback Datasets and in Applications of the Conjugate Gradient Method for Implicit Feedback Collaborative Filtering.
* Bayesian Personalized Ranking
* Logistic Matrix Factorization
* Item-Item Nearest Neighbour models, using Cosine, TFIDF or BM25 as a distance metric

## Notes

This project uses several datasets from Kaggle. You will need to create your own Kaggle accound and use your key to download data. We do not re-host their datasets.

## Reference Datasets

Here is a list of available datasets for training and evaluation - most from Kaggle.

### [eCommerce purchase history from electronics store](https://www.kaggle.com/mkechinov/ecommerce-purchase-history-from-electronics-store)

This dataset contains 2.6M purchased products from online store. This file contains purchase data from April 2020 to November 2020 from a large home appliances and electronics online store.

Each row in the file represents an event. All events are related to products and users. Each event is like many-to-many relation between products and users.

Data collected by [Open CDP](https://rees46.com/en/open-cdp) project. Feel free to use open source customer data platform.

### [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/olistbr/brazilian-ecommerce)

100,000 Orders with product, customer and reviews info

Welcome! This is a Brazilian ecommerce public dataset of orders made at Olist Store. The dataset has information of 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil. Its features allows viewing an order from multiple dimensions: from order status, price, payment and freight performance to customer location, product attributes and finally reviews written by customers. We also released a geolocation dataset that relates Brazilian zip codes to lat/lng coordinates.

This is real commercial data, it has been anonymised, and references to the companies and partners in the review text have been replaced with the names of Game of Thrones great houses.

### [E-Commerce Data](https://www.kaggle.com/carrie1/ecommerce-data/home)

Actual transactions from UK retailer

Typically e-commerce datasets are proprietary and consequently hard to find among publicly available data. However, The [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/index.php) has made this dataset containing actual transactions from 2010 and 2011. The dataset is maintained on their site, where it can be found by the title "Online Retail".

Possibly need to update from the latest dataset from UCI [here](http://archive.ics.uci.edu/ml/datasets/Online+Retail+II)

### [Retailrocket recommender system dataset](https://www.kaggle.com/retailrocket/ecommerce-dataset/home?select=events.csv)

Ecommerce data: web events, item properties (with texts), category tree

The dataset consists of three files: a file with behaviour data (events.csv), a file with item properties (itemproperties.сsv) and a file, which describes category tree (categorytree.сsv). The data has been collected from a real-world ecommerce website. It is raw data, i.e. without any content transformations, however, all values are hashed due to confidential issues. The purpose of publishing is to motivate researches in the field of recommender systems with implicit feedback.