""" Contains all 5 different portfolio strategies.

To calculate a portfolio, call calculate_portfolio() with a mark_date and strategy:
    >>> from datetime import date
    >>> from ropacea.portfolios import PortfolioStrategy, calculate_portfolio()
    >>> mark_date = date(2022, 11, 17)
    >>> strategy = PortfolioStrategy.SINGLE_FACTOR
    >>> my_portfolio = calculate_portfolio(mark_date, strategy)

"""


from datetime import date
from enum import Enum

import gurobipy as gp
from gurobipy import GRB
import numpy as np

from ropacea.data import UNIVERSE, get_in_sample_data


class Portfolio:
    holdings: list

    def __init__(self, holdings) -> None:
        assert len(holdings) == UNIVERSE
        self.holdings = holdings

    def total_return(self, returns) -> float:
        """Value the portfolio at a given set of returns"""
        return sum([r*h for r,h in zip(returns, self.holdings)])


class PortfolioStrategy(Enum):
    # two benchmark strategies
    VALUE_WEGHTED = 0
    EQUALLY_WEIGHTED = 1
    # three min risk strategies
    SINGLE_FACTOR = 2
    CONSTANT_CORRELATION = 3
    SAMPLE_COVARIANCE = 4


def calculate_portfolio(mark_date: date, strategy: PortfolioStrategy) -> Portfolio:
    portfolio = None

    match strategy:
        case PortfolioStrategy.VALUE_WEGHTED:
            portfolio = value_weighted_portfolio(mark_date)
        case PortfolioStrategy.EQUALLY_WEIGHTED:
            portfolio = equally_weighted_portfolio()
        case PortfolioStrategy.CONSTANT_CORRELATION | \
             PortfolioStrategy.SINGLE_FACTOR | \
             PortfolioStrategy.SAMPLE_COVARIANCE:
            portfolio = min_risk_portfolio(mark_date, strategy)
        case _:
            raise ValueError("Invald PortfolioStrategy specified")

    return portfolio


def value_weighted_portfolio(mark_date) -> Portfolio:
    # TODO
    pass

def equally_weighted_portfolio() -> Portfolio:
    N = len(UNIVERSE)
    holdings = [1/N] * N
    return Portfolio(holdings)


def _min_risk_model(expected_returns: np.ndarray,
                    covariance: np.ndarray,
                    min_return: float):
    
    model = gp.Model()

    # check input shape
    n_assets = len(expected_returns)
    if covariance.shape != (n_assets, n_assets):
        raise ValueError(f"{covariance.shape = } incompatible with {expected_returns.shape = }")

    # allocation vairables
    holdings = model.addMVar(
        shape = n_assets,
        lb = 0.0, # long only
        ub = float('inf'),
        name = 'holdings'
    )

    # set objective to minimize risk
    model.setObjective(holdings @ covariance @ holdings, GRB.MINIMZE)

    # fully invested constraint
    model.addConstr(sum([x for x in holdings]) == 1)

    # minimum return constraint
    model.addCosntr(expected_returns.T @ holdings >= min_return)

    model.optimize()

    return holdings.X


def min_risk_portfolio(mark_date: date, 
                       strategy: PortfolioStrategy) -> Portfolio:
    """Calculate a portfolio using the min risk model and 
    one of the three covariance estimation strategies"""

    data = get_in_sample_data(mark_date)

    # get average returns for each ticker
    expected_returns = data.groupby('Ticker')['Monthly Total Return'].mean()
    # convert from pandas series to numpy array
    expected_returns = np.array(
        expected_returns[ticker] for ticker in UNIVERSE
    )

    covariance = None
    match strategy:
        case PortfolioStrategy.SINGLE_FACTOR:
            # TODO: calculate covariance matrix for single factor
            pass
        case PortfolioStrategy.CONSTANT_CORRELATION:
            # TODO: calculate covariance matrix for constant correlation
            pass
        case PortfolioStrategy.SAMPLE_COVARIANCE:
            # TODO: calculate covariance matrix using sample covariance
            pass

    # TODO: find a way to get min return or switch min risk model to use gamma instead
    min_return = 0
    holdings = _min_risk_model(expected_returns, covariance, min_return)

    return Portfolio(holdings)

    

