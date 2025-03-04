import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, accuracy_score

# Load the data
data = pd.read_csv('Task_3_and_4_Loan_Data.csv')

# Separate features and target variable
X = data.drop(columns=['default', 'customer_id'])
y = data['default']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize models
log_reg = LogisticRegression(random_state=42)
xgb_clf = XGBClassifier(random_state=42)

# Train Logistic Regression model
log_reg.fit(X_train, y_train)

# Train XGBoost model
xgb_clf.fit(X_train, y_train)

# Evaluate models
y_pred_log_reg = log_reg.predict_proba(X_test)[:, 1]
y_pred_xgb = xgb_clf.predict_proba(X_test)[:, 1]

print("Logistic Regression ROC-AUC:", roc_auc_score(y_test, y_pred_log_reg))
print("XGBoost ROC-AUC:", roc_auc_score(y_test, y_pred_xgb))

print("Logistic Regression Accuracy:", accuracy_score(y_test, log_reg.predict(X_test)))
print("XGBoost Accuracy:", accuracy_score(y_test, xgb_clf.predict(X_test)))

# Function to predict probability of default
def predict_pd(model, loan_data):
    loan_data_scaled = scaler.transform(loan_data)
    pd = model.predict_proba(loan_data_scaled)[:, 1]
    return pd

# Function to calculate expected loss
def calculate_expected_loss(pd, loan_amount, recovery_rate=0.1):
    return pd * (1 - recovery_rate) * loan_amount

# Example usage
loan_data = pd.DataFrame({
    'credit_lines_outstanding': [2],
    'loan_amt_outstanding': [5000],
    'total_debt_outstanding': [10000],
    'income': [60000],
    'years_employed': [5],
    'fico_score': [700]
})

pd_log_reg = predict_pd(log_reg, loan_data)
pd_xgb = predict_pd(xgb_clf, loan_data)

loan_amount = 10000
expected_loss_log_reg = calculate_expected_loss(pd_log_reg, loan_amount)
expected_loss_xgb = calculate_expected_loss(pd_xgb, loan_amount)

print("Expected Loss (Logistic Regression):", expected_loss_log_reg)
print("Expected Loss (XGBoost):", expected_loss_xgb)