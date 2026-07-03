from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as pl
from scipy import stats
y_axos = np.linspace(0,1,500)
data =  np.linspace(20, 80, 500)
poisson= np.arange(0, 15)
binom = np.arange(0,13)
mean,std = data.mean() , data.std()
Cdf_norm=  stats.norm.cdf(data, mean , std)
#Cdf_poisson = stats.poisson.cdf(poisson)
#Cdf_binom = stats.binom.cdf(binom)
pmf_norm=  stats.norm.pdf(data,mean,std)
pmf_poisson = stats.poisson.pmf(5, poisson.mean())
#pmf_binom = stats.binom.pmf(binom)

