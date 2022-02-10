from kedro.pipeline import Pipeline, node

from .transform import (
    transform_vipin20,
    transform_electronics,
    transform_brazilian,
    transform_ecommerce,
    transform_jewelry,
    transform_journey,
    transform_retailrocket,
    transform_instacart
)

from .cleaning import clean_data
from .splitting import split_data
from .training import train_implicit
from .scoring import (
    score_auc,
    score_confusion
) 

def create_electronics_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                transform_electronics,
                "electronics_kaggle_data",
                ["transactions", "products"],
                name="transform_electronics",
            ),
        ]
    )

def create_brazilian_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                transform_brazilian,
                ["brazilian_kaggle_order_data", "brazilian_kaggle_product_data", "brazilian_kaggle_customer_data"],
                ["transactions", "products"],
                name="brazilian"
            ),
        ]
    )

def create_ecommerce_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                transform_ecommerce,
                "ecommerce_kaggle_data",
                ["transactions", "products"],
                name="transform_ecommerce"
            ),
        ]
    )

def create_jewelry_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                transform_jewelry,
                "jewelry_kaggle_data",
                ["transactions", "products"],
                name="transform_jewelry"
            )
        ]
    )

def create_journey_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                transform_journey,
                ["journey_kaggle_transaction_data", "journey_kaggle_product_data"],
                ["transactions", "products"],
                name="transform_journey"
            )
        ]
    )

def create_retailrocket_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                transform_retailrocket,
                "retailrocket_kaggle_event_data",
                "transactions",
                name="transform_retailrocket"
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
                transform_instacart,
                ["instacart_kaggle_order_data", "instacart_kaggle_product_data"],
                ["transactions", "products"],
                name="transform_instacart"
            )
        ]
    )

def create_implicit_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                clean_data,
                ["transactions", "parameters"],
                "clean_transactions",
                name="clean_data"
            ),
            node(
                split_data,
                ["clean_transactions", "parameters"],
                ["train", "test"],
                name="split_data"
            ),
            node(
                train_implicit,
                ["train", "parameters"],
                ["user_factors", "item_factors", "product_train"],
                name="train_implicit"
            ),
            node(
                score_confusion,
                ["train", "test",
                    "user_factors", "item_factors", "parameters"],
                "score",
                name="score_implicit"
            )
        ]
    )
