"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

import productrec.pipelines as pipes

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """
    electronics_pipeline = pipes.create_electronics_pipeline()
    brazillian_pipeline = pipes.create_brazillian_pipeline()

    return {
        "electronics": electronics_pipeline,
        "brazillian": brazillian_pipeline,
        "__default__": electronics_pipeline + brazillian_pipeline
    }
