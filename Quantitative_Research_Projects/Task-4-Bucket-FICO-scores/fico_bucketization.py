import numpy as np
import pandas as pd

class FICOBucketizer:
    def __init__(self, n_buckets=5, method='mse', epsilon=1e-9):
        self.n_buckets = n_buckets
        self.method = method  # 'mse' or 'log_likelihood'
        self.epsilon = epsilon  # to avoid log(0)
        self.bucket_boundaries = None
        self.rating_map = None

    def fit(self, fico_scores, defaults):
        """
        Fit the bucketizer to the data.
        :param fico_scores: List or array of FICO scores.
        :param defaults: List or array of default indicators (1=default, 0=no default).
        """
        data = pd.DataFrame({'fico': fico_scores, 'default': defaults})
        data = data.sort_values('fico').reset_index(drop=True)
        n = len(data)
        
        # Precompute prefix sums for efficient interval calculations
        prefix_fico = np.zeros(n + 1)
        prefix_default = np.zeros(n + 1)
        for i in range(n):
            prefix_fico[i+1] = prefix_fico[i] + data['fico'][i]
            prefix_default[i+1] = prefix_default[i] + data['default'][i]
        
        # Precompute cost matrix for all intervals [i, j)
        cost = np.full((n+1, n+1), np.inf)
        for i in range(n):
            for j in range(i+1, n+1):
                total = j - i
                if total == 0:
                    continue
                sum_fico = prefix_fico[j] - prefix_fico[i]
                sum_default = prefix_default[j] - prefix_default[i]
                
                if self.method == 'mse':
                    mean = sum_fico / total
                    sum_sq_err = sum((data['fico'][k] - mean)**2 for k in range(i, j))
                    cost[i][j] = sum_sq_err
                elif self.method == 'log_likelihood':
                    p = (sum_default + self.epsilon) / (total + 2*self.epsilon)  # Laplace smoothing
                    if p <= 0 or p >= 1:
                        cost[i][j] = -np.inf
                    else:
                        ll = sum_default * np.log(p) + (total - sum_default) * np.log(1 - p)
                        cost[i][j] = -ll  # Convert to minimization problem
        
        # Dynamic programming to find optimal splits
        dp = np.full((n+1, self.n_buckets + 1), np.inf)
        dp[0][0] = 0
        split_points = np.zeros((n+1, self.n_buckets + 1), dtype=int)
        
        for k in range(1, self.n_buckets + 1):
            for j in range(1, n+1):
                for i in range(j):
                    if dp[i][k-1] + cost[i][j] < dp[j][k]:
                        dp[j][k] = dp[i][k-1] + cost[i][j]
                        split_points[j][k] = i
        
        # Backtrack to find boundaries
        boundaries = []
        j = n
        for k in range(self.n_buckets, 0, -1):
            i = split_points[j][k]
            boundaries.append(data['fico'][i])
            j = i
        boundaries.append(data['fico'].min())  # Add minimum FICO as lower bound
        boundaries = sorted(list(set(boundaries)))
        
        self.bucket_boundaries = boundaries
        self._assign_ratings()
    
    def _assign_ratings(self):
        """Assign ratings such that lower rating = better credit score."""
        sorted_boundaries = sorted(self.bucket_boundaries, reverse=True)
        self.rating_map = {}
        for i in range(len(sorted_boundaries)-1):
            lower = sorted_boundaries[i+1]
            upper = sorted_boundaries[i]
            self.rating_map[f"{lower}-{upper}"] = i + 1  # Rating starts at 1
    
    def transform(self, fico_scores):
        """Map FICO scores to ratings."""
        ratings = []
        sorted_boundaries = sorted(self.bucket_boundaries, reverse=True)
        for score in fico_scores:
            for i in range(len(sorted_boundaries)-1):
                if sorted_boundaries[i+1] <= score <= sorted_boundaries[i]:
                    ratings.append(i + 1)
                    break
            else:
                ratings.append(len(sorted_boundaries))  # Assign to last bucket
        return ratings

# Example Usage
if __name__ == "__main__":
    # Sample Data
    np.random.seed(42)
    fico_scores = np.random.randint(300, 850, 1000)
    defaults = np.random.binomial(1, 0.1, 1000)  # 10% default rate

    # Initialize bucketizer with MSE
    bucketizer_mse = FICOBucketizer(n_buckets=5, method='mse')
    bucketizer_mse.fit(fico_scores, defaults)
    print("MSE Bucket Boundaries:", bucketizer_mse.bucket_boundaries)
    print("Rating Map:", bucketizer_mse.rating_map)

    # Initialize bucketizer with Log-Likelihood
    bucketizer_ll = FICOBucketizer(n_buckets=5, method='log_likelihood')
    bucketizer_ll.fit(fico_scores, defaults)
    print("Log-Likelihood Bucket Boundaries:", bucketizer_ll.bucket_boundaries)
    print("Rating Map:", bucketizer_ll.rating_map)