# ------------------------------------------------------------------------
#                           caltransfer methods
# by: Valeria Fonseca Diaz
#  ------------------------------------------------------------------------


import numpy as np
from sklearn.cross_decomposition import PLSRegression
from sklearn.linear_model import LinearRegression


def ds_pc_transfer_fit(X_primary, X_secondary, max_ncp):
    

    '''    
    Direct Standardization (DS) based on PCR. Normally calculated with a high number of components (full rank)
    Method based on standard samples
    
    Parameters
    ----------    
    X_primary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from primary domain
        
    X_secondary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from secondary domain. X_secondary is expected to be paired with X_primary (standard samples)
        
    max_ncp : int
        Number of pc's to train DS model. For classical DS, max_ncp = K
        
    Returns
    -------    
    out : tuple
        (F,a), where `F` is the standardization matrix and `a` is the offset.
        F : ndarray (K,K)
        a : ndarray (1,K)
        
    Notes
    -----
    `F` and `a` used as:
        .. math:: X_p = X_s F + a
    If used for a bilinear model of the type 
        .. math:: y = X_p B_p + \beta_p
    then the final regression model after DS transfer becomes
        .. math:: B_s = F B_p
        .. math:: \beta_s = a B_p + \beta_p
        
    References
    ----------
    Y. Wang, D. J. Veltkamp, and B. R. Kowalski, “Multivariate Instrument Standardization,” Anal. Chem., vol. 63, no. 23, pp. 2750–2756, 1991, doi: 10.1021/ac00023a016.
    
    Examples
    --------
    
    >>> import numpy as np
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> F_sim = np.array([[0., -0.2, 1.], [1.,0.6,0.8], [0.4,2.5,-1.3]])
    >>> a_sim = np.array([[2.,5.,4.]])
    >>> X_secondary = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> X_primary = X_secondary.dot(F_sim) + a_sim + x_error
    >>> x_mean = np.mean(X_primary, axis = 0)
    >>> x_mean.shape = (1,X_primary.shape[1])
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> # plsr model primary domain
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(X_primary, Y)
    >>> B_p = pls2.coef_
    >>> beta_p = pls2.y_mean_ - (x_mean.dot(B_p)) # baseline model y = X_primary B_p + beta_p
    >>> # DS transfer
    >>> F, a = caltransfer.ds_pc_transfer_fit(X_primary, X_secondary, max_ncp = 2) # with 3 components it's already a perfect fit (possibly over fit)
    >>> B_ds = F.dot(B_p)
    >>> beta_s = a.dot(B_p) + beta_p # transferred model y = X_secondary B_s + beta_s
    >>> print(pls2.predict(X_primary))
    >>> print(pls2.predict(X_secondary.dot(F) + a))
    [[ 0.10057381]
     [ 1.03398846]
     [ 5.95594099]
     [12.00949675]]
    [[ 0.18648704]
     [ 0.80221134]
     [ 6.23273672]
     [11.87856491]]



   

    
    '''

    kk = X_primary.shape[1]
    N = X_primary.shape[0]
    ww = 2*kk


    F = np.zeros((kk,kk))
    a = np.zeros((1,kk))

    mean_primary = X_primary.mean(axis=0)
    mean_secondary = X_secondary.mean(axis=0)
    X_primary_c = X_primary - mean_primary
    X_secondary_c = X_secondary - mean_secondary
    
    
    X_in = X_secondary_c[:, :]
    current_ncp = np.amin([max_ncp,X_in.shape[1]])
        

    # ------ svd

    U0,S,V0t = np.linalg.svd(X_in.T.dot(X_in),full_matrices=True)
    S_matrix = np.zeros((current_ncp,current_ncp))
    S_matrix[0:current_ncp,:][:,0:current_ncp] = np.diag(S[0:current_ncp])
    V = V0t[0:current_ncp,:].T
    U = U0[:,0:current_ncp]
    
    X_out = X_primary_c[:, :]  
    
    F = U.dot(np.linalg.inv(S_matrix)).dot(V.T).dot(X_in.T).dot(X_out)
    
    a = mean_primary - F.T.dot(mean_secondary)
    
    a.shape = (1,a.shape[0]) # row vector

 
    
    return (F,a)

    


