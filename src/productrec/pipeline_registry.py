"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

import productrec.pipelines as pipes

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """
    implicit_pipeline = pipes.create_implicit_pipeline()
    vipin20_pipeline = pipes.create_vipin20_pipeline() + implicit_pipeline
    electronics_pipeline = pipes.create_electronics_pipeline() + implicit_pipeline
    brazilian_pipeine = pipes.create_brazilian_pipeline() + implicit_pipeline
    ecommerce_pipeline = pipes.create_ecommerce_pipeline() + implicit_pipeline
    jewelry_pipeline = pipes.create_jewelry_pipeline() + implicit_pipeline
    journey_pipelie = pipes.create_journey_pipeline() + implicit_pipeline
    retailrocket_pipeline = pipes.create_retailrocket_pipeline() + implicit_pipeline
    instacart_pipeline = pipes.create_instacart_pipeline() + implicit_pipeline

    return {
        "vipin20": vipin20_pipeline,
        "electronics": electronics_pipeline,
        "brazilian": brazilian_pipeine,
        "ecommerce": ecommerce_pipeline,
        "jewelry": jewelry_pipeline,
        "journey": journey_pipelie,
        "retailrocket": retailrocket_pipeline,
        "instacart": instacart_pipeline,
        "implicit": implicit_pipeline,
        "__default__": vipin20_pipeline
    }
