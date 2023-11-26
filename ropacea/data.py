"""Utility functions to read data provided by Dr. Ma.

Also defines the universe of tickers we are using for the rest of analysis.
    >>> from ropacea.data import UNIVERSE
"""


import os
import pandas as pd
from pathlib import Path
from functools import cache

from datetime import date
from dateutil.relativedelta import relativedelta

# change working directory to be the ropacea/ module folder
os.chdir(os.path.dirname(__file__))

DATA_DIR = Path('../data')

UNIVERSE= [
    'AAPL',
    'ABT',
    'ADBE',
    'AMGN',
    'BAC',
    'CAT',
    'COP',
    'CSCO',
    'CVX',
    'DHR',
    'DIS',
    'INTC',
    'JNJ',
    'JPM',
    'KO',
    'LLY',
    'MA',
    'MCD',
    'MRK',
    'MSFT',
    'NVDA',
    'ORCL',
    'PEP',
    'PFE',
    'PG',
    'TXN',
    'VZ',
    'WFC',
    'WMT',
    'XOM'
]

@cache
def read_monthly_return_capitalization() -> pd.DataFrame:
    """
    Returns monthly-return-capitalization filtered to the stock universe.

    Also drops duplicate values
    """
    #mrc = pd.read_excel(DATA_DIR / 'monthly-return-capitalization.xlsx')
    mrc = pd.read_csv(DATA_DIR / 'monthly-return-capitalization.csv', parse_dates=[3])
    #parse_dates=[4]) # parse the 'Monthly Calendar Date' col as date
    mrc = mrc[mrc['Ticker'].isin(UNIVERSE)]

    # drop duplicate values, keep the first
    mrc = mrc.drop_duplicates(subset=['Ticker', 'Monthly Calendar Date'], keep='first')

    return mrc


def subset_monthly_return_capitalization(start_date: date, end_date: date):
    """ Obtain a subset of monthly return capitalization from start_date (inclusive) to end_date (exclusive)
    Dates are rounded down to the start of the month.
    """
    start_date = start_date.replace(day=1)
    end_date = end_date.replace(day=1)

    # fetch all monthly return capitalizations
    mrc = read_monthly_return_capitalization()

    # filter
    mrc = mrc[mrc['Monthly Calendar Date'] < pd.to_datetime(end_date)]
    mrc = mrc[mrc['Monthly Calendar Date'] >= pd.to_datetime(start_date)]
    
    return mrc



def get_in_sample_data(mark_date: date, sample_months: int = 60) ->  pd.DataFrame:
    """
    Return monthly-return-capitalization filtered to include only those date within sample_months 
    back in time of the given mark_date.
    
    Parameters:
        mark_date: fetch historical data looking back in time from this date
        sample_month: the number of months back in time to fetch historical data

    Sample usage:
        >>> mark_date = date(year = 2017, month=1, day=1)
        >>> sample_months = 60
        >>> sample_data = get_in_sample_data(mark_date, sample_months)
    """

    # filter to after start of sample period
    start_date = mark_date - relativedelta(months=sample_months)

    # fetch all monthly return capitalizations
    mrc = subset_monthly_return_capitalization(start_date, mark_date)

    # validate data
    ticker_counts = mrc.groupby('Ticker')['Monthly Calendar Date'].count()
    for ticker in UNIVERSE:
        count = ticker_counts.get(ticker,0)
        if count != sample_months:
            print(f"WARNING: Only {count:2d} out of {sample_months} values found in sample " + 
                  f"for {ticker:4} at {mark_date}")

    return mrc


def get_returns(start_date, end_date):
    """Get the return rate for each ticker in UNIVERSE over the given period.

    Arguments:
        state_date: inclusive
        end_date: exclusive
    """
    out_of_sample_data = subset_monthly_return_capitalization(start_date, end_date)

    # series with Tickers as indices and total returns as values
    returns = out_of_sample_data.groupby('Ticker')['Monthly Total Return'].prod()
    # order by UNIVERSE
    returns = [returns.get(ticker, 0.0) for ticker in UNIVERSE]

    return returns


# test functionality
if __name__ == '__main__':
    mark_date = date(year = 2017, month=1, day=1)
    sample_months = 60
    out = get_in_sample_data(mark_date, sample_months)

    print(out)