def pds_pls_transfer_fit(X_primary, X_secondary, max_ncp, ww):
    
    '''
    
    (Piecewise) Direct Standardization (PDS) based on PLSR 
    Method based on standard samples
    
    Parameters
    ----------    
    X_primary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from primary domain
        
    X_secondary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from secondary domain. X_secondary is expected to be paired with X_primary (standard samples)
        
    max_ncp : int
        Number of latent variables for PLSR models.
        
    ww : int
        Half of the total window width. The total window width is 2*ww + 1
        
    Returns
    -------    
    out : tuple
        (F,a), where `F` is the standardization matrix and `a` is the offset.
        F : ndarray (K,K)
        a : ndarray (1,K)
        
    Notes
    -----
    `F` and `a` used as:
        .. math:: X_p = X_s F + a
    If used for a bilinear model of the type 
        .. math:: y = X_p B_p + \beta_p
    then the final regression model after PDS transfer becomes
        .. math:: B_s = F B_p
        .. math:: \beta_s = a B_p + \beta_p
        
    References
    ----------
    E. Bouveresse and D. L. Massart, “Improvement of the piecewise direct standardisation procedure for the transfer of NIR spectra for multivariate calibration,”   Chemom. Intell. Lab. Syst., vol. 32, no. 2, pp. 201–213, 1996, doi: 10.1016/0169-7439(95)00074-7.
    
    Examples
    --------
    
    >>> import numpy as np
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> F_sim = np.array([[0., -0.2, 1.], [1.,0.6,0.8], [0.4,2.5,-1.3]])
    >>> a_sim = np.array([[2.,5.,4.]])
    >>> X_secondary = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> X_primary = X_secondary.dot(F_sim) + a_sim + x_error
    >>> x_mean = np.mean(X_primary, axis = 0)
    >>> x_mean.shape = (1,X_primary.shape[1])
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> # plsr model primary domain
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(X_primary, Y)
    >>> B_p = pls2.coef_
    >>> beta_p = pls2.y_mean_ - (pls2.x_mean_.dot(B_p)) # baseline model y = X_primary B_p + beta_p
    >>> # PDS transfer
    >>> F, a = caltransfer.pds_pls_transfer_fit(X_primary, X_secondary, max_ncp = 1, ww = 1) # ww = 1 means a total window width of 3
    >>> B_ds = F.dot(B_p)
    >>> beta_s = a.dot(B_p) + beta_p # transferred model y = X_secondary B_s + beta_s
    >>> print(pls2.predict(X_primary))
    >>> print(X_primary.dot(B_p) + beta_p)
    >>> print(pls2.predict(X_secondary.dot(F) + a))
    [[ 0.10057381]
     [ 1.03398846]
     [ 5.95594099]
     [12.00949675]]
    [[ 0.10057381]
     [ 1.03398846]
     [ 5.95594099]
     [12.00949675]]
    [[ 0.76356358]
     [ 0.5984284 ]
     [ 5.69538785]
     [12.04262017]]




    '''

    kk = X_primary.shape[1]
    N = X_primary.shape[0]
   


    F = np.zeros((kk,kk))
    a = np.zeros((1,kk))

    mean_primary = X_primary.mean(axis=0)
    mean_secondary = X_secondary.mean(axis=0)
    X_primary_c = X_primary - mean_primary
    X_secondary_c = X_secondary - mean_secondary

    for jj_out in range(0,kk):

        # --- wv to predict    


        X_out = X_primary_c[:, jj_out]     


        # --- input matrix

        ll = np.amax([0, jj_out - ww])
        ul = np.amin([jj_out + ww, kk-1])
        jj_in = np.arange(ll, ul+1)
        X_in = X_secondary_c[:, jj_in]

        chosen_lv = np.amin([max_ncp,X_in.shape[1]])
        
        # --- pls transfer
        
 
        my_pls = PLSRegression(n_components = chosen_lv,scale=False)
        my_pls.fit(X_in, X_out)
        
 
        F[jj_in,jj_out] = my_pls.coef_[:,0]


    a[0,:] = mean_primary - F.T.dot(mean_secondary)
    
    return (F,a)


