

# Estimate Mean and Variance
import math
from math import sqrt
import matplotlib.pyplot as plt			



#dataset
dataset = [[165349.2,192261.83],[162597.7,191792.06],[153441.51,191050.39],[144372.41,182901.99],[142107.34,166187.94],[131876.9,156991.12],[134615.46,156122.51],[130298.13,155752.6],[120542.52,152211.77],[123334.88,149759.96],[101913.08,146121.95],[100671.96,144259.4],[93863.75,141585.52],[91992.39,134307.35],[119943.24,132602.65],[114523.61,129917.04],[78013.11,126992.93],[94657.16,125370.37],[91749.16,124266.9],[86419.7,122776.86],[76253.86,118474.03],[78389.47,111313.02],[73994.56,110352.25],[67532.53,108733.99],[77044.01,108552.04],[64664.71,107404.34],[75328.87,105733.54],[72107.6,105008.31],[66051.52,103282.38],[65605.48,101004.64],[61994.48,99937.59],[61136.38,97483.56],[63408.86,97427.84],[55493.95,96778.92],[46426.07,96712.8],[46014.02,96479.51],[28663.76,90708.19],[44069.95,89949.14],[20229.59,81229.06],[38558.51,81005.76],[28754.33,78239.91],[27892.92,77798.83],[23640.93,71498.49],[15505.73,69758.98],[22177.74,65200.33],[1000.23,64926.08],[1315.46,49490.75],[0,42559.73],[542.05,35673.41],[0,14681.4]]
x = [row[0] for row in dataset]
y = [row[1] for row in dataset]
# Load a CSV file
n=len(x)

#print(y)
        
def mean(values):
	return sum(values) / float(len(values))
mean_x=mean(x)
mean_y=mean(y)
#print("mean of x: ",mean_x)
#print("mean of y: ",mean_y)


def variance(values, mean):
    return sum([(x - mean) ** 2 for x in values]) / (n - 1)# n - 1: is used as sample data points are considered


mean_x, mean_y = mean(x), mean(y)
var_x, var_y = variance(x, mean_x), variance(y, mean_y)



# Calculate Covariance

# Calculate covariance between x and y
def covariance(x, mean_x, y, mean_y):
	covar = 0.0
	for i in range(len(x)):
		covar += (x[i] - mean_x) * (y[i] - mean_y)
	return covar / n - 1

mean_x, mean_y = mean(x), mean(y)
covar = covariance(x, mean_x, y, mean_y)




# Calculate coefficients
def coefficients(dataset):
	x_mean, y_mean = mean(x), mean(y)
	b1 = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
	b0 = y_mean - b1 * x_mean
	return [b0, b1]
b0, b1 = coefficients(dataset)





def simple_linear_regression(train, test):
	predictions = list()
	b0, b1 = coefficients(train)
	for row in test:
		yhat = b0 + b1 * row[0]
		predictions.append(yhat)
	return predictions
	   #"%.2f" defines the decimal place	

# Calculate root mean squared error
def rmse_metric(actual, predicted_y):
	sum_error = 0.0
	for i in range(len(actual)):
		prediction_error = predicted_y[i] - actual[i]
		sum_error += (prediction_error ** 2)
	mean_error = sum_error / float(len(actual))
	return sqrt(mean_error)
 
    
# Evaluate regression algorithm on training dataset
def evaluate_algorithm(dataset, algorithm):
	test_set = list()
	for row in dataset:
		row_copy = list(row)
		row_copy[-1] = None
		test_set.append(row_copy)
	predicted_y = algorithm(dataset, test_set)

	print("Predicted Line for given dataset is:y_hat ", "\n",(predicted_y))  #imp dont delete
	actual = [row[-1] for row in dataset]
	rmse = rmse_metric(actual, predicted_y)
	return rmse



rmse = evaluate_algorithm(dataset, simple_linear_regression)


  

#correlationCoefficient
def correlationCoefficient(X, Y, n) : 					
	sum_X = 0				
	sum_Y = 0				
	sum_XY = 0				
	squareSum_X = 0				
	squareSum_Y = 0				
						
	i = 0				
	while i < n : 				
		# sum of elements of array X. 			
		sum_X = sum_X + X[i] 			
					
		# sum of elements of array Y. 			
		sum_Y = sum_Y + Y[i] 			
					
		# sum of X[i] * Y[i]. 			
		sum_XY = sum_XY + X[i] * Y[i] 			
					
		# sum of square of array elements. 			
		squareSum_X = squareSum_X + X[i] * X[i] 			
		squareSum_Y = squareSum_Y + Y[i] * Y[i] 			
					
		i = i + 1			
					
	# use formula for calculating correlation coefficient. 				
	corr = (float)(n * sum_XY - sum_X * sum_Y)/(float)(math.sqrt((n * squareSum_X - sum_X * sum_X)* (n * squareSum_Y - sum_Y * sum_Y))) 				
	return corr 				
					
# Driver function 					
X = x				
Y = y					
					
# Find the size of array. 					
n = len(X) 					
					
			
print("number of observation: ",n)
print("mean of x: ", "%.2f"% mean_x, "mean of y: ", "%.2f"% mean_y)
print("variance of x: ", "%.2f"% var_x , "variance of y: ","%.2f"% var_y)
print("SD of x: ", "%.2f"% sqrt(var_x), "SD of y: ", "%.2f"% sqrt(var_y))
print("covariance of x & y: ", "%.2f"% covar)
print("b0: ","%.2f"% b0, "b1: ", "%.2f"% b1)
print("Best fit line:")					
print("y = ""%.2f"% +(b1)+"*x+"+"%.2f"% (b0))
print('RMSE: %.3f' % (rmse))
print ('Correlation Coefficient between x & y is ','{0:.6f}'.format(correlationCoefficient(X, Y, n)))


plt.scatter(x, y, s=50, alpha=1)					
plt.title('Scatter plot of predicted_y & y')					
plt.xlabel('predicted_y')					
plt.ylabel('y')					
plt.show()		

#===================================================================
"""
print("number of observation: ",n)
print("mean of x: ", "%.2f"% mean_x, "mean of y: ", "%.2f"% mean_y)
print("variance of x: ", "%.2f"% (var_x/n), "variance of y: ","%.2f"% (var_y/n-1))
print("SD of x: ", "%.2f"% sqrt(var_x/n), "SD of y: ", "%.2f"% sqrt(var_y/n-1))
print("covariance of x & y: ", covar/n-1)
print("b0: ","%.2f"% b0, "b1: ", "%.2f"% b1)
print("Best fit line:")					
print("y = ""%.2f"% +(b1)+"*x+"+"%.2f"% (b0))
print('RMSE: %.3f' % (rmse))
print ('Correlation Coefficient between x & y is ','{0:.6f}'.format(correlationCoefficient(X, Y, n)))
"""
#====================================================================



