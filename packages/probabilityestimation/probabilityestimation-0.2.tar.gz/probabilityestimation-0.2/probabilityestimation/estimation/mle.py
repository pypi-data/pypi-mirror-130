import pandas as pd
import numpy as np
import statistics
from scipy.stats import gamma

class InvalidDataError(Exception):
    pass

def readData(file):
    """ reads a comma-separated values (csv) file with only one column where all values are non-negative
        
    Args:
        file (str): Any valid string path to file

    Returns:
        list: List containing the values from the comma-sperated values (csv) file
    """
    import pandas as pd
    try:
        data = pd.read_csv(file)
    except:
        raise InvalidDataError

    if len(data.columns) != 1:
        raise ValueError("Data file must only have one column of data.")
    else:
        data =data.iloc[:, 0].tolist()

    for i in data:
        if (type(i)!=int and type(i)!=float) or i < 0 :
            raise ValueError("For poisson, gamma, and exponential distributions your response data must be numerical and non-negative.")
    return data

def setDistribution(distribution):
    """checks if the distribution passed as an argument is exponential, gamma or poisson

    Args:
        distribution (str): The name of the distribution to be checked 

    Returns:
        int: The integer corresponding to the distribution passed as an argument 
                1 : "exponential"
                2 : "gamma"
                3: "poisson"
    """
    distributions = {'exponential':1, 'gamma':2, 'poisson':3}
    try:
        distribution = distributions[distribution]
        return distribution
    except:
        raise ValueError("You must provide one of the three possible distributions: exponential, gamma, or poisson")

def calculate_mle(distribution, data):
    """calculates the maximum likelihood estimatation of the parameters for a specific distribution given observations

    Args:
        distribution (str): The name of the distribution for which MLE is used to estimate its parameters
                            (only accepts "exponential", "gamma" or "poisson")
        data (list): List of observations

    Returns:
        float or list: returns the maximum likelihood estimates. A list is returned when the distribution 
                       has more than one parameter to estimate. 
    """
    
    distribution = setDistribution(distribution)
    
    # Make sure there is sufficient information to actually calculate the MLE. 
    if len(data) == 0:
        raise ValueError("insufficient info to compute mle.")

    #For exponential, the MLE is one over the mean of the data. 
    if distribution == 1:
        return 1/statistics.mean(data)

    #For gamma, MLE is more complicated so I'm just using scipy gamma.fit - uses MLE by default.
    #In this case, it returns shape in the first position and 1/scale (lambda) in the second). 
    elif distribution == 2:
        x = pd.Series(data)
        params = gamma.fit(x)
        return [params[0], 1/params[2]]
    # For Poisson, MLE for lambda is the mean of the data. 
    else:
        for i in data:
            if type(i) != int:
                raise ValueError("Poisson data must be discrete (non-negative integers)")
            else:
                return statistics.mean(data)