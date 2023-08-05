import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt

def A_learning(df, ctst_vrb, ps, nu, ttt, y):
    
    """A-learning algorithm
    Takes as input 
        df: pandas dataframe
        ctst_vrb: list of column names for contrast model fit
        ps: single column name of the predicted propensity scores
        nu: single column name of the predicted prognosis under treatment option 0
        ttt: single column name of the treatment option=1 (binary coding required 0/1)
        y: single column name of the outcome
        
    Contrast function is linear in the coefficients. Solution has linear algebra implementation.
    Output is a tuple of the contrast function coefficients and the in-sample CATE prediction"""
    
    H = df[ctst_vrb]
    H.insert(0, 'H_0', np.repeat(1, len(H)) )
    
    A = np.empty((len(ctst_vrb)+1, len(ctst_vrb)+1))
    for i in range(len(A)):
        for j in range(len(A)):
            A[i,j] =  np.sum(H.iloc[:,j] * H.iloc[:,i] * (df[ttt] - df[ps]) * df[ttt] )
    try:
        A_inverse = np.linalg.inv(A)
    except np.linalg.LinAlgError:
        A_inverse = float("nan")
        print('Singular matrix, Nan output.')
    C = np.empty((len(ctst_vrb)+1,1))
    
    for i in range(len(C)):
        C[i] = np.sum(H.iloc[:,i] * (df[ttt] - df[ps]) * (df[y] - df[nu])) 
        
    psi_hat = np.dot(A_inverse, C)
    cate_hat = np.dot(H, psi_hat)
    return psi_hat, cate_hat

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_deriv(x):
    return sigmoid(x)*(1-sigmoid(x))

def M_M_t(r_x, ttt, y, X_ctst, X_pr, X_ps, delta, ctst_icpt, ctst_coef, pr_icpt, pr_coef, ps_icpt, ps_coef, p_x):
    """Produces a (p1+p2+p3+4) * (p1+p2+p3+4) matrix M dot M transpose (central element of the sanwitch formula) """
    M = []
    for i in range(len(r_x)):
        M.append( np.empty((X_ctst.shape[1] + X_pr.shape[1] + X_ps.shape[1] + 4, 1) ) )
    
    # Delta (=ARE) estimating equation
        M[i][0] = p_x[i] * ( r_x[i] - ttt[i] ) * (ctst_icpt + np.dot(ctst_coef, X_ctst.iloc[i])) - delta
    
    # Contrast function estimating equations   
        M[i][1] = ( ttt[i] - sigmoid(ps_icpt + np.dot(ps_coef, X_ps.iloc[i])) ) * (y[i] - ttt[i] * (ctst_icpt + np.dot(ctst_coef, X_ctst.iloc[i]) ) - sigmoid(pr_icpt + np.dot(pr_coef, X_pr.iloc[i])) )
        
        for j in range(X_ctst.shape[1]):
            M[i][2+j] = X_ctst.iloc[i,j] * M[i][1]
    
    # Prognostic model estimating equations
        M[i][X_ctst.shape[1]+2] = y[i] - sigmoid(pr_icpt + np.dot(pr_coef, X_pr.iloc[i]) )
        
        for j in range(X_pr.shape[1]):
            M[i][X_ctst.shape[1]+3+j] = X_pr.iloc[i,j] * M[i][X_ctst.shape[1]+2]
            
    # PS model estimating equations
        M[i][X_ctst.shape[1]+X_pr.shape[1]+3] = ttt[i] - sigmoid(ps_icpt + np.dot(ps_coef, X_ps.iloc[i]) )
        
        for j in range(X_ps.shape[1]):
            M[i][X_ctst.shape[1]+X_pr.shape[1]+4+j] = X_ps.iloc[i,j] * M[i][X_ctst.shape[1]+X_pr.shape[1]+3]
    
    # Get list of M.dot(M.T)
    M_M_Ts = np.array([np.outer(element, element) for element in M])
    
    # Get element-wise mean of M_M_Ts
    M_M_T = np.mean(M_M_Ts, axis=0)
    
    return M_M_T