def epo_fit(X_primary, X_secondary,epo_ncp=1):
    
    
    '''
    
    External Parameter Orthogonalization (EPO) based on spectral value decomposition (SVD) of the difference matrix
    Method based on standard samples
    
    Parameters
    ----------    
    X_primary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from primary domain
        
    X_secondary : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K) from secondary domain. X_secondary is expected to be paired with X_primary (standard samples)
        
    epo_ncp : int
        Number of EPO components to remove. 
          
    Returns
    -------    
    out : tuple
        (E,a), where `E` is the orthogonalization matrix and `a` is the offset.
        E : ndarray (K,K)
        a : ndarray (1,K)
        
    Notes
    -----
    `E` comes from `SVD(D)` where `D = X_primary - X_secondary`
    Orthogonalization of matrices as:
        .. math:: X_{pE} = X_p E + a
        .. math:: X_{sE} = X_s E + a
    If used for a bilinear model, retrain model using `X_{pE}` and `y`. Obtain model 
        .. math:: y = X_{pE} B_e + \beta_e
    Then the final regression model after EPO transfer becomes
        .. math:: B_s = E B_e
        .. math:: \beta_s = a B_e + \beta_e
        
    References
    ----------
    
    M. Zeaiter, J. M. Roger, and V. Bellon-Maurel, “Dynamic orthogonal projection. A new method to maintain the on-line robustness of multivariate calibrations. Application to NIR-based monitoring of wine fermentations,” Chemom. Intell. Lab. Syst., vol. 80, no. 2, pp. 227–235, 2006, doi: 10.1016/j.chemolab.2005.06.011.
    J. M. Roger, F. Chauchard, and V. Bellon-Maurel, “EPO-PLS external parameter orthogonalisation of PLS application to temperature-independent measurement of sugar content of intact fruits,” Chemom. Intell. Lab. Syst., vol. 66, no. 2, pp. 191–204, 2003, doi: 10.1016/S0169-7439(03)00051-0.
    
    Examples
    --------
    >>> import numpy as np
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> X_primary = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> X_secondary = X_primary + x_error
    >>> # Fit EPO
    >>> E,a = caltransfer.epo_fit(X_primary, X_secondary,epo_ncp=1)
    >>> X_primary_e = X_primary.dot(E) + a
    >>> x_mean_e = np.mean(X_primary_e, axis = 0)
    >>> x_mean_e.shape = (1,X_primary_e.shape[1])
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> # PLSR after EPO
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(X_primary_e, Y)
    >>> B_pe = pls2.coef_
    >>> beta_pe = pls2.y_mean_ - (x_mean_e.dot(B_pe)) # Model after EPO y = X_se B_pe + beta_pe; X_se = X_s E +a
    >>> B_s = E.dot(B_pe)
    >>> beta_s = a.dot(B_pe) + beta_pe # transferred model y = X_s Bs + beta_s
    >>> print(X_secondary.dot(B_s) + beta_s)
    >>> print(Y)
    [[ 0.47210387]
     [-0.01622479]
     [ 6.95309782]
     [10.92865516]]
    [[ 0.1]
     [ 0.9]
     [ 6.2]
     [11.9]]

    
    '''  
    
    D = X_primary - X_secondary


    U0,S,V0t = np.linalg.svd(D)
    S_matrix = np.zeros((epo_ncp,epo_ncp))
    S_matrix[0:epo_ncp,:][:,0:epo_ncp] = np.diag(S[0:epo_ncp])
    V = V0t[0:epo_ncp].T
    U = U0[:,0:epo_ncp]

    E = np.identity(n=V.shape[0]) - V.dot(V.T)    
    a = np.mean(X_primary,axis=0)
    a.shape = (1,a.shape[0]) # row vector    

    
    return (E, a)


