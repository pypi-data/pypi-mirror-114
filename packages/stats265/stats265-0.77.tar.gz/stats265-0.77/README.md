# stats265 package
A pip package which will hopefully have all the distributions from STATS265(Stats 1) - Ualberta soon


Currently:
* Bernoulli
* Binomial
* Gaussian (Normal)
* Poisson



If you are risk averse, you can try it out on a virtual environment first
* https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
* https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv-win.html


Testing was done using unittest library https://docs.python.org/3/library/unittest.html

# Documentation:
    * Calling a distribution
        * from stats265 import Bernoulli
            * g = Bernolli(p = 0.7)
        * from stats265 import Gaussian
            * g = Gaussian(mean, stdev)
        * from stats265 import Binomial
            * g = Binomial(p = 0.7, n = 20)
        * from stats265 import Poisson
            * g = Poisson(mean)

    * Methods of distributions (varies for obvious reasons)
        * read_data_file(file_name)
            reads the data in said file into our object, and now we can play around with the data

        * calculate_mean()
            calculates and returns the mean
            
        * calculate_stdev()
            calculates and returns the standard deviation of the distribution

        * plot_histogram()
            plots a histogram of the data

        * pdf(x)
            returns probability density function for a value x

        * plot_histogram_pdf()
            Plots histogram of data and pdf

        * Distribution_1 + Distribution_2 (__add__)
            Add a two distributions
                same type only for now

        * print(Distribution) (__repr__)
            Allows for representation on a print call
    


# Installation and Dependencies:
* Installation:
    * pip install stats265
 
* Dependencies:
    * Matplotlib:
        * pip install matplotlib

