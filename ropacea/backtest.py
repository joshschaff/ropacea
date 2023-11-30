from dataclasses import dataclass
from datetime import date
from dateutil.relativedelta import relativedelta
import statistics
import math

from ropacea.portfolios import Portfolio, PortfolioStrategy, calculate_portfolio
from ropacea.data import get_market_returns, get_risk_free_rate


BASIS_POINT = 0.0001

@dataclass
class BacktestResult():
    mark_date: date
    portfolio: Portfolio
    market_returns: list[float]
    excess_return: float


@dataclass 
class BacktestSummary():
    monthly_returns_bp_mean: float
    monthly_returns_bp_std: float
    annualized_mean_pct: float
    annualized_std_pct: float
    sharpe_ratio: float


def backtest(mark_date: date,
             strategy: PortfolioStrategy,
             frequency: relativedelta,
             min_return_ratio: float) -> BacktestResult:

    portfolio = calculate_portfolio(mark_date, strategy, min_return_ratio)
    market_returns = get_market_returns(mark_date, mark_date+frequency)

    monthly_portfolio_return = portfolio.calc_portfolio_return(market_returns)
    print(f"{monthly_portfolio_return = :.4f}")

    risk_free_return = get_risk_free_rate(mark_date)
    print(f"{risk_free_return = :.4f}")

    excess_return = monthly_portfolio_return - risk_free_return

    return BacktestResult(
        mark_date,
        portfolio,
        market_returns,
        excess_return,
    )


def backtest_loop(start_date: date, 
                  end_date: date, 
                  strategy: PortfolioStrategy,
                  frequency = relativedelta(months=1),
                  min_return_ratio: float =1) -> list[BacktestResult]:

    mark_date = start_date
    backtest_results = []

    while (mark_date < end_date):
        print(f"{mark_date = }")
        backtest_result = backtest(mark_date, strategy, frequency, min_return_ratio)
        backtest_results.append(backtest_result)

        mark_date = mark_date + frequency

    return backtest_results


def summarize_results(backtest_results: list[BacktestResult]) -> BacktestSummary:

    print(f"{'='*10} SUMMARY {'='*10}")

    # monhtly returns (bp)
    monthly_returns_bp_mean = statistics.mean([
      br.excess_return/BASIS_POINT for br in backtest_results  
    ])

    monthly_returns_bp_std = statistics.stdev([
      br.excess_return/BASIS_POINT for br in backtest_results  
    ])

    print(f"{monthly_returns_bp_mean = :>.2f}")
    print(f"{monthly_returns_bp_std = :>.2f}")

    # annualized mean
    annualized_mean_pct = (
        (1+ monthly_returns_bp_mean * BASIS_POINT) ** 12 - 1
    ) * 100
    # annualized STD
    annualized_std_pct = (
        (monthly_returns_bp_std * BASIS_POINT) * math.sqrt(12)
    ) * 100

    print(f"{annualized_mean_pct = :>.2f}")
    print(f"{annualized_std_pct = :>.2f}")

    sharpe_ratio = annualized_mean_pct / annualized_std_pct

    print(f"{sharpe_ratio = :>.2f}")

    out =  BacktestSummary(
        monthly_returns_bp_mean,
        monthly_returns_bp_std,
        annualized_mean_pct,
        annualized_std_pct,
        sharpe_ratio
    )

    return out




if __name__ == '__main__':
    results = backtest_loop(
        start_date = date(year = 2017, month=1, day=1),
        end_date = date(2023, month=1, day=1),
        strategy=PortfolioStrategy.EQUALLY_WEIGHTED,
        min_return_ratio=1.75
    )

    summarize_results(results)

