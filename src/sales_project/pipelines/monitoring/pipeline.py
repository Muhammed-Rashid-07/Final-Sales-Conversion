# """
# This is a boilerplate pipeline 'monitoring'
# generated using Kedro 0.19.1
# """

from kedro.pipeline import Pipeline, pipeline,node
from .nodes import regression_quality, data_split, model_monitoring, model_performance_test, data_drift

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=data_split,
            inputs='data',
            outputs=['reference_data', 'current_data'],
            name='data_split_node'
        ),
        node(
            func=regression_quality,
            inputs=['reference_data', 'current_data','model'],
            outputs= 'regression_quality_metrics',
            name='regression_quality_node'
        ),
        node(
            func=data_drift,
            inputs=['reference_data', 'current_data','model'],
            outputs= 'data_drift_metrics',
            name='regression_performance_node'
        ),
        node(
            func=model_performance_test,
            inputs=['reference_data', 'current_data','model'],
            outputs='test_status',
            name='model_performance_test_node'
        ),
        node(
            func=model_monitoring,
            inputs=['reference_data', 'current_data','model'],
            outputs='model_monitoring_metrics',
            name='model_monitoring_node'
        ),
        
    ])