def jointypls_regression(tscores_primary,tscores_secondary, y_primary, y_secondary):
    
    '''
    
    Re-specification of Q parameters based on scores variables (or latent variables) from an existing PLSR model.
    This function should be used for univariate response (y 1D)
    
    Parameters
    ----------    
    tscores_primary : ndarray
        A 2-D array containing the scores of the primary domain spectra (assumed to be centered). Shape (Np,A)
        
    tscores_secondary : ndarray
        A 2-D array containing the scores of the secondary domain spectra (assumed to be centered). Shape (Ns,A)
        
    y_primary : ndarray
         A 1-D array with reference values of primary spectra. Shape (Np,) 
         
    y_secondary : ndarray
        A 1-D array with reference values of secondary spectra. Shape (Ns,)
        
    Returns
    -------
    out : tuple
        (q_jpls,b), where `q_jpls` is the set of coefficients in the output layer of the bilinear model and `b` is the new intercept.
        q_jpls : array of shape (A,) 
        a : float
    
    Notes
    -----
    If used for a bilinear model of the type 
        .. math:: y = X_p B_p + \beta_p
    where `B_p = Rq`, then the new regression vector is
        .. math:: B_{jpls} = Rq_{jpls}
        .. math:: \beta_{jpls} = b - (\bar(x) B_{jpls})
        
    References
    ----------
    S. García Muñoz, J. F. MacGregor, and T. Kourti, “Product transfer between sites using Joint-Y PLS,” Chemom. Intell. Lab. Syst., vol. 79, no. 1–2, pp. 101–114, 2005, doi: 10.1016/j.chemolab.2005.04.009.
    A. Folch-Fortuny, R. Vitale, O. E. de Noord, and A. Ferrer, “Calibration transfer between NIR spectrometers: New proposals and a comparative study,” J. Chemom., vol. 31, no. 3, pp. 1–11, 2017, doi: 10.1002/cem.2874.
    
    Examples
    --------
    
    >>> import numpy as np
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> X_secondary = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> X_primary = X_secondary + x_error
    >>> x_mean = np.mean(X_primary, axis = 0)
    >>> x_mean.shape = (1,X_primary.shape[1])
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> # PLSR
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(X_primary, Y)
    >>> R_p = pls2.x_rotations_
    >>> B_p = pls2.coef_
    >>> beta_p = pls2.y_mean_ - (x_mean.dot(B_p)) # baseline model y = X_primary B_p + beta_p
    >>> # Transfer with Joint Y PLS. Here a subset of samples or other samples can be used. For the example we use the same samples
    >>> tprimary = (X_primary-x_mean).dot(R_p)
    >>> tsecondary = (X_secondary-x_mean).dot(R_p)
    >>> y_primary = Y[:,0] # flatten 1D
    >>> y_secondary = Y[:,0] # flatten 1D
    >>> q_jpls,b_jpls = caltransfer.jointypls_regression(tprimary, tsecondary, y_primary, y_secondary)
    >>> B_jpls = R_p.dot(q_jpls)  
    >>> beta_jpls = np.asarray(b_jpls - (x_mean).dot(B_jpls))
    >>> print(X_primary.dot(B_jpls) + beta_jpls)
    >>> print(X_secondary.dot(B_jpls) + beta_jpls)
    [ 0.0759273   1.01125531  6.07352354 11.87814864]
    [ 0.12036472  0.81699714  6.28765203 11.93613132]
    

    '''
 
    t_jointpls = np.concatenate((tscores_primary,tscores_secondary), axis = 0)
    y_jointpls = np.concatenate((y_primary,y_secondary), axis = 0)


    calmodel_tr_jointpls = LinearRegression()
    calmodel_tr_jointpls.fit(t_jointpls,y_jointpls) # output values need to be 1D always here
    
            # output
    
    q_jpls = calmodel_tr_jointpls.coef_ 
    b_jpls = calmodel_tr_jointpls.intercept_
  
    
    return (q_jpls,b_jpls)



