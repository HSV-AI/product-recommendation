from kedro.pipeline import Pipeline, node

from productrec.pipelines.scoring.nodes import score_auc

from .cleaning import clean_brazillian, clean_electronics, clean_ecommerce, clean_jewelry
from .splitting import split_data
from .training import train_implicit
from productrec.pipelines import splitting

def create_electronics_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                clean_electronics,
                "electronics_kaggle_data",
                ["electronics_transactions", "electronics_products"],
                name="clean_electronics",
            ),
             node(
                split_data,
                "electronics_transactions",
                ["electronics_train", "electronics_test", "electronics_products_altered", "electronics_transactions_altered"],
                name="split_electronics_data"
            ),
            node(
                train_implicit,
                ["electronics_train", "electronics_hyperparameters"],
                ["electronics_user_factors", "electronics_item_factors", "electronics_product_train"],
                name="train_implicit_electronics"
            ),
            node(
                score_auc,
                ["electronics_train", "electronics_test", "electronics_products_altered", 
                    "electronics_user_factors", "electronics_item_factors", "electronics_hyperparameters"],
                "electronics_score",
                name="score_electronics"
            )
        ]
    )

def create_brazillian_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                clean_brazillian,
                ["brazillian_kaggle_order_data", "brazillian_kaggle_product_data", "brazillian_kaggle_customer_data"],
                ["brazillian_transactions", "brazillian_products"],
                name="clean_brazillian"
            ),
            node(
                split_data,
                "brazillian_transactions",
                ["brazillian_train", "brazillian_test", "brazillian_products_altered", "brazillian_transactions_altered"],
                name="split_brazillian_data"
            ),
            node(
                train_implicit,
                ["brazillian_train", "brazillian_hyperparameters"],
                ["brazillian_user_factors", "brazillian_item_factors", "brazillian_product_train"],
                name="train_implicit_brazillian"
            ),
            node(
                score_auc,
                ["brazillian_train", "brazillian_test", "brazillian_products_altered", 
                    "brazillian_user_factors", "brazillian_item_factors", "brazillian_hyperparameters"],
                "brazillian_score",
                name="score_brazillian"
            )
        ]
    )

def create_ecommerce_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                clean_ecommerce,
                "ecommerce_kaggle_data",
                ["ecommerce_transactions", "ecommerce_products"],
                name="clean_ecommerce"
            ),
            node(
                split_data,
                "ecommerce_transactions",
                ["ecommerce_train", "ecommerce_test", "ecommerce_products_altered", "ecommerce_transactions_altered"],
                name="split_ecommerce_data"
            ),
            node(
                train_implicit,
                ["ecommerce_train", "ecommerce_hyperparameters"],
                ["ecommerce_user_factors", "ecommerce_item_factors", "ecommerce_product_train"],
                name="train_implicit_ecommerce"
            ),
            node(
                score_auc,
                ["ecommerce_train", "ecommerce_test", "ecommerce_products_altered", 
                    "ecommerce_user_factors", "ecommerce_item_factors", "ecommerce_hyperparameters"],
                "ecommerce_score",
                name="score_ecommerce"
            )
        ]
    )

def create_jewelry_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                clean_jewelry,
                "jewelry_kaggle_data",
                ["jewelry_transactions", "jewelry_products"],
                name="clean_jewelry"
            ),
            node(
                split_data,
                "jewelry_transactions",
                ["jewelry_train", "jewelry_test", "jewelry_products_altered", "jewelry_transactions_altered"],
                name="split_jewelry_data"
            ),
            node(
                train_implicit,
                ["jewelry_train", "jewelry_hyperparameters"],
                ["jewelry_user_factors", "jewelry_item_factors", "jewelry_product_train"],
                name="train_implicit_jewelry"
            ),
            node(
                score_auc,
                ["jewelry_train", "jewelry_test", "jewelry_products_altered", 
                    "jewelry_user_factors", "jewelry_item_factors", "jewelry_hyperparameters"],
                "jewelry_score",
                name="score_jewelry"
            )
        ]
    )