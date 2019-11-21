import stats_team3 as st
import data_load as load
import file_upload as upload
from nonlinear_regression import NonLinearRegression as nlr

import math
from collections import namedtuple
class IndivModel:
    def __init__(self, values):
        self.values = values
        
    def mean(self):
        self.mean = st.mean(self.values)
        return self.mean
    def var(self):
        self.var = st.variance(self.values)
        return self.var
"""
a = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
b = [9.0, 8.0, 9.0, 12.0, 9.0, 12.0, 11.0, 7.0, 13.0, 9.0, 11.0, 10.0]

x = IndivModel(a)
y = IndivModel(b)
"""
class BiDataModel(IndivModel):

    def __init__(self,x, y):
       super(IndivModel, self).__init__()  # calls Base.__init__
       self.x = x
       self.y = y

    #global x_bar, y_bar
    def x_bar(self):
    #    global x_bar
        self.x_bar = x.mean
     #   x_bar = self.x_bar
        return self.x_bar
        #return self.x_bar

    def y_bar(self):
     #   global y_bar
        self.y_bar = y.mean
      #  y_bar = self.y_bar
        return self.y_bar

    def x_var(self):
        self.x_var = x.var
        return self.x_var

    def y_var(self):
        self.y_var = y.var
        return self.y_var

    def cov(self):
        self.cov = st.covariance(self.x.values,self.x_bar(), self.y.values, self.y_bar())
        return self.cov

    def corr_coeff(self):
        self.corr_coeff = st.correlationCoefficient(self.x.values,self.y.values)
        self.threshold = 1.96/ math.sqrt(len(self.x.values))
        return self.corr_coeff

    def nlr_coef(self):
        self.poly_coeff = []
        self.exp_coeff = []
        self.sin_coeff = []

    def anova(self):
        self.msr = None
        self.mse = None
        self.ssr = None
        self.sse = None
        self.f = None
        self.p = None
        self.model_confidence = None
        self.t_m=None
        self.t_c=None
        

    def models(self):
        self.linear = {'eqn' : '','msr': None, 'mse': None,'ssr':None, 'sse': None,'f':None,'p':None}
        self.poly_2 = {'eqn' : '','msr': None, 'mse': None,'ssr':None, 'sse': None,'f':None,'p':None}
        self.poly_3 = {'eqn' : '','msr': None, 'mse': None,'ssr':None, 'sse': None,'f':None,'p':None}
        self.poly_4 = {'eqn' : '','msr': None, 'mse': None,'ssr':None, 'sse': None,'f':None,'p':None}        
       

"""
    def nlr_coeff(self):
        self.nlr_coeff = 
    def anova(self):
        ...
"""
#t = DataModel(x, y)
"""
x = [[5.94, 6.00, 6.08, 6.17, 6.14, 6.09, 5.87, 5.84, 5.99, 6.12, 6.42, 6.48, 6.52, 6.64, 6.75, 6.73, 6.89, 6.98, 6.98, 7.1, 7.19, 7.29, 7.65, 7.75, 7.72, 7.67, 7.66, 7.89, 8.14, 8.21, 8.05, 7.94, 7.88, 7.79, 7.41, 7.18, 7.15, 7.27, 7.37, 7.54, 7.58, 7.62, 7.58, 7.48, 7.35, 7.19, 7.19, 7.11, 7.16, 7.22, 7.36, 7.34, 7.30],
     [5.31, 5.6, 5.49, 5.8, 5.61, 5.28, 5.19, 5.18, 5.3, 5.23, 5.64, 5.62, 5.67, 5.83, 5.53, 5.76, 6.09, 6.52, 6.68, 7.07, 7.12, 7.25, 7.85, 8.02, 7.87, 7.14, 7.2, 7.59, 7.74, 7.51, 7.46, 7.09, 6.82, 6.22, 5.61, 5.48, 4.78, 4.14, 4.64, 5.52, 5.95, 6.20, 6.03, 5.6, 5.26, 4.96, 5.28, 5.37, 5.53, 5.72, 6.04, 5.66, 5.75],
     [0.29, -0.11, 0.31, -0.19, -0.33, -0.09, -0.01, 0.12, -0.07, 0.41, -0.02, 0.05, 0.16, -0.3, 0.23, 0.33, 0.43, 0.16, 0.39, 0.05, 0.13, 0.6, 0.17, -0.15, -0.73, 0.06, 0.39, 0.15, -0.23, -0.05, -0.37, -0.27, -0.6, -0.61, -0.13, -0.7, -0.64, 0.5, 0.88, 0.43, 0.25, -0.17, -0.43, -0.34, -0.3, 0.32, 0.09, 0.16, 0.19, 0.32, -0.38, 0.09, 0.07]]

Y = [1.146,-2.443,1.497,-0.132,2.025,0.737,-1.023,-0.956,0.385,0.983,5.092,3.649,2.703,-0.271,2.055,-0.714,0.653,-0.034,-1.058,-2.051,1.451,-0.989,1.358,0.746,1.855,-1.894,0.781,-0.161,2.233,2.425,2.169,0.982,4.708,6.063,9.382,9.304,10.69,6.531,7.873,3.882,4.96,1.301,1.154,0.116,4.928,2.53,8.425,5.291,5.192,0.257,4.402,3.173,5.104,]
"""
class MultiDataModel():
    def __init__(self,x, y):
        self.x = x
        self.y = y

    def x_stats(self):
        self.no_of_indep_var = len(self.x)
        self.x_mean = [st.mean(i) for i in self.x]
        self.x_var = [st.variance(i) for i in self.x]
        self.x_std_dev = [math.sqrt(st.variance(i)) for i in self.x]

    def y_stats(self):
        self.y_mean = st.mean(self.y)
        self.y_var = st.variance(self.y)
        self.y_std_dev = math.sqrt(st.variance(self.y))

    def linear_regression_coeff(self):
        self.lin_reg_coeff = []

    def anova(self):
        self.msr = None
        self.mse = None
        self.ssr = None
        self.sse = None
        self.f = None
        self.p = None
        self.model_confidence = None
        
        
        

    
    