def slope_bias_correction(y_secondary, y_secondary_pred):
    
    '''
    
    Slope and Bias Correction (SBC) as `y_secondary = b + s*y_secondary_pred`
    This function should be used for univariate response (y 1D)
    
    Parameters
    ----------
    y_secondary : ndarray
        A 1-D array with observed reference values of secondary spectra. Shape (Ns,)
        
    y_secondary_pred : ndarray
        A 1-D array with predicted reference values of secondary spectra using primary model. Shape (Ns,)
        
    Returns
    -------
    out : tuple
        (slope,bias) 
        slope : float 
        bias : float
        
    Notes
    -----
    
    SBC corrects the predictions as `y = y_pred *s + b`
    If used for a bilinear model of the type 
        .. math:: y = X_p B_p + \beta_p
    then the transferred model becomes
        .. math:: B_s = B_p*s
        .. math:: \beta_s = \beta_p*s + b
        
    References
    ----------
    T. Fearn, “Standardisation and calibration transfer for near infrared instruments: A review,” J. Near Infrared Spectrosc., vol. 9, no. 4, pp. 229–244, 2001, doi: 10.1255/jnirs.309.
    
    Examples
    --------
    >>> import numpy as np
    >>> from sklearn.cross_decomposition import PLSRegression
    >>> import pycaltransfer.caltransfer as caltransfer
    >>> X_secondary = np.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [2.,5.,4.]])
    >>> x_error = np.array([[-0.03774524, -0.00475627,  0.01938877],
    ...       [-0.02925257,  0.1500586 ,  0.01706783],
    ...       [-0.11049506, -0.03469373, -0.03136003],
    ...       [-0.00685062, -0.00367186, -0.07211823]])
    >>> X_primary = X_secondary + x_error
    >>> x_mean = np.mean(X_primary, axis = 0)
    >>> x_mean.shape = (1,X_primary.shape[1])
    >>> Y = np.array([[0.1], [0.9], [6.2], [11.9]])
    >>> # PLSR
    >>> pls2 = PLSRegression(n_components=2,scale=False)
    >>> pls2.fit(X_primary, Y)
    >>> R_p = pls2.x_rotations_
    >>> B_p = pls2.coef_
    >>> beta_p = pls2.y_mean_ - (x_mean.dot(B_p)) # baseline model y = X_primary B_p + beta_p
    >>> # Transfer with Slope and Bias Correction
    >>> y_secondary = Y[:,0]
    >>> y_secondary_pred = X_secondary.dot(B_p) + beta_p
    >>> slope, bias = caltransfer.slope_bias_correction(y_secondary, y_secondary_pred)
    >>> B_sbc = B_p.dot(slope)
    >>> beta_sbc = beta_p.dot(slope) + bias
    >>> print(y_secondary)
    >>> print(X_secondary.dot(B_sbc) + beta_sbc)
    [ 0.1  0.9  6.2 11.9]
    [ 0.15333474  0.81766258  6.25070668 11.87829601]

    '''
    
    sbc = LinearRegression()
    sbc.fit(y_secondary_pred, y_secondary)
    
    slope = sbc.coef_
    bias = sbc.intercept_
    
    return (slope, bias)
    



