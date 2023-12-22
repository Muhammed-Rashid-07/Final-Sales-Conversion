"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.14
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split    
from typing import Tuple, Dict

def encoding(data: pd.DataFrame) -> pd.DataFrame:
    label_encoder = LabelEncoder()
    data['Age_Group'] = label_encoder.fit_transform(data['age'])
    data['Gender_Code'] = data['gender'].map({'F':0, 'M':1})
    data = pd.get_dummies(data, columns=['xyz_campaign_id'], prefix='campaign', drop_first=True)
    df = data
    return df

def feature_engineering(data:pd.DataFrame) -> pd.DataFrame:
    # Interaction Features
    data['Interaction_Imp_Clicks'] = data['Impressions'] * data['Clicks']

    # Spent per Click
    data['Spent_per_Click'] = data['Spent'] / data['Clicks']

    # Total Conversion Rate
    data['Total_Conversion_Rate'] = data['Total_Conversion'] / data['Clicks']

    # Budget Allocation
    data['Budget_Allocation_Imp'] = data['Spent'] / data['Impressions']

    # Ad Performance Metrics
    data['CTR'] = data['Clicks'] / data['Impressions']
    data['Conversion_per_Impression'] = data['Total_Conversion'] / data['Impressions']

    df = data
    return df


def reduntant_columns(data:pd.DataFrame) -> pd.DataFrame:
    data.drop(['age', 'gender','ad_id', 'fb_campaign_id'], axis=1, inplace=True)
    df = data
    print(data.dtypes)
    return df


def null_infi_value(data:pd.DataFrame) -> pd.DataFrame:
    # Replace infinite values with NaN
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.fillna(0, inplace=True)
    print("preprocessing done")
    df = data
    return df

    
def preprocess_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """Preprocess the raw data for training"""
    
    # Data cleaning
    data = encoding(data)
    
    # Feature engineering 
    data = feature_engineering(data)
    
    # Remove redundant columns
    data = reduntant_columns(data)
    
    # Handle nulls and infinities
    data = null_infi_value(data)
    
    
    return data, {"columns":data.columns.tolist(), "data_type":"data"}

def data_split(data: pd.DataFrame) -> tuple[
        pd.DataFrame, 
        pd.DataFrame, 
        pd.Series, 
        pd.Series
    ]:
    X = data.drop(['Approved_Conversion'], axis=1)
    y = data['Approved_Conversion']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    return X_train, X_test, y_train, y_test
    