from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as pl
from scipy import stats

from scipy.stats import ecdf

data =  np.linspace(20, 80, 500)
poisson= np.arange(0, 15)
binom = np.arange(0,13)
mean,std = data.mean() , data.std()
Cdf_norm=  stats.norm.cdf(14, mean , std)
#Cdf_poisson = stats.poisson.cdf(poisson)
#Cdf_binom = stats.binom.cdf(binom)
pmf_norm=  stats.norm.pdf(data)
#pmf_poisson = stats.poisson.pmf(poisson)
#pmf_binom = stats.binom.pmf(binom)
print(Cdf_norm)