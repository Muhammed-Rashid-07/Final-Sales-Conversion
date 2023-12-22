"""
This is a boilerplate pipeline 'monitoring'
generated using Kedro 0.19.1
"""

from evidently import ColumnMapping
from typing import Any, Dict, Tuple
import pandas as pd
from .reports import (
    build_regression_quality_report,
    get_regression_quality_metrics,
    build_data_drift_report,
    get_data_drift_metrics,
    build_model_performance_test_report,
    get_test_status,
    build_model_monitoring_report,
    get_model_monitoring_metrics,
)
import joblib
from sklearn.model_selection import train_test_split
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, RegressionPreset


def set_columns_mapping() -> Any:
    target =  'Approved_Conversion'
    prediction = 'prediction'
    numerical_features = ['interest', 'Impressions', 'Clicks', 'Spent', 'Total_Conversion',
    'Age_Group', 'Gender_Code', 'campaign_936',
    'campaign_1178', 'Interaction_Imp_Clicks', 'Spent_per_Click',
    'Total_Conversion_Rate', 'Budget_Allocation_Imp', 'CTR',
    'Conversion_per_Impression']
    categorical_features = []
    feature_columns = numerical_features
    column_mapping = ColumnMapping(
        target=target,
        numerical_features=numerical_features,  
        categorical_features=categorical_features,
        prediction=prediction
    )
    return column_mapping
    

def data_split(df:pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    reference_data, current_data = train_test_split(df, test_size=0.2, random_state=42)
    return reference_data, current_data


def regression_quality(reference_data, current_data, model) -> Dict:
    print(reference_data.columns)
    column_mapping = set_columns_mapping()
    reference_data['prediction'] = model.predict(reference_data[column_mapping.numerical_features])
    current_data['prediction'] = model.predict(current_data[column_mapping.numerical_features])
    regression_quality_report = build_regression_quality_report(
        reference_data,
        current_data,
        column_mapping,
    )
    regression_quality_metrics = get_regression_quality_metrics(regression_quality_report)
    regression_quality_report.save_html("/Users/rashid/Sales-Conversion-Optimization/Sales-Optimization/sales-project/reports/regression_quality_report.html")
    return regression_quality_metrics
    
    
    
def data_drift(reference_data, current_data, model) -> Dict:
    column_mapping = set_columns_mapping()
    reference_data['prediction'] = model.predict(reference_data[column_mapping.numerical_features])
    current_data['prediction'] = model.predict(current_data[column_mapping.numerical_features])
    data_drift_report = build_data_drift_report(
        reference_data,
        current_data,
        column_mapping,
    )
    data_drift_metrics = get_data_drift_metrics(data_drift_report)
    data_drift_report.save_html("/Users/rashid/Sales-Conversion-Optimization/Sales-Optimization/sales-project/reports/data_drift_report.html")
    return data_drift_metrics



def model_performance_test(reference_data, current_data, model) -> Dict:
    column_mapping = set_columns_mapping()
    current_data['prediction'] = model.predict(current_data[column_mapping.numerical_features])
    model_performance_test_report = build_model_performance_test_report(
        current_data,
        column_mapping,
    )
    test_status = get_test_status(model_performance_test_report)
    model_performance_test_report.save_html("/Users/rashid/Sales-Conversion-Optimization/Sales-Optimization/sales-project/reports/model_performance_test_report.html")
    return test_status



def model_monitoring(reference_data, current_data, model) -> Dict:
    column_mapping = set_columns_mapping()
    reference_data['prediction'] = model.predict(reference_data[column_mapping.numerical_features])
    current_data['prediction'] = model.predict(current_data[column_mapping.numerical_features])
    model_monitoring_report = build_model_monitoring_report(
        reference_data,
        current_data,
        column_mapping,
    )
    model_monitoring_metrics = get_model_monitoring_metrics(model_monitoring_report)
    model_monitoring_report.save_html("/Users/rashid/Sales-Conversion-Optimization/Sales-Optimization/sales-project/reports/model_monitoring_report.html")
    return model_monitoring_metrics