def M_jacob_inv(r_x, ttt, y, X_ctst, X_pr, X_ps, delta, ctst_icpt, ctst_coef, pr_icpt, pr_coef, ps_icpt, ps_coef, p_x):
    """Produces the (p1+p2+p3+4) * (p1+p2+p3+4) inverse of the jacobian matrix of the M unbiaised estimating equations:
    estimator for the left end part of the sanwitch formula """
    
    dim = X_ctst.shape[1] + X_pr.shape[1] + X_ps.shape[1] + 4
    Jacob = [np.ones((dim,dim)) for _ in range(len(r_x))]
    
    for patient in range(len(X_pr)):
    
        ### ARE row 
        ## derivation wrt delta
        Jacob[patient][0,0] = -1

        ## derivation wrt psi0
        Jacob[patient][0,1] = p_x[patient] * (r_x[patient] - ttt[patient] )

        ## derivation wrt psi_s
        for ctst_var in range(len(X_ctst.columns)):
            Jacob[patient][0, 2 + ctst_var] = X_ctst.iloc[patient,ctst_var] * Jacob[patient][0,1]

        ## derivation wrt phi_s
        for pr_var in range(1 + len(X_pr.columns)):
            Jacob[patient][0, 2 + len(X_ctst.columns) + pr_var] = 0

        ## derivation wrt gamma0
        Jacob[patient][0, 2 + len(X_ctst.columns) + len(X_pr.columns) + 1] = 0

        ## derivation wrt gamma_s
        for ps_var in range(len(X_ps.columns)):
            Jacob[patient][0, 2 + len(X_ctst.columns) + len(X_pr.columns) + 1 + 1 + ps_var] = 0


        ### A-learning row 1
        ## derivation wrt delta
        Jacob[patient][1,0] = 0

        ## derivation wrt psi0
        Jacob[patient][1,1] =  ( sigmoid( ps_icpt + np.dot(ps_coef, X_ps.iloc[patient]) ) - ttt[patient] ) * ttt[patient]

        ## derivation wrt psi_s
        for ctst_var in range(len(X_ctst.columns)):
            Jacob[patient][1, 2 + ctst_var] =  X_ctst.iloc[patient, ctst_var] * Jacob[patient][1,1]

        ## derivation wrt phi0
        Jacob[patient][1, 2 + len(X_ctst.columns)] =  ( sigmoid( ps_icpt + np.dot(ps_coef, X_ps.iloc[patient]) ) - ttt[patient] ) * sigmoid_deriv( pr_icpt + np.dot(pr_coef, X_pr.iloc[patient]) )

        ## derivation wrt phi_s
        for pr_var in range(len(X_pr.columns)):
            Jacob[patient][1, 2 + len(X_ctst.columns) + 1 + pr_var] = X_pr.iloc[patient, pr_var] * Jacob[patient][1, 2 + len(X_ctst.columns)]

        ## derivation wrt gamma0
        Jacob[patient][1, 2 + len(X_ctst.columns) + 1 + len(X_pr.columns)] = - sigmoid_deriv( ps_icpt + np.dot(ps_coef, X_ps.iloc[patient]) ) * (y[patient] - ttt[patient] * ( ctst_icpt + np.dot(ctst_coef, X_ctst.iloc[patient]) ) - sigmoid( pr_icpt + np.dot(pr_coef, X_pr.iloc[patient] ) ) )

        ## derivation wrt gamma_s
        for ps_var in range(len(X_ps.columns)):
            Jacob[patient][1, 2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + ps_var] = X_ps.iloc[patient, ps_var] * Jacob[patient][1, 2 + len(X_ctst.columns) + 1 + len(X_pr.columns)]

        ### A-learning next rows
        for row in range(len(X_ctst.columns)):
            ## derivation wrt delta
            Jacob[patient][2 + row,0] = 0

            ## derivation wrt psi0
            Jacob[patient][2 + row, 1] =  X_ctst.iloc[patient, row] * Jacob[patient][1,1]

            ## derivation wrt psi_s
            for ctst_var in range(len(X_ctst.columns)):
                Jacob[patient][2 + row, 2 + ctst_var] =  X_ctst.iloc[patient, ctst_var] * Jacob[patient][2 + row, 1]

            ## derivation wrt phi0
            Jacob[patient][2 + row, 2 + len(X_ctst.columns)] =  X_ctst.iloc[patient, row] * Jacob[patient][1, 2 + len(X_ctst.columns)]

            ## derivation wrt phi_s
            for pr_var in range(len(X_pr.columns)):
                Jacob[patient][2 + row, 2 + len(X_ctst.columns) + 1 + pr_var] = X_pr.iloc[patient, pr_var] * Jacob[patient][2 + row, 2 + len(X_ctst.columns)]

            ## derivation wrt gamma0
            Jacob[patient][2 + row, 2 + len(X_ctst.columns) + 1 + len(X_pr.columns)] = X_ctst.iloc[patient, row] * Jacob[patient][1, 2 + len(X_ctst.columns) + 1 + len(X_pr.columns)]

            ## derivation wrt gamma_s
            for ps_var in range(len(X_ps.columns)):
                Jacob[patient][2 + row, 2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + ps_var] = X_ps.iloc[patient, ps_var] * Jacob[patient][2 + row, 2 + len(X_ctst.columns) + 1 + len(X_pr.columns)]

        ### Prognosis row 1
        ## derivation wrt delta
        Jacob[patient][2 + len(X_ctst.columns), 0] = 0

        ## derivation wrt psi0
        Jacob[patient][2 + len(X_ctst.columns),1] = 0 

        ## derivation wrt psi_s
        for ctst_var in range(len(X_ctst.columns)):
            Jacob[patient][2 + len(X_ctst.columns), 2 + ctst_var] =  0

        ## derivation wrt phi0
        Jacob[patient][2 + len(X_ctst.columns), 2 + len(X_ctst.columns)] =  - sigmoid_deriv( pr_icpt + np.dot(pr_coef, X_pr.iloc[patient]) )

        ## derivation wrt phi_s
        for pr_var in range(len(X_pr.columns)):
            Jacob[patient][2 + len(X_ctst.columns), 2 + len(X_ctst.columns) + 1 + pr_var] =  X_pr.iloc[patient, pr_var] * Jacob[patient][2 + len(X_ctst.columns), 2 + len(X_ctst.columns)]

        ## derivation wrt gamma0
        Jacob[patient][2 + len(X_ctst.columns), 2 + len(X_ctst.columns) + 1 + len(X_pr.columns)] = 0

        ## derivation wrt gamma_s
        for ps_var in range(len(X_ps.columns)):
            Jacob[patient][2 + len(X_ctst.columns), 2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + ps_var] = 0


        ### Prognosis next rows
        for row in range(len(X_pr.columns)):

            ## derivation wrt delta
            Jacob[patient][2 + len(X_ctst.columns) + 1 + row, 0] = 0

            ## derivation wrt psi0
            Jacob[patient][2 + len(X_ctst.columns) + 1 + row, 1] = 0 

            ## derivation wrt psi_s
            for ctst_var in range(len(X_ctst.columns)):
                Jacob[patient][2 + len(X_ctst.columns) + 1 + row, 2 + ctst_var] =  0

            ## derivation wrt phi0
            Jacob[patient][2 + len(X_ctst.columns) + 1 + row, 2 + len(X_ctst.columns)] =  X_pr.iloc[patient, row] * Jacob[patient][2 + len(X_ctst.columns), 2 + len(X_ctst.columns)]

            ## derivation wrt phi_s
            for pr_var in range(len(X_pr.columns)):
                Jacob[patient][2 + len(X_ctst.columns) + 1 + row, 2 + len(X_ctst.columns) + 1 + pr_var] =  X_pr.iloc[patient, pr_var] * Jacob[patient][2 + len(X_ctst.columns) + 1 + row, 2 + len(X_ctst.columns)]

            ## derivation wrt gamma0
            Jacob[patient][2 + len(X_ctst.columns) + 1 + row, 2 + len(X_ctst.columns) + 1 + len(X_pr.columns)] = 0

            ## derivation wrt gamma_s
            for ps_var in range(len(X_ps.columns)):
                Jacob[patient][2 + len(X_ctst.columns) + 1 + row, 2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + ps_var] = 0

        ### PS row 1
        ## derivation wrt delta
        Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns), 0] = 0

        ## derivation wrt psi0
        Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns), 1] = 0 

        ## derivation wrt psi_s
        for ctst_var in range(len(X_ctst.columns)):
            Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns), 2 + ctst_var] =  0

        ## derivation wrt phi0
        Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns), 2 + len(X_ctst.columns)] =  0

        ## derivation wrt phi_s
        for pr_var in range(len(X_pr.columns)):
            Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns), 2 + len(X_ctst.columns) + 1 + pr_var] =  0

        ## derivation wrt gamma0
        Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns), 2 + len(X_ctst.columns) + 1 + len(X_pr.columns)] = - sigmoid_deriv( ps_icpt + np.dot(ps_coef, X_ps.iloc[patient]) )

        ## derivation wrt gamma_s
        for ps_var in range(len(X_ps.columns)):
            Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns), 2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + ps_var] = X_ps.iloc[patient, ps_var] * Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_ctst.columns), 2 + len(X_ctst.columns) + 1 + len(X_pr.columns)]

        ### PS next rows
        for row in range(len(X_ps.columns)):

            ## derivation wrt delta
            Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + row, 0] = 0

            ## derivation wrt psi0
            Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + row, 1] = 0 

            ## derivation wrt psi_s
            for ctst_var in range(len(X_ctst.columns)):
                Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + row, 2 + ctst_var] =  0

            ## derivation wrt phi0
            Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + row, 2 + len(X_ctst.columns)] =  0

            ## derivation wrt phi_s
            for pr_var in range(len(X_pr.columns)):
                Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + row, 2 + len(X_ctst.columns) + 1 + pr_var] =  0

            ## derivation wrt gamma0
            Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + row, 2 + len(X_ctst.columns) + 1 + len(X_pr.columns)] = X_ps.iloc[patient, row] * Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns), 2 + len(X_ctst.columns) + 1 + len(X_pr.columns)]

            ## derivation wrt gamma_s
            for ps_var in range(len(X_ps.columns)):
                Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + row, 2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + ps_var] = X_ps.iloc[patient, ps_var] * Jacob[patient][2 + len(X_ctst.columns) + 1 + len(X_pr.columns) + 1 + row, 2 + len(X_ctst.columns) + 1 + len(X_pr.columns)]
    
    # Get element-wise mean of the jacobian matrices
    Mean_Jacob = np.mean(Jacob, axis=0)
    
    # Return the inverse of this mean jacobian matrix
    return np.linalg.pinv(Mean_Jacob)


