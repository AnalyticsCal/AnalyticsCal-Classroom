import math					
import matplotlib.pyplot as plt					
					
x1=[0,542.05,0,1315.46,1000.23,22177.74,15505.73,23640.93,27892.92,28754.33,38558.51,20229.59,44069.95,28663.76,46014.02,46426.07,55493.95,63408.86,61136.38,61994.48,65605.48,66051.52,72107.6,75328.87,64664.71,77044.01,67532.53,73994.56,78389.47,76253.86,86419.7,91749.16,94657.16,78013.11,114523.61,119943.24,91992.39,93863.75,100671.96,101913.08,123334.88,120542.52,130298.13,134615.46,131876.9,142107.34,144372.41,153441.51,162597.7,165349.2]					
y=	[14681.4,35673.41,42559.73,49490.75,64926.08,65200.33,69758.98,71498.49,77798.83,78239.91,81005.76,81229.06,89949.14,90708.19,96479.51,96712.8,96778.92,97427.84,97483.56,99937.59,101004.64,103282.38,105008.31,105733.54,107404.34,108552.04,108733.99,110352.25,111313.02,118474.03,122776.86,124266.9,125370.37,126992.93,129917.04,132602.65,134307.35,141585.52,144259.4,146121.95,149759.96,152211.77,155752.6,156122.51,156991.12,166187.94,182901.99,191050.39,191792.06,192261.83] 				
					
n=len(x1)					
print("count of data is: ",n)					
sum_x1=sum(x1)					
sum_y=sum(y)					
					
#sum of x1*y					
x1y = [x1[i]*y[i] for i in range(len(x1))]					
#print(x1y)					
sum_x1y=sum(x1y)					
#print("sum of x1*y: ",sum_x1y)					
					
#n* sum of x1 y					
nx1y=n*sum_x1y					
#print(nx1y)					
					
#sum of x1* sum of y					
Ex1Ey=sum_x1*sum_y					
#print(Ex1Ey)					
					
#sum of sqaures of x1					
SS_x1 = sum(map(lambda i : i * i, x1)) 					
#print ("The sum of squares of list is : " + str(SS_x1)) 					
#n* sum of x1^2					
nSSx1=n*SS_x1					
#print(nSSx1)					
					
					
#(sum of x1)^2					
S_x1=sum_x1*sum_x1					
#print(S_x1)					
					
#print("sum of sum_x1: ", sum_x1)					
#print("sum of sum_y: ", sum_y)					
					
n=len(x1)					
print("count of data: ",n)					
					
mean_x1 = sum(x1) / len(x1)					
mean_y = sum(y) / len(y) 					
					
print("Mean of x1 is : " + str(mean_x1)) 					
print("Mean of y is : " + str(mean_y)) 					
					
#calculating cross deviation 					
SS_x1y = nx1y-Ex1Ey					
#print(SS_x1y)					
SS_x1x1 = nSSx1-S_x1					
#print(SS_x1x1)					
					
m=SS_x1y/SS_x1x1					
print("X Variable 1: ",m)					
					
#m*sum of x1					
mEx1=m*sum_x1					
#print(mEx1)					
					
nmrtr=sum_y-mEx1 #nmrtr=numerator					
#print(nmrtr)					
					
c=nmrtr/n					
print("Intercept: ",c)					
					
#so the regression line for x1 and y is					
					
					
print("Best fit line:")					
print("y = "+str(m)+"x1"+str(c))					
					
#testing of regression equation					
#x = float(input("Enter a value to calculate: "))					
#print("y = "+str(m*x+c))					
					
					
						
				
#correlation coefficient					
					
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
X = x1					
Y = y					
					
# Find the size of array. 					
n = len(X) 					
					
# Function call to correlationCoefficient. 					
print ('Correlation Coefficient between x1 & y is ','{0:.6f}'.format(correlationCoefficient(X, Y, n))) 					
var_x1  = sum(pow(x-mean_x1,2) for x in x1) / len(x1)					
print("variance of x1 is : " + str(var_x1))					
					
std_x1  = math.sqrt(var_x1)					
print("SD of x1 is : " + str(std_x1)) 					
var_y  = sum(pow(x-mean_y,2) for x in y) / len(y)					
std_y  = math.sqrt(var_y)					
print("SD of y is : " + str(std_y)) 					
					
#covariance(x1, y)					

#x1 bar and y bar
x1_bar=	sum_x1/n
y_bar=	sum_y/n

#print(x1_bar)	
#print(y_bar)	

x1x_bar = [x1[i]-x1_bar for i in range(len(x1))]
#print(x1x_bar)
sum_x1x_bar=sum(x1x_bar)
#print(sum_x1x_bar)

yy_bar=[y[i]-y_bar for i in range(len(y))]
#print(yy_bar)
sum_yy_bar=sum(yy_bar)
#print(sum_yy_bar)

z = [x1x_bar[i]*yy_bar[i] for i in range(len(x1x_bar))]
#print(z)
sum_z=sum(z)
#print(sum_z)

cov=sum_z/n
print("coveriance between x1 & y is: ",cov)
    