def nipals_dipls(X,y_uni,Xs,Xt,nlv,lambda_, mode = 0):
    
    
    '''
    
    Domain-Invariant Partial Least Squares(di-PLS) Regression. This algorithm is for univariate response    
    Algorithm based on: 
    Domain-Invariant Partial Least Squares(di-PLS) Regression
    https://pubs.acs.org/doi/abs/10.1021/acs.analchem.8b00498
    Algorithm: https://pubs.acs.org/doi/suppl/10.1021/acs.analchem.8b00498/suppl_file/ac8b00498_si_001.pdf
    In the jargon of this algorithm, `primary` is referred to as `source` and `secondary` is referred to as `target`.
    
    
    Parameters
    ----------
    X : ndarray
        A 2-D array corresponding to the spectral matrix. Shape (N, K). This array can be the source calibration data or a concatenation of the source and target data whose reference values are available. (See parameter mode) 
        
    y_uni : ndarray
        A 1-D array of reference values.  Shape (N,). This array can be the source calibration data or a concatenation of the source and target data whose reference values are available (See parameter mode) 
    
    Xs : ndarray
        A 2-D array corresponding to source spectral data.  Shape (Ns,K). (See parameter mode) 
        
    Xt : ndarray
        A 2-D array corresponding to target spectral data. Shape (Nt,K).  (See parameter mode) 
        
    nlv : int
        Number of latent variables
        
    lambda_ : float
        Regularization parameter
        
    mode : int, default=0
        Options are 0, 1, 2.
        |0 : Unsupervised mode. `X` and `y_uni` correspond to source calibration data. `Xs` is the same as `X`. `Xt` is target spectra without reference analyses. 
        |1 : (Semi)supervised mode. `X` and `y_uni` correspond to a concatenation of source calibration data and target data with reference analyses. `Xs` is only the source calibration data. `Xt` is target spectra with and without reference analyses.
        |2: Calibration transfer mode.  `X` and `y_uni` correspond to source calibration data. `Xs` and `Xt` are standard samples from source and target.
    
    Returns
    -------
    out : tuple
        (B,beta,R,Q,x_mu_target_torecenter,b0)
        B : ndarray. Regression vector.  Shape (K,1). 
        beta : ndarray. Bias term. 
        R : ndarray. Loadings. Shape (K, nlv)
        Q : ndarray. Regression coefficients output layer. Shape (nlv, 1)
        x_mu_target_torecenter: ndarray. `X` mean to be retained. This depends on parameter mode.
        b0 : float. Bias term output layer (`y` mean)
        
    Notes
    -----
    For this bilinear model, the final model for target  (secondary) data is specified as
        .. math:: B = RQ
        .. math:: \beta = b_0 - (\hat(x)B)
        .. math:: y = Xt B + \beta
        
    References
    ----------
    R. Nikzad-Langerodi, W. Zellinger, E. Lughofer, and S. Saminger-Platz, “Domain-Invariant Partial-Least-Squares Regression,” Anal. Chem., vol. 90, no. 11, pp. 6693–6701, 2018, doi: 10.1021/acs.analchem.8b00498.
    
    Examples
    --------
    
    For a full application see the jupyter notebooks at https://gitlab.com/vfonsecad/pycaltransfer
        

    '''
    
    assert y_uni.ndim < 2 or y_uni.shape[1] == 1, "this algorithm is for univariate response"

    
    y = y_uni.copy()
    
    if y.ndim == 1:
        y.shape = (y.shape[0], 1)

    
    x_mu = np.mean(X, axis=0)
    x_mu_source = np.mean(Xs, axis=0)
    x_mu_target = np.mean(Xt, axis=0)
    
    ns = Xs.shape[0]
    nt = Xt.shape[0]
    n = X.shape[0]
    k = X.shape[1]
    ky = y.shape[1]
    
    
    # centering x's
    X_c = X - x_mu
    Xs_c = Xs - x_mu_source
    Xt_c = Xt - x_mu_target
    
    # cov matrices
    
    cov_Xs = (np.dot(Xs_c.T, Xs_c))/(ns-1)
    cov_Xt = (np.dot(Xt_c.T, Xt_c))/(nt-1)
    
    # setting the mean to which test samples should be recentered
    
    if mode == 0:       
        
        assert y.shape[0] == Xs.shape[0], "for unsupervised, X and Xs must be the same"
        
        x_mu_target_torecenter = np.mean(Xt, axis=0)
         
    elif mode == 1:
        
        x_mu_target_torecenter = np.mean(X, axis=0)
        
    elif mode == 2:
        
        x_mu_target_torecenter = np.mean(Xt, axis=0)
        
    
    
    b0 = np.mean(y,axis=0)
    
    y_c = y - b0 # centering y
      
    
    # store output matrices
    
    T = np.zeros((n, nlv))
    Ts = np.zeros((ns, nlv))
    Tt = np.zeros((nt, nlv))
    
    P = np.zeros((k, nlv))
    Ps = np.zeros((k, nlv))
    Pt = np.zeros((k, nlv))
    
    Wdi = np.zeros((k, nlv)) 
    
    Q = np.zeros((nlv,ky))
    
    for a in range(nlv):
        
        IXSXT = np.linalg.inv(np.eye(k) + lambda_*(1/2*np.dot(y_c.T,y_c))*(cov_Xs - cov_Xt))
        w = np.dot(np.dot(y_c.T,X_c)/np.dot(y_c.T,y_c),IXSXT).T
        w = w/np.sqrt(np.dot(w.T,w))        
        
        tt = np.dot(X_c,w)
        tts = np.dot(Xs_c,w)
        tt_t = np.dot(Xt_c,w)
        
        p = (1/np.dot(tt.T,tt))*np.dot(tt.T,X_c)
        ps = (1/np.dot(tts.T,tts))*np.dot(tts.T,Xs_c)
        pt = (1/np.dot(tt_t.T,tt_t))*np.dot(tt_t.T,Xt_c) 
        
        q = (1/np.dot(tt.T,tt))*np.dot(tt.T,y_c)
        
        # deflation
 
        X_c -= np.dot(tt,p)
        Xs_c -= np.dot(tts,ps)
        Xt_c -= np.dot(tt_t,pt)
        
        y_c -= q*tt
        
        T[:,a] = tt.flatten()
        Ts[:,a] = tts.flatten()
        Tt[:,a] = tt_t.flatten()
        
        P[:,a] = p.flatten()
        Ps[:,a] = ps.flatten()
        Pt[:,a] = pt.flatten()
        
        Wdi[:,a] = w.flatten()
        Q[a,:] = q.flatten()
        
        
    # loadings for X
    

 
    PWI = np.linalg.inv(np.dot(P.T, Wdi))

    R = np.dot(Wdi, PWI)
    
    B = np.dot(R,Q)
    
    beta = b0 - np.dot(x_mu_target_torecenter,B)
    
        
    return (B,beta,R,Q,x_mu_target_torecenter,b0)


