"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

import productrec.pipelines as pipes

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """
    vipin20_pipeline = pipes.create_vipin20_pipeline()
    implicit_pipeline = pipes.create_implicit_pipeline()
    electronics_pipeline = pipes.create_electronics_pipeline()

    return {
        "vipin20": vipin20_pipeline,
        "electronics": electronics_pipeline,
        "implicit": implicit_pipeline,
        "__default__": vipin20_pipeline
    }
