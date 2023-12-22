"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import preprocess_data, data_split


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=preprocess_data,
            inputs="raw_data",
            outputs=["data","sale_columns"],
            name="data_preprocessing_node"
        ),
        
        node(
            func=data_split,
            inputs="data",
            outputs=["X_train", "X_test", "y_train", "y_test"],
            name="train_test_split_node"
        )
        
    ])
