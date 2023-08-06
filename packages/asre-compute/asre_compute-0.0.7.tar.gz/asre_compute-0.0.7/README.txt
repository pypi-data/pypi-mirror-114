From a pandas dataframe, this program computes the Absolute Rule Effect or cognitive biais Absolute Stochastic Rule Effect through A-learning and provides asymptotic 95% confidence intervals from M-estimation sandwich formula.

asre_package takes as arguments

- df: pandas dataframe
- rule: column name for the rule as a string (random variable must be Bernoulli) 
- ttt: column name for the experimental treatment as a string (random variable must be Bernoulli) 
- y: column name for the outcome as a string (random variable can be either binary or continuous) 
- ps_predictors: list of column names (strings) for variables causing experimental treatment initiation e.g.propensity score predictors (random variables can be either binary or continuous) 
- pronostic_predictors: list of column names (strings) for variables causing the outcome e.g. prognosis predictors (random variables can be either binary or continuous) 
- ctst_vrb: list of column names (strings) for variables acting as treatment effect modifiers e.g. contrast variables (random variables can be either binary or continuous) 
- est='ARE': takes value 'ARE' computes only the Absolute Rule Effect or 'ASRE_cb' then the program computes ARE and cognitive biais ASRE with alpha value provided below 
- alpha = .5: cognitive bias value for ASRE, if est="ASRE_cb'
- n_alphas=5: number of alphas computed on the plot, if est="ASRE_cb'
- precision=3: rounding of the printed ARE/ASRE and their 95% confidence intervals.