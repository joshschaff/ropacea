from dataclasses import dataclass
from datetime import date
from dateutil.relativedelta import relativedelta

from ropacea.portfolios import Portfolio, PortfolioStrategy, calculate_portfolio
from ropacea.data import get_returns

@dataclass
class BacktestResult():
    mark_date: date
    portfolio: Portfolio
    returns: list[float]


def backtest(mark_date: date,
             strategy: PortfolioStrategy,
             frequency: relativedelta) -> BacktestResult:

    portfolio = calculate_portfolio(mark_date, strategy)
    returns = get_returns(mark_date, mark_date+frequency)

    portfolio_return = portfolio.portfolio_return(returns)
    print(f"{portfolio_return = }")

    return BacktestResult(
        mark_date,
        portfolio,
        returns
    )


def backtest_loop(start_date: date, 
                  end_date: date, 
                  strategy: PortfolioStrategy,
                  frequency = relativedelta(months=1)) -> list[BacktestResult]:

    mark_date = start_date
    backtest_results = []

    total_return = 1.00

    while (mark_date < end_date):
        print(f"{mark_date = }")
        backtest_result = backtest(mark_date, strategy, frequency)
        backtest_results.append(backtest_result)
        total_return *= (1+backtest_result.portfolio.portfolio_return(backtest_result.returns) )

        mark_date = mark_date + frequency


    print(f"{total_return = }")

    return backtest_results



if __name__ == '__main__':
    out = backtest_loop(
        start_date = date(year = 2017, month=1, day=1),
        end_date = date(2023, month=1, day=1),
        strategy=PortfolioStrategy.CONSTANT_CORRELATION
    )