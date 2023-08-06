import math
from scipy.stats import poisson

class Poisson:
    """Information pertaining to the poisson distribution.
    """
    def pdf(self, x, lam):
        """Probability density function for the poisson distribution. 

        Args:
            x (non-negaitve float or int): Value to return a probability for. 
            lam (non-negative float or int): The rate parameter of the poisson distribution.

        Returns:
            float: The probability of x in the poisson distribution with the provided lambda. 
        """
        self.x = x
        self.lam = lam

        try:
            if self.lam < 0:
                print("The rate must be positive")
                raise ValueError
            
            if self.x >= 0 and type(self.x) == int:
                pdf = (self.lam**(self.x)*math.exp(-self.lam))/math.factorial(self.x)
                return pdf 
           
            elif self.x < 0 and type(self.x) ==int:
                return 0
            
            elif type(self.x) != int:
                print("The domain of the Poisson distribution is discrete, non-integer values return 0")
                return 0
                
        except TypeError:
            print("The arguments passed should be numerical")

        
        

    
    def cdf(self, x, lam):
        """Cumulative distribution function for the poisson distribution. 
        Args:
            x (non-negaitve float or int): Value to return a probability for.  
            lam (non-negative float or int): The rate parameter of the poisson distribution.
        Returns:
            float: the probability that a number is less than or equal to x in the poisson distribution with the given lamda. 
        """
        self.x = x
        self.lam = lam

        

        try:
            if self.lam < 0:
                print("The rate must be positive")
                raise ValueError
            if self.x >= 0:
                cdf = 0
                x = math.floor(self.x)
                for i in range(0, x + 1):
                    cdf +=  Poisson.pdf(self, i, self.lam)
                return cdf
            else:
                return 0
        
        except TypeError:
            print("The arguments passed should be numerical")
        

       

    
    def quantile(self, p, lam):
        """Computes the value for the poisson distribution with parameter lambda corresponding to the given probability.

        Args:
            p (float): Number between 0 and 1 representing a probability.
            lam (non-negative float or int): The rate parameter of the poisson distribution.

        Returns:
            float: The value that yeild proability p for poisson distribution with parameter lambda.
        """
        self.p = p
        self.lam = lam
        
        try:
            if self.lam < 0:
                print("The rate must be positive")
                raise ValueError
            if 0 <= self.p <= 1:
                quantile = poisson.ppf(self.p, self.lam)
                return quantile
            else:
                print("The probability must be between 0 and 1")
        except TypeError:
            print("The arguments passed should be numerical")
        
