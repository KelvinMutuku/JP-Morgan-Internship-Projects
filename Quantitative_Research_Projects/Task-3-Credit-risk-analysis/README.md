# Loan Default Prediction and Expected Loss Calculation

This project aims to predict the probability of default (PD) for loan borrowers and calculate the expected loss on a loan using machine learning models. The dataset contains information about borrowers, including their income, total loans outstanding, and other metrics. The goal is to build a model that can predict the probability of default and use it to estimate the expected loss on a loan, assuming a recovery rate of 10%.

## Project Overview

The project involves the following steps:
1. **Data Preprocessing**: Cleaning and preparing the data for modeling.
2. **Model Selection**: Using Logistic Regression and XGBoost to predict the probability of default.
3. **Model Training**: Training the models on the provided dataset.
4. **Probability of Default (PD) Prediction**: Predicting the probability of default for new loan data.
5. **Expected Loss Calculation**: Calculating the expected loss using the predicted PD and a recovery rate of 10%.

## Installation

To run this project, you need to have Python installed along with the following libraries:

```bash
pip install pandas scikit-learn xgboost

## Run script

To run this project use this command:

```bash
python loan_default_prediction.py