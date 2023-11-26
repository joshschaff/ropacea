#sample covariance matrix with shrinkage
from datetime import date
import data
import numpy as np
import pandas as pd

mark_date = date(year = 2017, month=1, day=1)
sample_months = 60
data = get_in_sample_data(mark_date, sample_months)

#sample covariance matrix
cov = np.cov(data)

# Number of assets (variables)
n_assets = cov.shape[0]

# Calculate the average of the diagonal elements of the sample covariance matrix
trace_cov = np.trace(cov) / n_assets

# Calculate the Ledoit-Wolf shrinkage target: diagonal matrix with average covariance on the diagonal
target_cov_matrix = np.full_like(cov, trace_cov)
np.fill_diagonal(target_cov_matrix, np.diag(cov))

# Estimate the optimal shrinkage coefficient (Ledoit-Wolf method)
delta = np.mean(np.diag(cov - target_cov_matrix))
gamma = np.linalg.norm(cov - target_cov_matrix, ord='fro') ** 2
n_obs = data.shape[0]  #number of observations in the data set

alpha = max(0, (gamma - n_assets) / (delta * n_obs))

# Calculate the shrunken covariance matrix
shrunken_cov_matrix = alpha * target_cov_matrix + (1 - alpha) * cov

print("Shrunken Covariance Matrix:")
print(shrunken_cov_matrix)