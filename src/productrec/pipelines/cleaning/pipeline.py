from kedro.pipeline import Pipeline, node

from .nodes import clean_electronics

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                clean_electronics,
                "electronics_kaggle_data",
                ["electronics_transactions", "electronics_products"],
                name="clean_electronics",
            )
        ]
    )
