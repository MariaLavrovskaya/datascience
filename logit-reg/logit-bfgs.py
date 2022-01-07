class LogisticRegression(BaseEstimator):
    """ Logistic Regression classifier using Maximum Likelihood Estimation and BFGS optimisation algorithm. 
    
    This class implements logistic regression using Maximum Likeligood Estimation (MLE) and BFGS 
    optimisation algorithm. The guidance on BFGS algorithm is provided in Scipy library: 
    https://docs.scipy.org/doc/scipy/reference/optimize.minimize-bfgs.html
    
    Parameters
    ----------
    fit_intercept : bool, default=True
                    Specifies if a constant should be
                    added to the decision function. 
                    Note that the data matrix should contain ones as a first column for bias.
    max_iter : int, default=None
                Maximum number of iterations taken by the solver to converge 
    tol : float, default=None
          Tolerance for termination of the BFGS algorithm
    Attributes
    ----------
    classes_ : ndarray, shape (n_classes, )
               A list of class values known to the classifier 
    coef_ : ndarray, shape (1, n_features)
            Coefficient of the features in the logistic model, 
            where `n_features` is the number of features.

    intercept_ : ndarray, shape (1,)
        Intercept added to the logistic model.
    
    n_features_in : int
                    Number of features seen during `fit`
    
    References 
    ----------
    BFGS -- Nocedal, J, and S J Wright (2006). 
            Numerical Optimization. Springer New York.
            https://link.springer.com/book/10.1007/978-0-387-40065-5
            
    """
        #Tag to ensure that only the binary output is considered 
    def _more_tags(self):
        tags = super()._more_tags()
        tags['binary_only'] = True
        return tags
    def __init__(
        self,
        fit_intercept = True,
        max_iter = None, 
        tol = None
        ):
            self.fit_intercept = fit_intercept
            self.max_iter = max_iter
            self.tol = tol
        
    def _log_likelihood(self, _weights, X,y):
        """ Loglikelihood function specified for the Logistic regression. 
            The function is used for internal implementation 
            
        Parameters
        ----------
        X : {array-like}, shape (n_samples, n_features)
            The training input samples, where `n_samples` is the number of samples ad 
            `n_features` is the number of features
        y : ndarray, shape (n_samples,)
            Vector of targets
        _weights : np.ndarray, shape (n_features,)
                       Initial weights (starting point) for the beta parameters
        Returns 
        -------
        ll : float
             Value of log-likelihood function     
        """
        scores = safe_sparse_dot(X, _weights)
        ll = -np.sum( y*scores - np.log(1 + np.exp(scores)))
        return ll
        # Add the functionality to include value of the intercept and not 
    def fit(self, X,y):
        """ Fit the model based on the given training data.
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training vector, where `n_samples` is the number of samples and
            `n_features` is the number of features.
        y : array-like, shape (n_samples,)
            Vector of targets
        Returns
        -------
        self
            Fitted estimator.
        """
        X,y = check_X_y(X,y,accept_sparse=False,accept_large_sparse=False)
        if isspmatrix(X):
            return -1
        self.n_features_in = X.shape[1]
        # Variables for internal implementation 
        _weights=np.zeros(X.shape[1])
        #Attributes required by the sklearn interface
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        #Loglikelihood minimisation using BFGS method 
        intermediate = dict(minimize(self._log_likelihood, _weights, args = (X, y),method='BFGS'))
        self.coef_ = np.array([intermediate['x']])
        if self.fit_intercept:
            self.intercept_ = self.coef_[:, 0] 
            self.coef_ = self.coef_[:, 1:]
        else:
            self.intercept_ = np.zeros(n_classes)
        return self
    def predict_proba(self,X):
        """ Probability estimates. 
            The probability estimates are ordered by the label of classes in the ascending manner
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Matrix of samples to be scored. `n_samples` is the number of samples and
            `n_features` is the number of features.
        Returns 
        -------
        A : array-like, shape (n_samples, n_classes)
            Returns the probability for each sample for every class in the model,
            where the classes are order as they are present in self.classes_
        """
            # We check whether the estimator has been fitted
        check_is_fitted(self)
            # Input validation on an array
        X = check_array(X, accept_sparse=False, accept_large_sparse=False)
            # Checks for consistency 
        if isspmatrix(X):
            raise TypeError('The estimator does not support sparse input')
        if X.shape[1] != self.n_features_in:
            raise ValueError('Shape of input is different from what was seen in `fit`')
        score = safe_sparse_dot(X, np.concatenate((self.intercept_,self.coef_.ravel())).T, dense_output=True)
        score = score.ravel()
        score_2d = np.c_[-score, score]
        return softmax(score_2d)
    def predict(self, X):
        """ A reference implementation of a predicting function.
        Parameters
        ----------
        X : {array-like}, shape (n_samples, n_features)
            The training input samples.
        Returns
        -------
        y : ndarray, shape (n_samples,)
            Returns an array of ones.
        """
        # Check whether the estimator has been fitted 
        check_is_fitted(self) 
        # Input validation on an array
        X = check_array(X, accept_sparse=False, accept_large_sparse=False)
        # Checks for consistency
        if isspmatrix(X):
            raise TypeError('The estimator does not support sparse input')
        if X.shape[1] != self.n_features_in:
            raise ValueError('Shape of input is different from what was seen'
                             'in `fit`')
        n_classes = len(self.classes_)
        predicted_scores = safe_sparse_dot(X, np.concatenate((self.intercept_,self.coef_.ravel().T)), dense_output=True)
        predicted_scores = predicted_scores.ravel()
        if len(predicted_scores.shape) == 1: 
            indices = (predicted_scores > 0).astype(int)
        return self.classes_[indices]