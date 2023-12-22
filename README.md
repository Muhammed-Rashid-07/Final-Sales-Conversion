# Sales Conversion Optimization Project

## Table of Contents

## Table of Contents

1. [Project Description]
2. [Project Structure]
3. [Necessary Installations](#necessary-installations) 🛠️
4. [Training Pipeline](#train-pipeline) 🚂
5. [Model Monitoring]
6. [Streamlit Web Application]

## Project Description

In this project we are going to create an end to end sales conversion prediction model using kedro, mlflow, evidently, and streamlit

We use kedro as workflow orchestrator and mlflow for experiment tracking, evidently AI for monitoring and streamlit for creating web application. By using this technologies will help us to build a robust Sales Conversion prediction Model.


## How to install dependencies

Let's start the project by installing the required libraries.

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```
pip install -r requirements.txt
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```


## Project dependencies

To see and update the dependency requirements for your project use `requirements.txt`. You can install the project requirements with `pip install -r requirements.txt`.


### Training Dateset

1. ad_id:- An unique ID for each ad.

2. xyz_campaign_id - An ID associated with each ad campaign of XYZ company.

3. fb_campaign_id - An ID associated with how Facebook tracks each campaign.

4. age - Age of the person to whom the ad is shown.

5. gender - Gender of the person to whim the add is shown

6. interest - A code specifying the category to which the person’s interest belongs (interests are as mentioned in the person’s Facebook public profile).

7. Impressions - The number of times the ad was shown.

8. Clicks - Number of clicks on for that ad.

9. Spent - Amount paid by company xyz to Facebook, to show that ad.

10. Total conversion - Total number of people who enquired about the product after seeing the ad.

11 .Approved conversion - Total number of people who bought the product after seeing the ad. <--- Target Class


### Training Pipeline

1. Data Preprocessing - the raw is will process using some encoding, droping unwanted features and feature engineering etc.
2. Model Training -  Training the model with best result
3. Evaluation of model - Evaluating the accuracy of the model.
4. Monitoring - monitoring the model and data to identify,  if there is any change in model accuracy and data.

### Run the Application

Run the application of streamlit using this command:

```
streamlit run streamlit_app.py
```