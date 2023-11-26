# Single factor
mark_date = date(year = 2017, month=1, day=1)
sample_months = 60
data = get_in_sample_data(mark_date, sample_months)

'''Create unique dates to numbers'''

# Creating a mapping of unique dates to numbers
date_to_number = {date: i + 1 for i, date in enumerate(data['Monthly Calendar Date'].unique())}

# Assigning numbers based on the mapping
data['Month'] = data['Monthly Calendar Date'].map(date_to_number)

### Find rM for each month and overall std
# Grouping by 'Month' and calculating the mean of each month
mkt = data.groupby('Month')['Monthly Total Return'].mean().reset_index()

# Renaming the columns for clarity
mkt.columns = ['Month', 'rM']

# Displaying the resulting DataFrame
print(mkt)

#Find std of market
stdM = data['Monthly Total Return'].std()

# Displaying the resulting DataFrame
print(stdM)

# Merging the two DataFrames based on the 'Number' column
data = pd.merge(data, mkt, on='Month', how='left')

import statsmodels.api as sm

# Creating an empty DataFrame to store regression results
regression_results = pd.DataFrame(columns=['Ticker', 'Alpha', 'Beta'])

# Grouping by 'Group' column
grouped = data.groupby('Ticker')

# Performing linear regression within each group
for group, group_df in grouped:
    # Adding a constant term for the intercept (alpha)
    X = sm.add_constant(group_df['rM'])
    y = group_df['Monthly Total Return']

    # Performing linear regression
    model = sm.OLS(y, X).fit()

    # Extracting coefficients
    alpha = model.params['const']
    beta = model.params['rM']

    # Appending results to the DataFrame
    regression_results = regression_results.append({
        'Ticker': group,
        'Alpha': alpha,
        'Beta': beta,
    }, ignore_index=True)

# Displaying the results
print(regression_results)

import numpy as np

# Extracting the column as a NumPy array
B = regression_results['Beta'].to_numpy()
column_theta = regression_results['Theta'].to_numpy()

# Creating a diagonal matrix from theta
D = np.diag(column_theta)

# Displaying the resulting diagonal matrix

V = stdM**2 * np.dot(B, B.T) + D
print(V)