def V_cov_mat(df, rule, ttt, y, ps_predictors, pronostic_predictors, ctst_vrb, p_x):
    
    """This program performs ARE through A-learning/Logistic regression and 
    returns all parameters along their variance covariance matrix from M-estimation theory
    ARE is the first parameter, its variance corresponds to the top left element in the VCV matrix"""
    
    df_temp = df.copy()

    ## A-learning step
    
    # Fit PS model
    from sklearn.linear_model import LogisticRegression
    ps_mod = LogisticRegression(max_iter=2000)
    ps_mod = ps_mod.fit(df[ps_predictors], df[ttt])
    df_temp["e_hat"] = ps_mod.predict_proba(df[ps_predictors])[:,1]      

    # Fit prognositic model
    # If outcome is binary use logistic regression
    if np.isin(df[y].dropna().unique(), [0,1]).all() == True:
    
        pr_mod = LogisticRegression(max_iter=2000)
        pronostic_predictors_A = pronostic_predictors.copy()
        pronostic_predictors_A.append(ttt)
        pr_mod1 = pr_mod.fit(df.loc[:,pronostic_predictors_A], df.loc[:,y])

        X = df.loc[:,pronostic_predictors]
        X[ttt] = np.repeat(0, len(X))        
        df_temp["y0_hat"] = pr_mod1.predict_proba(X)[:,1]
    
    # Else if outcome is continuous use linear regression
    else:
        from sklearn.linear_model import LinearRegression
        pr_mod = LinearRegression()
        pronostic_predictors_A = pronostic_predictors.copy()
        pronostic_predictors_A.append(ttt)
        pr_mod1 = pr_mod.fit(df.loc[:,pronostic_predictors_A], df.loc[:,y])

        X = df.loc[:,pronostic_predictors]
        X[ttt] = np.repeat(0, len(X))        
        df_temp["y0_hat"] = pr_mod1.predict(X)

    # Apply A-learning perse and get contrast ( coefficients, predictions )
    psi_hat, df_temp["cate_hat"] = A_learning(df = df_temp, ctst_vrb = ctst_vrb, ps = "e_hat", nu = "y0_hat", ttt = ttt, y = y)            
    
    # Compute ARE and organize all other parameters
    are_hat = np.array( np.mean( (df_temp[rule] - df_temp[ttt]) * df_temp.cate_hat) ).squeeze()
    
    psi_hat_icpt = psi_hat[0].squeeze()
    psi_hat_coef = psi_hat[1:].squeeze()
    
    phi_hat_icpt = pr_mod.intercept_.squeeze()
    
    if np.isin(df[y].dropna().unique(), [0,1]).all() == True: # .coef_ is 2 dimentional when fit with logistic regression
        phi_hat_coef = pr_mod.coef_[0,:-1].squeeze() # coef for treatment variable is excluded, was only present so that the model could be fit on all patients and not only those who did not receive ttt
    else:                                                     # .coef_ is 1 dimentional when fit with linear regression
        phi_hat_coef = pr_mod.coef_[:-1].squeeze()
        
    gamma_hat_icpt = ps_mod.intercept_.squeeze()
    gamma_hat_coef = ps_mod.coef_.squeeze()
    
    # Store parameters
    parameters = np.hstack([are_hat, psi_hat_icpt, psi_hat_coef, phi_hat_icpt, phi_hat_coef, gamma_hat_icpt, gamma_hat_coef ])

    # Compute Lateral estimator from the sandwitch formula
    Lat = M_jacob_inv(r_x = df_temp[rule],
      ttt = df_temp[ttt], 
      y = df_temp[y],
      X_ctst = df_temp.loc[:, ctst_vrb],
      X_pr = df_temp.loc[:, pronostic_predictors],
      X_ps = df_temp.loc[:, ps_predictors],
      delta = are_hat,
      ctst_icpt = psi_hat_icpt,
      ctst_coef = psi_hat_coef,
      pr_icpt = phi_hat_icpt,
      pr_coef = phi_hat_coef,
      ps_icpt = gamma_hat_icpt,
      ps_coef = gamma_hat_coef,
      p_x = p_x)
    
    # Compute Central estimator from the sandwitch formula
    Central = M_M_t(r_x = df_temp[rule],
      ttt = df_temp[ttt], 
      y = df_temp[y],
      X_ctst = df_temp.loc[:, ctst_vrb],
      X_pr = df_temp.loc[:, pronostic_predictors],
      X_ps = df_temp.loc[:, ps_predictors],
      delta = are_hat,
      ctst_icpt = psi_hat_icpt,
      ctst_coef = psi_hat_coef,
      pr_icpt = phi_hat_icpt,
      pr_coef = phi_hat_coef,
      ps_icpt = gamma_hat_icpt,
      ps_coef = gamma_hat_coef,
      p_x = p_x)
    
    # Compute the sandwitch formula for sigma
    Sigma = Lat.dot(Central).dot(Lat.T)
    
    # Get the variance covariance matrix
    VCV = Sigma / len(df_temp) 
    
    return parameters, VCV, are_hat, psi_hat_icpt, psi_hat_coef, phi_hat_icpt, phi_hat_coef, gamma_hat_icpt, gamma_hat_coef, df_temp["cate_hat"]

