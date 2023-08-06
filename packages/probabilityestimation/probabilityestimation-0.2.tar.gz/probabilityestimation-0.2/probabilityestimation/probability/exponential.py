import math
from .gamma import Gamma
class Exponential(Gamma):
    """Information pertaining to the exponential distribution. Inherits from gamma since it is a special case of gamma with alpha = 1. 
    """
    def pdf(self, x, lam):
        """Probability density function for the exponential distribution. 

        Args:
        x (non-negaitve float or int): Value to return a probability for. 
        lam (non-negative float or int): The rate parameter of the gamma distribution (1/scale).

        Returns:
            float: The probability of x in the exponential distribution with the provided lambda. 
        """
        return Gamma.pdf(self, x, 1, lam)
    
    def cdf(self, x, lam):
        """Cumulative distribution function for the gamma distribution. 
       Args:
            x (non-negaitve float or int): Value to return a probability for.  
            lam (non-negative float or int): The rate parameter of the gamma distribution (1/scale).

        Returns:
            float: the probability that a number is less than or equal to x in the exponential distribution with the given lamda. 
        """
        return Gamma.cdf(self, x, 1, lam)
    
    def quantile(self, p, lam):
        """Computes the value for the exponential distribution with parameter lambda corresponding to the given probability.

        Args:
            p (float): Number between 0 and 1 representing a probability.
            lam (non-negative float or int): The rate parameter of the exponential distribution (1/scale).

        Returns:
            float: The value that yeild proability p for exponential distribution with parameter lambda.
        """
        return Gamma.quantile(self, p, 1, lam)
        