import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.optimize import minimize

def quantize_fico_mse(fico_scores, n_buckets):
    """Quantizes FICO scores into buckets using KMeans to minimize MSE."""
    fico_scores = np.array(fico_scores).reshape(-1, 1)
    kmeans = KMeans(n_clusters=n_buckets, random_state=42, n_init=10)
    kmeans.fit(fico_scores)
    buckets = np.sort(kmeans.cluster_centers_.flatten())
    return buckets

def log_likelihood(buckets, fico_scores, defaults):
    """Computes the log-likelihood function given bucket boundaries."""
    buckets = np.sort(buckets)
    buckets = np.insert(buckets, 0, min(fico_scores))
    buckets = np.append(buckets, max(fico_scores))
    
    total_ll = 0
    for i in range(len(buckets) - 1):
        mask = (fico_scores >= buckets[i]) & (fico_scores < buckets[i+1])
        ni = np.sum(mask)
        ki = np.sum(defaults[mask])
        if ni == 0:
            continue
        pi = ki / ni if ni > 0 else 0
        if pi in [0, 1]:
            continue
        total_ll += ki * np.log(pi) + (ni - ki) * np.log(1 - pi)
    
    return -total_ll  # Minimizing negative log-likelihood

def quantize_fico_ll(fico_scores, defaults, n_buckets):
    """Finds optimal FICO score buckets by maximizing log-likelihood."""
    initial_buckets = np.linspace(min(fico_scores), max(fico_scores), n_buckets + 1)[1:-1]
    result = minimize(log_likelihood, initial_buckets, args=(fico_scores, defaults), method='Powell')
    return np.sort(result.x)

# Load dataset
df = pd.read_csv("Task 3 and 4_Loan_Data.csv")
fico_scores = df['fico_score'].values
defaults = df['default'].values

# Set number of buckets
n_buckets = 5

# Get bucket boundaries using MSE
mse_buckets = quantize_fico_mse(fico_scores, n_buckets)
print("MSE Optimized Buckets:", mse_buckets)

# Get bucket boundaries using Log-Likelihood
ll_buckets = quantize_fico_ll(fico_scores, defaults, n_buckets)
print("Log-Likelihood Optimized Buckets:", ll_buckets)