def V_cov_mat_fast(df_temp, rule, ttt, y, ps_predictors, pronostic_predictors, ctst_vrb, p_x, are_hat, psi_hat_icpt, psi_hat_coef, phi_hat_icpt, phi_hat_coef, gamma_hat_icpt, gamma_hat_coef):
    
    """Fast computation of all parameters VCV when parameters have been comptued elswhere and are passed to this program"""
    
    # Compute Lateral estimator from the sandwitch formula
    Lat = M_jacob_inv(r_x = df_temp[rule],
      ttt = df_temp[ttt], 
      y = df_temp[y],
      X_ctst = df_temp.loc[:, ctst_vrb],
      X_pr = df_temp.loc[:, pronostic_predictors],
      X_ps = df_temp.loc[:, ps_predictors],
      delta = are_hat,
      ctst_icpt = psi_hat_icpt,
      ctst_coef = psi_hat_coef,
      pr_icpt = phi_hat_icpt,
      pr_coef = phi_hat_coef,
      ps_icpt = gamma_hat_icpt,
      ps_coef = gamma_hat_coef,
      p_x = p_x)
    
    # Compute Central estimator from the sandwitch formula
    Central = M_M_t(r_x = df_temp[rule],
      ttt = df_temp[ttt], 
      y = df_temp[y],
      X_ctst = df_temp.loc[:, ctst_vrb],
      X_pr = df_temp.loc[:, pronostic_predictors],
      X_ps = df_temp.loc[:, ps_predictors],
      delta = are_hat,
      ctst_icpt = psi_hat_icpt,
      ctst_coef = psi_hat_coef,
      pr_icpt = phi_hat_icpt,
      pr_coef = phi_hat_coef,
      ps_icpt = gamma_hat_icpt,
      ps_coef = gamma_hat_coef,
      p_x = p_x)
    
    # Compute the sandwitch formula for sigma
    Sigma = Lat.dot(Central).dot(Lat.T)
    
    # Get the variance covariance matrix
    VCV = Sigma / len(df_temp) 
    
    return VCV

