
import pandas as pd
from typing import Any, Dict, Tuple
import pandas as pd
from evidently import ColumnMapping
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import RegressionErrorPlot, RegressionErrorDistribution, RegressionQualityMetric
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.tests import TestValueMeanError, TestValueMAE
from sklearn.model_selection import train_test_split
import joblib



def build_regression_quality_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    column_mapping: ColumnMapping,
) -> Any:
    model_report = Report(
        metrics= [
            RegressionQualityMetric(),
        ]
    )
    model_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping,
    )
    get_regression_quality_metrics(model_report)
    return model_report


def get_regression_quality_metrics(regression_quality_report: Report) -> Dict:
    metrics = {}
    report_dict = regression_quality_report.as_dict()
    
    metrics["me"] = report_dict["metrics"][0]["result"]["current"]["mean_error"]
    metrics["rmse"] = report_dict["metrics"][0]["result"]["current"]["rmse"]
    
    return metrics


def build_data_drift_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    column_mapping: ColumnMapping,
    drift_share=0.4
) -> Report:
    """_summary_

    Args:
        reference_data (pd.DataFrame): _description_
        current_data (pd.DataFrame): _description_
        column_mapping (ColumnMapping): _description_
        drift_share (float, optional): _description_. Defaults to 0.4.

    Returns:
        Report: _description_
    """
    data_drift_report = Report(metrics=[DataDriftPreset(drift_share=drift_share)])
    data_drift_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping,
    )
    return data_drift_report


def get_data_drift_metrics(report: Dict) -> Dict:
    metrics = {}
    report_dict = report.as_dict()
    for metric in [
        "dataset_drift",
        "number_of_drifted_columns",
        "share_of_drifted_columns",
    ]:
        metrics.update({metric: report_dict["metrics"][0]["result"][metric]})

    return metrics


def build_model_performance_test_report(
    current_data: pd.DataFrame, column_mapping: ColumnMapping
) -> Report:
    """
    Returns a list with pairs (feature_name, drift_score)
    Drift Score depends on the selected statistical test or distance and the threshold
    """
    regression_performance_test = TestSuite(
        tests=[
            TestValueMeanError(lte=10, gte=-10),
            TestValueMAE(lte=15),
        ]
    )

    regression_performance_test.run(
        reference_data=None,
        current_data=current_data,
        column_mapping=column_mapping,
    )

    return regression_performance_test



def get_test_status(report) -> Dict:
    """
    Returns a list with pairs (feature_name, drift_score)
    Drift Score depends on the selected statistical test or distance and the threshold
    """
    FAIL = 0
    SUCCESS = 1

    for test in report.as_dict()["tests"]:
        if test["status"] == "FAIL":
            return FAIL

    return SUCCESS



def build_model_monitoring_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    column_mapping: ColumnMapping,
) -> Any:

    model_report = Report(
        metrics=[
            RegressionQualityMetric(),
            RegressionErrorPlot(),
            RegressionErrorDistribution(),
        ]
    )
    model_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping,
    )

    return model_report


def get_model_monitoring_metrics(regression_quality_report: Report) -> Dict:

    metrics = {}
    report_dict = regression_quality_report.as_dict()

    metrics["me"] = report_dict["metrics"][0]["result"]["current"]["mean_error"]
    metrics["rmse"] = report_dict["metrics"][0]["result"]["current"]["rmse"]
    metrics["mape"] = report_dict["metrics"][0]["result"]["current"][
        "mean_abs_perc_error"
    ]

    return metrics