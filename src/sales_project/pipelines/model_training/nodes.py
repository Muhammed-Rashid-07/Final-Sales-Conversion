"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import logging
import mlflow
from typing_extensions import Dict
from mlflow import MlflowClient
import pandas as pd
import pickle
import numpy as np

def train_model(X_train:pd.DataFrame, y_train:pd.Series):
    """Tracking the model """
    mlflow.search_registered_models()
    mlflow.set_tracking_uri('sqlite:///mlruns.db')
    mlflow.set_experiment('Sales Conversion Optimization model')
    # Start MLflow run
    """Train the model"""
    model = LinearRegression()
    mlflow.sklearn.autolog()
    mlflow.register_model(model_uri="/Users/rashid/Sales-Conversion-Optimization/Sales-Optimization/sales-project/mlruns/1/d625779cbb8a4d7198fba6e1f2bc8634/artifacts/model", name="Lr_model")
    client = MlflowClient()
    client.set_registered_model_alias(name='Lr_model', alias='Champion',version='4')
    model.fit(X_train, y_train)
    return model


def evaluate_model(X_test:pd.DataFrame|pd.Series, y_test:pd.Series, model) -> Dict[str, float] :
    """Evaluate the model"""
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred) 
    
    logger = logging.getLogger(__name__)
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"R-squared: {r2:.2f}")
    logging.info("Model has a coefficient R2 of %.3f on test data", r2)
    return {
        "mse": mse,
        "mae": mae,
        "r2": r2
    }
    
