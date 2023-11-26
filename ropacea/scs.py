#sample covariance matrix with shrinkage
from datetime import date
import data
import numpy as np
import pandas as pd

def scs(data):

    # Pivot the data to create a DataFrame suitable for covariance calculation
    pivot_data = data.pivot_table(values='Monthly Total Return', 
                                    index='Monthly Calendar Date', 
                                    columns='Ticker')

    # Calculate the sample covariance matrix
    sample_cov_matrix = pivot_data.cov()

    # Number of assets (variables)
    n_assets = sample_cov_matrix.shape[0]

    # Calculate the average of the diagonal elements of the sample covariance matrix
    trace_cov = np.trace(sample_cov_matrix) / n_assets

    # Calculate the Ledoit-Wolf shrinkage target: diagonal matrix with average covariance on the diagonal
    target_cov_matrix = np.full_like(sample_cov_matrix, trace_cov)
    np.fill_diagonal(target_cov_matrix, np.diag(sample_cov_matrix))

    # Estimate the optimal shrinkage coefficient (Ledoit-Wolf method)
    delta = np.mean(np.diag(sample_cov_matrix - target_cov_matrix))
    gamma = np.linalg.norm(sample_cov_matrix - target_cov_matrix, ord='fro') ** 2
    n_obs = data['Monthly Calendar Date'].nunique()  # Number of unique dates (observations)

    alpha = max(0, (gamma - n_assets) / (delta * n_obs))

    # Calculate the shrunken covariance matrix
    shrunken_cov_matrix = alpha * target_cov_matrix + (1 - alpha) * sample_cov_matrix

    # print("Shrunken Covariance Matrix:")
    # print(shrunken_cov_matrix.values)

    return shrunken_cov_matrix.values