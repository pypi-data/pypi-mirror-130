import math
from scipy.stats import gamma
from scipy.special import gammainc
class Gamma:
    """Information pertaining to the gamma distribution.
    """
    def pdf(self, x, alpha, lam):
        """Probability density function for the gamma distribution. 

        Args:
            x (non-negaitve float or int): Value to return a probability for. 
            alpha (non-negative float or int): The shape parameter of the gamma distribution. 
            lam (non-negative float or int): The rate parameter of the gamma distribution (1/scale).

        Returns:
            float: The probability of x in the gamma distribution with the provided parameters. 
        """
        self.x = x
        self.lam = lam
        self.alpha = alpha


        try:
            if self.lam < 0 or self.alpha < 0:
                print("The rate and shape parameter must be positive")
                raise ValueError
            if self.x >= 0:
                pdf = ((self.x**(self.alpha - 1))*math.exp(-self.lam*self.x)*(self.lam**(self.alpha)))/math.gamma(self.alpha)
                return(pdf)
            else:
                return 0
        except TypeError:
            print("The arguments passed should be numerical")

    
    def cdf(self, x, alpha, lam):
        """Cumulative distribution function for the gamma distribution. 
       Args:
            x (non-negaitve float or int): Value to return a probability for. 
            alpha (non-negative float or int): The shape parameter of the gamma distribution. 
            lam (non-negative float or int): The rate parameter of the gamma distribution (1/scale).

        Returns:
            float: the probability that a number is less than or equal to x in the gamma distribution with the given parameters. 
        """
        self.x = x
        self.lam = lam
        self.alpha = alpha
        

        try:
            if self.lam < 0 or self.alpha < 0:
                print("The rate and shape parameter must be positive")
                raise ValueError
            if self.x > 0:
                cdf = gamma.cdf(self.x, self.alpha, scale = 1/self.lam)
                return cdf
            else:
                return 0
        except TypeError:
            print("The arguments passed should be numerical")
        

    
    def quantile(self, p, alpha, lam):
        """Computes the value for the gamma distribution with parameters alpha and lambda corresponding to the given probability.

        Args:
            p (float): Number between 0 and 1 representing a probability.
            alpha (non-negative float or int): The shape parameter of the gamma distribution. 
            lam (non-negative float or int): The rate parameter of the gamma distribution (1/scale).

        Returns:
            float: The value that yeild proability p for gamma distribution with parameters alpha and lam.
        """
        self.p = p
        self.lam = lam
        self.alpha = alpha
        
        
        try:
            if self.lam < 0 or self.alpha < 0:
                print("The rate and shape parameter must be positive")
                raise ValueError

            if 0 <= self.p <= 1:
                quantile = gamma.ppf(self.p, self.alpha, scale = 1/self.lam)
                return quantile
            else:
                print("The probability must be between 0 and 1")
                raise ValueError
        except TypeError:
            print("The arguments passed should be numerical")
