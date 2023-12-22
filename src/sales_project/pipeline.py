from sales_project.pipelines import data_preprocessing as dp
from sales_project.pipelines import model_training as mt
from sales_project.pipelines import monitoring as mon 

def create_pipelines(**kwargs):
    data_processing_pipeline = dp.create_pipeline()
    model_training_pipeline = mt.create_pipeline()
    monitoring_pipeline = mon.create_pipeline()
    return {
        "de": data_processing_pipeline,
        "mt": model_training_pipeline,
        "mon": monitoring_pipeline,
        "__default__": data_processing_pipeline + model_training_pipeline + monitoring_pipeline,
    }