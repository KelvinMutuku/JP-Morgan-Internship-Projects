# FICO Score Bucketization for Mortgage Default Prediction

This project provides a method to bucketize FICO scores into discrete ratings, where a lower rating signifies a better credit score. The bucketization process optimizes either **Mean Squared Error (MSE)** or **Log-Likelihood (LL)** to determine the optimal boundaries. The solution uses dynamic programming for efficient optimization.

## Features

- **Two Optimization Methods**:
  - **Mean Squared Error (MSE)**: Minimizes the approximation error between FICO scores and bucket representatives.
  - **Log-Likelihood (LL)**: Maximizes the likelihood of observed default rates given the bucket boundaries.
- **Dynamic Programming**: Efficiently solves the optimization problem by breaking it into subproblems.
- **Rating Map**: Assigns lower ratings to higher FICO scores (e.g., Rating 1 = Best creditworthiness).

## Files

- `fico_bucketization.py`: Contains the `FICOBucketizer` class for bucketizing FICO scores.
- `requirements.txt`: Lists the required Python packages.

## Installation

1. Install dependencies::
   ```bash
   pip install -r requirements.txt
2. Run the project:
   ```bash
   python fico_bucketization.py