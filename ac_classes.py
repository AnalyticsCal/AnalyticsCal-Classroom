import stats_team3 as st
import data_load as load
import file_upload as upload
from nonlinear_regression import NonLinearRegression as nlr
import math

class IndivModel:
    def __init__(self, values):
        self.values = values
        
    def mean(self):
        self.mean = st.mean(self.values)
        return self.mean
    def var(self):
        self.var = st.variance(self.values, self.mean)
        return self.var
#"""
a = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
b = [9.0, 8.0, 9.0, 12.0, 9.0, 12.0, 11.0, 7.0, 13.0, 9.0, 11.0, 10.0]

x = IndivModel(a)
y = IndivModel(b)
#"""
class DataModel(IndivModel):

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
        
        
       

"""
    def nlr_coeff(self):
        self.nlr_coeff = 
    def anova(self):
        ...
"""
t = DataModel(x, y)

