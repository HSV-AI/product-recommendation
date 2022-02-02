from kedro.pipeline import Pipeline, node

from productrec.pipelines.scoring.nodes import score_auc
from productrec.pipelines.transform.electronics import transform_electronics

from .transform import (
    transform_vipin20,
    transform_electronics
)

from .cleaning import ( 
    clean_brazillian, 
    clean_ecommerce, clean_journey,
    clean_jewelry, clean_instacart, 
    clean_retailrocket, clean_vipin20
)

from .splitting import split_data
from .training import train_implicit
from productrec.pipelines import splitting

def create_electronics_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                transform_electronics,
                "electronics_kaggle_data",
                ["products", "transactions"],
                name="transform_electronics",
            ),
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

def create_journey_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                clean_journey,
                ["journey_kaggle_transaction_data", "journey_kaggle_product_data"],
                ["journey_transactions", "journey_products"],
                name="clean_journey"
            ),
            node(
                split_data,
                "journey_transactions",
                ["journey_train", "journey_test", "journey_products_altered", "journey_transactions_altered"],
                name="split_journey_data"
            ),
            node(
                train_implicit,
                ["journey_train", "journey_hyperparameters"],
                ["journey_user_factors", "journey_item_factors", "journey_product_train"],
                name="train_implicit_journey"
            ),
            node(
                score_auc,
                ["journey_train", "journey_test", "journey_products_altered", 
                    "journey_user_factors", "journey_item_factors", "journey_hyperparameters"],
                "journey_score",
                name="score_journey"
            )
        ]
    )

def create_retailrocket_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                clean_retailrocket,
                "retailrocket_kaggle_event_data",
                "retailrocket_transactions",
                name="clean_retailrocket"
            ),
            node(
                split_data,
                "retailrocket_transactions",
                ["retailrocket_train", "retailrocket_test", "retailrocket_products_altered", "retailrocket_transactions_altered"],
                name="split_retailrocket_data"
            ),
            node(
                train_implicit,
                ["retailrocket_train", "retailrocket_hyperparameters"],
                ["retailrocket_user_factors", "retailrocket_item_factors", "retailrocket_product_train"],
                name="train_implicit_retailrocket"
            ),
            node(
                score_auc,
                ["retailrocket_train", "retailrocket_test", "retailrocket_products_altered", 
                    "retailrocket_user_factors", "retailrocket_item_factors", "retailrocket_hyperparameters"],
                "retailrocket_score",
                name="score_retailrocket"
            )
        ]
    )

def create_vipin20_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                transform_vipin20,
                "vipin20_kaggle_data",
                ["transactions", "products"],
                name="transform_vipin20"
            ),
        ]
    )

def create_instacart_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                clean_instacart,
                ["instacart_kaggle_order_data", "instacart_kaggle_product_data"],
                ["instacart_transactions", "instacart_products"],
                name="clean_instacart"
            ),
            node(
                split_data,
                "instacart_transactions",
                ["instacart_train", "instacart_test", "instacart_products_altered", "instacart_transactions_altered"],
                name="split_instacart_data"
            ),
            node(
                train_implicit,
                ["instacart_train", "instacart_hyperparameters"],
                ["instacart_user_factors", "instacart_item_factors", "instacart_product_train"],
                name="train_implicit_instacart"
            ),
            node(
                score_auc,
                ["instacart_train", "instacart_test", "instacart_products_altered", 
                    "instacart_user_factors", "instacart_item_factors", "instacart_hyperparameters"],
                "instacart_score",
                name="score_instacart"
            )
        ]
    )

def create_implicit_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                split_data,
                "transactions",
                ["train", "test", "products_altered", "transactions_altered"],
                name="split_data"
            ),
            node(
                train_implicit,
                ["train", "parameters"],
                ["user_factors", "item_factors", "product_train"],
                name="train_implicit"
            ),
            node(
                score_auc,
                ["train", "test", "products_altered", 
                    "user_factors", "item_factors", "parameters"],
                "score",
                name="score_implicit"
            )
        ]
    )
