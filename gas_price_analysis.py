import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# Load the data
data = pd.read_csv("Nat_Gas.csv")

# Convert the 'Dates' column to datetime format
data['Dates'] = pd.to_datetime(data['Dates'])

# Sort the data by date
data = data.sort_values(by='Dates')

# Plot the historical data
plt.figure(figsize=(12, 6))
plt.plot(data['Dates'], data['Prices'], marker='o', linestyle='-', color='b')
plt.title('Natural Gas Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.show()

# Prepare data for regression
X = np.arange(len(data)).reshape(-1, 1)  # Time steps as features
y = data['Prices'].values  # Prices as target

# Fit a linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict for the next 12 months
future_steps = 12
X_future = np.arange(len(data), len(data) + future_steps).reshape(-1, 1)
y_future = model.predict(X_future)

# Create future dates
last_date = data['Dates'].iloc[-1]
future_dates = [last_date + timedelta(days=30 * i) for i in range(1, future_steps + 1)]

# Combine historical and future data
future_data = pd.DataFrame({'Dates': future_dates, 'Prices': y_future})
extended_data = pd.concat([data, future_data], ignore_index=True)

# Plot the extended data
plt.figure(figsize=(12, 6))
plt.plot(extended_data['Dates'], extended_data['Prices'], marker='o', linestyle='-', color='b', label='Historical Data')
plt.plot(future_data['Dates'], future_data['Prices'], marker='o', linestyle='--', color='r', label='Extrapolated Data')
plt.title('Natural Gas Prices: Historical and Extrapolated')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()

# Function to estimate price for a given date
def estimate_price(date):
    # Convert input date to datetime
    date = pd.to_datetime(date)
    
    # Check if the date is within the historical data range
    if date <= data['Dates'].iloc[-1]:
        # Find the closest historical date
        closest_date = data.iloc[(data['Dates'] - date).abs().idxmin()]
        return closest_date['Prices']
    else:
        # Calculate the number of months beyond the last date
        months_diff = (date.year - last_date.year) * 12 + (date.month - last_date.month)
        if months_diff <= future_steps:
            return future_data.iloc[months_diff - 1]['Prices']
        else:
            return "Date is beyond the extrapolation range."

# Example usage
print(estimate_price('2024-12-31'))  # Extrapolated date
print(estimate_price('2023-07-31'))  # Historical date

# Analyze seasonal trends
data['Month'] = data['Dates'].dt.month
monthly_avg = data.groupby('Month')['Prices'].mean()

# Plot seasonal trends
plt.figure(figsize=(10, 5))
monthly_avg.plot(kind='bar', color='skyblue')
plt.title('Average Natural Gas Prices by Month')
plt.xlabel('Month')
plt.ylabel('Average Price')
plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.grid(True)
plt.show()