# ropacea
Risk-Optimized Portfolios: An Analysis of Covariance Estimation Approaches


## How to Install
```pip install -e .```


# Development
Put new python files inside the `ropacea/` directory

Append any new Python package dependencies to the `dependencies` list in `pyproject.toml`


Hello this is a new change!



## structure

 - whenever we are running our model is the mark_dt 
 - We will have one piece of code that subsets the historical data before the mark_dt
    - this will bea a subset of the market_return.xlsx
 - this subset, likely as a pandas dataframe, will be the input to each of our 3 covariance estimation methods