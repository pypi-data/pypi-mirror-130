[![Build Status](https://app.travis-ci.com/SaraAnnHall/533Lab4_SaraJustine.svg?token=fCRD5ox8wxGuFNwfs8Ju&branch=main)](https://app.travis-ci.com/SaraAnnHall/533Lab4_SaraJustine)

# Package (probability) 
Contains functionality relating to the gamma, exponential, and poisson distributions. This includes things like visualization, probability density functions, cumulative distribution functions, and parameter estimation via maximum likelihood. This functionality is split up into two subpackages - distributions and estimation. 
## Subpackage 1 (distributions)
### Module 1 (poisson)
This module contains 3 different methods that allow us to find the probability density function, the cumulative distribution function and the quantiles of a Poisson distribution. 

**pdf(self, x, lam):** This method calculates the probability density function using the formula for the Poisson probability mass function which is :

$$p(x;\lambda) = \frac{\lambda^{x} e^{-\lambda}}{x!}$$

When using this method, the user has to specify the value of ‘x’ as well as the rate parameter.

This method also tests the user’s inputs and ensures that they are suitable (ex: rate greater than 0, x must be a non-negative integer).

**cdf(self, x, lam):** This method calculates the cumulative distribution function for a Poisson distribution. The fact that the Poisson distribution is discrete enabled us to use the following property: 

$$F_x(x) = Pr(X \le x) = \sum_{x_i \le x}p(x_i)$$

Also, because the Poisson distribution is discrete, we know that the probability that it takes on a non-integer value is 0. For example, this means that $$Pr(X \le 2.4) = Pr(X \le 2)$$. This is why we used `x = math.floor(self.x)`. It rounds down the value of x inputted by the user. 
to the nearest integer. 

This method also tests the user’s inputs and ensures that they are suitable (ex: rate greater than 0).

**quantile(self, p, lam):** This method calculates the quantile distribution of a Poisson distribution. The ppf method from the poisson module imported from the scipy.stats package was used for simplicity. We did include additional tests to ensure that the user inputs were valid (rate greater than 0, probability between 0 and 1, numerical arguments).

### Module 2 (gamma)
This module contains 3 different methods that allow us to find the probability density function, the cumulative distribution function and the quantiles of the gamma distribution. 

**pdf(self, x, alpha, lam):** This method calculates the probability density function using the formula for the Poisson probability mass function which is :

$$p(x;\alpha, \lambda) = \frac{x^{\alpha-1}e^{-\lambda x}\lambda^\alpha}{\Gamma(\alpha)}$$

We had to use the `math.gamma` method for the denominator of this formula.

This method also tests the user’s inputs and ensures that they are suitable (ex: rate and shape greater than 0).

**cdf(self, x, alpha, lam):** This method calculates the cumulative distribution function for a Gamma distribution. There is no closed form for this, we thus resulted in using the `gamma.cdf` method from the scipy.stats package.

We did include additional tests to ensure that the user inputs were valid (rate and shape parameter greater than 0, numerical arguments).

**quantile(self, p, lam):** This method calculates the quantile distribution for a Gamma distribution. The ppf method from the gamma module imported from the `scipy.stats` package was used because once again, there is no mathematical closed form for this. We did include additional tests to ensure that the user inputs were valid (rate and shape greater than 0, probability between 0 and 1, numerical arguments).

### Module 3 (exponential)
This module contains 3 different methods that allow us to find the probability density function, the cumulative distribution function and the quantiles of the exponential distribution. 

For this module we used inheritance. We were able to use the relationship between the gamma distribution and the exponential distribution (the exponential distribution is simply a gamma distribution with shape parameter $$\alpha = 1$$) to write all the methods using the ones written for the gamma distribution. We simply had to specify that our shape parameter was 1.
## Subpackage 2 (estimation)
Contains modules designed to help explore how actual data fits with the three distributions (gamma, exponential, and poisson). These include calculating the maximum likelihood estimations (MLE) for provided data given one of the distributions, plotting the data along with the distributions, and displaying some summary statistics about the provided data. 
### Module 1 (mle)
Contains functions to read a single column of data from a csv file, select a distribution, and calculate the MLE parameter estimates of the selected distribution and provided data. 

**readdata(file):** Reads a single numerical column of data from a csv file, indicated by the input argument file path using panda’s read.csv function. If there is more than one column, or values are not numerical or are negative, an error is thrown (since these can’t be a part of exponential/gamma/poisson distributed data). Otherwise, the data is returned as a list. 

**setDistibution(distribution):** Takes a string input (all lower case) and verifies that it is one of the 3 possible distributions. Then returns the associated integer value (stored in a dictionary) for that distribution (1 = exponential, 2 = gamma, and 3 = poisson). If the distribution is not one of the three possible distributions, then an error is thrown. 

**calulate_mle(distribution, data):** Takes a lower case string to indicate the distribution and a list of data (ideally created with the readdata() function) as parameters. Uses the setDistribution() function to verify that the distribution is acceptable, and get the integer representation. If the data provided is an empty list, then an error is thrown. If...Else clauses are then used to calculate the MLE depending on the distribution. For exponential, MLE for lambda is returned as 1 over the mean of the data. For exponential, MLE for lambda is returned as the mean of the data. For gamma, since there are two parameters and it does not have a closed form probability density function, the scipy.stats function is used to get the estimates for rate and shape parameters, which are returned in a list with shape in the first position and rate in the second. 
### Module 2 (plot)
Contains functions to show how well the estimated distributions found with the mle module match the actual provided data. 

**hist(distribution, data):** Takes a lower case string to indicate the distribution and a list of data (ideally created with the mle.readdata() function) as parameters. The function mle.calculate_mle() is used to get parameter estimates, then histograms of the data are made with the pdf for the distribution using the estimated parameters overlaid. These pdf’s are retrieved using the scipy.stats package. 

**qqplot(distribution, data):** Takes a lower case string to indicate the distribution and a list of data (ideally created with the mle.readdata() function) as parameters. The function mle.calculate_mle() is used to get parameter estimates and a qqplot is made for the data and the estimated distribution using the scipy.stats.probplot function. 

**boxplot(data):** Takes a list of data (ideally created with the mle.readdata() function) as a parameter, and employs the pandas dataframe boxplot function to create a boxplot of the data with no grid displayed in the background. 
### Module 3 (summary)
Contains functions to compute some summary information about a list of data (ideally created with the mle.readdata() function). 

**summary(data):**  Takes a list of data (ideally created with the mle.readdata() function) as a parameter, and prints the minimum and maximum values, the variance, and the mean. Uses the Python statistics package. 

**contains_all_ints(data):** Takes a list of data (ideally created with the mle.readdata() function), and returns whether it is entirely composed of integers by iterating through the list and returning false if there is a non-integer, and true otherwise. 

**is_non_negative(data):** Takes a list of data (ideally created with the mle.readdata() function), and returns whether it is entirely composed of non-negative values by iterating through the list and returning false if there is a negative element, and true otherwise. 
