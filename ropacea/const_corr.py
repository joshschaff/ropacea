from datetime import date
import data
import numpy as np
import pandas as pd

mark_date = date(year = 2017, month=1, day=1)
sample_months = 60

data_copy = data.get_in_sample_data(mark_date, sample_months)

print(data_copy)


# Estimation of Individual Asset Volatilities
sigma = data_copy.groupby('Ticker')['Monthly Total Return'].std()
print("sigma")
print(sigma)

# Estimation of Pairwise Correlations

# Pivot the DataFrame to get 'Monthly Total Return' for each 'Ticker' in columns
pivot_data = data_copy.pivot(index='Monthly Calendar Date', columns='Ticker', values='Monthly Total Return')

# Calculate the correlation matrix
rho = pivot_data.corr()
print(rho)

 # Construct Covariance Matrix using Constant Correlation Model
V = rho.values * np.dot(sigma.values, sigma.values.T) + (1 - rho.values) * np.diag(sigma.values)**2
V_df = pd.DataFrame(V, index=rho.index, columns=rho.columns)

print("Constant Correlation Covariance Matrix:")
print(V_df)

import openpyxl

excel_file_path = '/Users/kathrynjarjoura/Desktop/V_cc.xlsx'

# Export the DataFrame to Excel
V_df.to_excel(excel_file_path, index=True)