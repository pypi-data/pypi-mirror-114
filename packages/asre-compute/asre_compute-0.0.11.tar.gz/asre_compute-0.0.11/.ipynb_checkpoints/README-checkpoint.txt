From a pandas dataframe, this program computes the Absolute Rule Effect (ARE) or cognitive biais Absolute Stochastic Rule Effect (ASRE) through A-learning and provides asymptotic 95% confidence intervals from M-estimation sandwich formula.

asre-package takes as arguments

- df: pandas dataframe with no missing values.
- rule: column name for the rule as a string (random variable must be Bernoulli). 
- ttt: column name for the experimental treatment as a string (random variable must be Bernoulli). 
- y: column name for the outcome as a string (random variable can be either binary or continuous). 
- ps_predictors: list of column names (strings) for variables causing experimental treatment initiation e.g.propensity score predictors (random variables can be either binary or continuous). 
- pronostic_predictors: list of column names (strings) for variables causing the outcome e.g. prognosis predictors (random variables can be either binary or continuous). 
- ctst_vrb: list of column names (strings) for variables acting as treatment effect modifiers e.g. contrast variables (random variables can be either binary or continuous). 
- est = 'ARE': takes value 'ARE' or 'ASRE_cb'. When 'ARE' is passed, the program computes only the Absolute Rule Effect ; when 'ASRE_cb' is passed it computes the ARE and alpha-level cognitive biais ASRE with alpha provided below.
- alpha = .5: alpha-level cognitive biais for ASRE used when est = 'ASRE_cb'.
- n_alphas = 5: number of linearly spaced alphas computed on the plot wehn est='ASRE_cb'.
- precision = 3: rounding of the printed ARE/ASRE and their 95% confidence intervals.

          
Implementation detail will be posted on https://github.com/fcgrolleau/Emulated-ITR
Theoretical argument including extensive simulations will be posted on Arxiv soon.