from scipy.stats import gamma, poisson
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .mle import calculate_mle

def hist(distribution, data):
    """Plots a histogram of empirical data and overlays a curve of the density function for the distribution passed as an argument
       where its parameters are estimated using MLE. Allows user to verify if the distribution chosen is well-suited for the data.

    Args:
        distribution (str): The name of the distribution to plot (only accepts "exponential", "gamma" or "poisson")
        data (list): List of observations
    """

    mle = calculate_mle(distribution, data)
    plt.hist(data, density = True, histtype = 'stepfilled', alpha=0.4, label = "empirical distribution")

    if distribution == 'exponential':
        x_values = np.linspace(gamma.ppf(q = 0.0001, a = 1, scale = 1/mle), gamma.ppf(q = 0.9999, a = 1, scale = 1/mle), num = 1000)
        plt.plot(x_values, gamma.pdf(x_values, 1, scale = 1/mle), 'r-', lw = 3, alpha = 0.6, label = f'exponential pdf with MLE = {mle:0.2}')
        plt.legend(loc = 'best', frameon = True)
    
    elif distribution == 'gamma':
        x_values = np.linspace(gamma.ppf(q = 0.0001, a = mle[0], scale = 1/mle[1]), gamma.ppf(q = 0.9999, a = mle[0], scale = 1/mle[1]), num = 1000)
        plt.plot(x_values, gamma.pdf(x_values, a = mle[0], scale = 1/mle[1]), 'r-', lw = 3, alpha = 0.6, label = f'gamma pdf \n MLE_alpha = {mle[0]:0.2} \n MLE_lambda = {mle[1]:0.2}')
        plt.legend(loc = 'best', frameon = True)
    
    elif distribution == 'poisson':
        x_values = np.arange(min(data), max(data), 1)
        plt.plot(x_values, poisson.pmf(x_values, mu = mle), 'r-', lw = 3, alpha = 0.6, label = f'poisson pmf with MLE = {mle:0.2}')
        plt.legend(loc = 'best', frameon = True)
        
    return x_values

def qqplot(distribution, data):
    """Produces a QQ-plot of the quantiles for the distribution passed as an argument where its parameters are estimated using MLE
       versus the quantiles of the empirical data. Allows user to verify if the distribution chosen is well-suited for the data.

    Args:
        distribution (str): The name of the distribution to plot (only accepts "exponential", "gamma" or "poisson")
        data (list): List of observations
    """
    fig = plt.figure()
    ax = fig.add_subplot()
    mle = calculate_mle(distribution, data)

    if distribution == 'gamma':
        p = stats.probplot(data, sparams = (mle[0], 0, mle[1]), dist='gamma', plot = plt) 
        ax.set_title(f"QQ - Plot for gamma dist with shape parameter {mle[0]:0.2} and scale parameter 1/{mle[1]:0.2}")
    
    elif distribution == 'exponential':
        p = stats.probplot(data, sparams = (mle, ), dist='expon', plot = plt) 
        ax.set_title(f"QQ - Plot for exponential dist with rate parameter {mle:0.2}")
    
    else:
        p = stats.probplot(data, sparams = (mle, ), dist='poisson', plot = plt) 
        ax.set_title(f"QQ - Plot for poisson dist with rate parameter {mle:0.2}")

    return p

def boxplot(data): 
    """Produces a box-and-whisker plot 

    Args:
        data (list or DataFrame): Values to be plotted
    """
    data = pd.DataFrame(data)
    return data.boxplot(grid = False, return_type = 'dict')