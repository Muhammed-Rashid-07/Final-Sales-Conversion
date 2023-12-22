import streamlit as st
import pandas as pd 
import joblib
import numpy as np



def prediction():
    st.title('Sales Conversion Optimization Model')
    
    try:
        age_group = st.selectbox('Age Group', ['30-34', '35-39', '40-44', '45-49'])
        gender = st.selectbox('Gender',['Male', 'Female'])
        interest = st.number_input('Interest', min_value=0)
        impressions = st.number_input('Impressions', min_value=0)
        clicks = st.number_input('Clicks', min_value=0)
        spent = st.number_input('Spent')
        total_conversion = st.number_input('Total Conversion Rate', min_value=0)
        campaign_936 = st.selectbox('Is Campaign ID 936? ', [True, False])
        campaign_1178 = st.selectbox('Is Campaign ID 1178?', [True, False])


        gender_map = {'Male': 1, 'Female': 0}
        age_group_map = {'30-34': 0, '35-39': 1, '40-44': 2, '45-49': 3}
        interaction_imp_clicks = impressions*clicks


        spent_per_click = spent/clicks
        age = age_group_map[age_group]
        gender_feat = gender_map[gender]


        ctr = clicks / impressions
        conversion_per_impression = total_conversion / impressions
        total_conversion_rate = total_conversion / clicks
        budget_allocation_imp = spent / impressions

        df = {
            'interest': interest,
            'Impressions': impressions,
            'Clicks': clicks,
            'Spent': spent,
            'Total_Conversion': total_conversion,
            'campaign_936': campaign_936,
            'campaign_1178': campaign_1178,
            'Age_Group': age,
            'Gender_Code':gender_feat,
            'Interaction_Imp_Clicks': interaction_imp_clicks,
            'Spent_per_Click': spent_per_click,
            'Total_Conversion_Rate': total_conversion_rate,
            'Budget_Allocation_Imp': budget_allocation_imp,
            'CTR': ctr,
            'Conversion_per_Impression': conversion_per_impression
        }
    
        
        data = pd.Series([interest,impressions, clicks, spent,total_conversion, campaign_936, campaign_1178, age, gender_feat, interaction_imp_clicks, spent_per_click, total_conversion_rate, budget_allocation_imp, ctr, conversion_per_impression])
        if st.button('Predict'):
            model = joblib.load('model/model.pkl')
            print(data)
            data_reshaped = np.array(data).reshape(1, -1)

            output = model.predict(data_reshaped)
            st.success(f"Approved Conversion Rate  :{output}") 
            
    except Exception as e:
        st.error(e)
        
        
        

def display_report(report_path: str):
    """Displays an Evidently HTML report in Streamlit.

    Args:
        report_path: File path of the Evidently HTML report.
    """   
    with open(report_path) as report_file:
        report_html = report_file.read()

    st.components.v1.html(report_html, height=1000, width=1000,scrolling=True)
 

def run_reports():
    data_drift_report = st.checkbox("Data Quality Report")
    model_performance_report = st.checkbox("Model Performance Report")
    model_monitoring_report = st.checkbox("Model Monitoring Report")
    regression_quality_report = st.checkbox("Regression Quality Report")
    
    selected_reports = []
    if data_drift_report:
        selected_reports.append("data_drift_report")
    if model_performance_report:
        selected_reports.append("model_performance_report")
    if model_monitoring_report:
        selected_reports.append("model_monitoring_report")
    if regression_quality_report:   
        selected_reports.append("regression_quality_report")

        
    if 'data_drift_report' in selected_reports:
        display_report("/Users/rashid/Sales-Conversion-Optimization/Sales-Optimization/sales-project/reports/data_drift_report.html")
    if 'model_performance_report' in selected_reports:
        display_report("/Users/rashid/Sales-Conversion-Optimization/Sales-Optimization/sales-project/reports/model_monitoring_report.html")
    if 'model_monitoring_report' in selected_reports:
        display_report("/Users/rashid/Sales-Conversion-Optimization/Sales-Optimization/sales-project/reports/model_performance_test_report.html")
    if 'regression_quality_report' in selected_reports:
        display_report("/Users/rashid/Sales-Conversion-Optimization/Sales-Optimization/sales-project/reports/regression_quality_report.html")
        


if __name__ == '__main__':
    st.sidebar.title("Choose the option")
    selection = st.sidebar.radio("Select an option", ["Prediction", "Reports"])
    
    if selection == "Prediction":
        prediction()
    if selection == "Reports":
        run_reports()
