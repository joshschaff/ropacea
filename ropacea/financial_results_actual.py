import yfinance as yf
import pandas as pd
from datetime import datetime

# Define the list of ticker symbols
ticker_symbols = [
    'AAPL', 'ABT', 'ADBE', 'AMGN', 'BAC', 'CAT', 'COP', 'CSCO', 'CVX', 'DHR',
    'DIS', 'INTC', 'JNJ', 'JPM', 'KO', 'LLY', 'MA', 'MCD', 'MRK', 'MSFT',
    'NVDA', 'ORCL', 'PEP', 'PFE', 'PG', 'TXN', 'VZ', 'WFC', 'WMT', 'XOM'
]

# Define the date range for the past 10 years
end_date = datetime.now()
start_date = end_date.replace(year=end_date.year - 10)

# Fetch historical data for each stock
historical_data = yf.download(ticker_symbols, start=start_date, end=end_date)['Adj Close']

# Calculate annual returns
annual_returns = historical_data.resample('Y').ffill().pct_change()

# Display the annual returns
print(annual_returns)

# Calculate the average of annual returns for all stocks
average_returns_all = annual_returns.mean(axis=1)

# Calculate the average of annual returns for each stock
average_returns_individual = annual_returns.mean()

# Display the results
print("Average Annual Returns for All Stocks:")
print(average_returns_all)

print("\nAverage Annual Returns for Each Stock:")
print(average_returns_individual)