def asre_package(df, rule, ttt, y, ps_predictors, pronostic_predictors, ctst_vrb, est='ARE', alpha = .5, n_alphas=5, precision=3):
    
    """From a pandas dataframe, this program computes through A-learning the ARE or cognitive biais ASRE along their 95% confidence intervals."""
    
    df_temp = df.copy()

    p_x = np.repeat(1, len(df))
    
    parameters, VCV, are_hat, psi_hat_icpt, psi_hat_coef, phi_hat_icpt, phi_hat_coef, gamma_hat_icpt, gamma_hat_coef, df_temp["cate_hat"] = V_cov_mat(df_temp, rule, ttt, y, ps_predictors, pronostic_predictors, ctst_vrb, p_x)
    
    are_hat = parameters[0]
    se_are = np.sqrt(VCV[0,0])
    print('ARE = ' + str(np.round(are_hat, precision)) + '  95% CI (' + 
          str(np.round(parameters[0] - st.norm.ppf(.975) * se_are, precision)) + ' to ' + 
          str(np.round(parameters[0] + st.norm.ppf(.975) * se_are, precision)) + ')' )
    
    estimator = 'ARE'
    
    if est == 'ASRE_cb':
        estimator = 'ASRE_cb_' + str(alpha)

        def sigmoid(x):
            return 1/(1+np.exp(-x))
        
        ps_pred = sigmoid( gamma_hat_icpt + df_temp[ps_predictors].dot(gamma_hat_coef) )
        
        def legit(x):
            return .5 * np.log((x+1)/(1-x))
        
        p_x = ( 1 - np.abs( df_temp[rule] - ps_pred ) ) ** legit(alpha)
               
        VCV = V_cov_mat_fast(df_temp, rule, ttt, y, ps_predictors, pronostic_predictors, ctst_vrb, p_x, are_hat, psi_hat_icpt, psi_hat_coef, phi_hat_icpt, phi_hat_coef, gamma_hat_icpt, gamma_hat_coef)
        
        asre_hat = np.array( np.mean( p_x * (df_temp[rule] - df_temp[ttt]) * df_temp["cate_hat"]) ).squeeze()
        
        se_asre = np.sqrt(VCV[0,0])
        print('ASRE (cognitive biais ' + str(alpha) + ')' + ' = ' + str(np.round(asre_hat, precision)) + '  95% CI (' + 
        str(np.round(parameters[0] - st.norm.ppf(.975) * se_asre, precision)) + ' to ' + 
        str(np.round(parameters[0] + st.norm.ppf(.975) * se_asre, precision)) + ')' )
        
        alphas = np.linspace(0,1,n_alphas+1)[:-1]
        asre_hats = []
        asre_ses = []
        cb_mean_px_alphas = []
        
        for alpha in alphas:
            p_x_temp = ( 1 - np.abs( df_temp[rule] - ps_pred ) ) ** legit(alpha)
            VCV_temp = V_cov_mat_fast(df_temp, rule, ttt, y, ps_predictors, pronostic_predictors, ctst_vrb, p_x_temp, are_hat, psi_hat_icpt, psi_hat_coef, phi_hat_icpt, phi_hat_coef, gamma_hat_icpt, gamma_hat_coef)
            asre_hats.append( np.mean( p_x_temp * (df_temp[rule] - df_temp[ttt]) * df_temp["cate_hat"]) )
            asre_ses.append(np.sqrt(VCV_temp[0,0]))
            cb_mean_px_alphas.append( np.mean(p_x_temp) )
            
        asre_hats_lci = np.array(asre_hats) - st.norm.ppf(.975) * np.array(asre_ses)
        asre_hats_lci = np.append(asre_hats_lci, 0)
        
        asre_hats_uci = np.array(asre_hats) + st.norm.ppf(.975) * np.array(asre_ses)
        asre_hats_uci = np.append(asre_hats_uci, 0)
        
        alphas = np.append(alphas, 1)
        asre_hats = np.append(asre_hats, 0)
        cb_mean_px_alphas = np.append( np.array(cb_mean_px_alphas), 0 )
            
        fig, axs = plt.subplots(1, 2, figsize=(10,5))

        fig.suptitle("Impact of rule's stochastic implementation on the observational population provided", fontsize=11)
        axs[0].plot([0,1],[0, 0], color= "black", alpha=1, linewidth=.5, linestyle='solid')
        axs[0].plot([0,1],[are_hat, are_hat], color= "black", alpha=.9, linewidth=1, linestyle='dashed', label=r'$\widehat{ARE}$')
        axs[0].plot(alphas, asre_hats, 'o', color= "tab:orange", label="Cognitive biais implementation")
        axs[0].fill_between(alphas, asre_hats_lci, asre_hats_uci, color="tab:orange", alpha=.1, label="95% Confidence Interval")

        axs[0].set_xlabel('Cognitive Biais', fontsize=10)
        axs[0].set_ylabel(r'$\widehat{ASRE}$', fontsize=20)

        axs[0].set_xlim([-.01,1])
        axs[1].set_xlim([-.01,1])
        
        if are_hat < 0:
            axs[0].set_ylim([ asre_hats_lci[0] + are_hat/10, np.max([asre_hats_uci[0], 0]) - are_hat/10 ])
            axs[1].set_ylim([ asre_hats_lci[0] + are_hat/10, np.max([asre_hats_uci[0], 0]) - are_hat/10 ])
            
        else:
            axs[0].set_ylim([ np.min([asre_hats_lci[0], 0]) - are_hat/10, asre_hats_uci[0] + are_hat/10 ])
            axs[0].set_ylim([ np.min([asre_hats_lci[0], 0]) - are_hat/10, asre_hats_uci[0] + are_hat/10 ])

        axs[1].plot([0,1],[0, 0], color= "black", alpha=1, linewidth=.5, linestyle='solid')
        axs[1].plot([0,1],[are_hat, are_hat], color= "black", alpha=.9, linewidth=1, linestyle='dashed', label=r'$\widehat{ARE}$')
        axs[1].plot(cb_mean_px_alphas, asre_hats, 'o', color= "tab:orange", label="Cognitive biais implementation")
        axs[1].fill_between(cb_mean_px_alphas, asre_hats_lci, asre_hats_uci, color="tab:orange", alpha=.1, label="95% Confidence Interval")
        axs[1].set_xlabel('Fraction of the population implementing the rule', fontsize=10)
        
        axs[1].legend();
        
        print('\nIn a tuple, this program returs the ASRE plot as well as all parameters along their corresponding variance-covariance matrix.')
        print('Parameters are provided in the following order.')
        print(estimator + ', Contrast intercept, Contrast coefficients, Prognostic intercept, Prognostic coefficients, Propensity score intercept, Propensity score coefficients.')
        return fig, parameters, VCV
    
    else :
        print('\nIn a tuple, this program returs all parameters along their corresponding variance-covariance matrix.')
        print('Parameters are provided in the following order.')
        print(estimator + ', Contrast intercept, Contrast coefficients, Prognostic intercept, Prognostic coefficients, Propensity score intercept, Propensity score coefficients.')
        return parameters, VCV