from kedro.pipeline import Pipeline, node

from productrec.pipelines.scoring.nodes import score_auc

from .cleaning import clean_brazillian, clean_electronics
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