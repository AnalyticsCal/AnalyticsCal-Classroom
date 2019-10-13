## Module Structure

    - nonlinear_regression.py
    - linear_algebra.py
    - gauss_newton.py
    - main.py 
    
- nonlinear_regression.py :
Module contain a class NonLinearRegression which has method for each type of nonlinear_regression.
Currently we support following kinds of non linear model.

#####1. Polynomial Model 
    - Equation: B0+B1*X+B2*X^2+B3*X^3 + -- + --
    - Any order of polynomial regression can be performed.
#####2. Sinusoidal Model 
    - Equation: B0 * Sin(B1*X+B2)+B3 . 
    - Order for this regression is fixed to 4.
#####3. Exponential Model
    - Equation: B0 * (1-exp^B1x) . 
    - Order for this regression is fixed to 2

- linear_algebra.py : This module has all Matrix related operations such as finding inverse, tranpose, multiplication etc operations of matrix.
    -   Used internally by nonlinear_regression.py 

- gauss_newton.py : This has the implementation for least square gauss newton method.
     -   Used for implementing sinusoidal and exponential regression.

- main.py : This module shows example of how to use the nonlinear_regression.py to perform the listed regression. main.py can be ignored when project is integrated with other modules.

## Integration

- Module needs to be initialized with two parameters, Independent Variable (Xin) and Dependent Variable (Yin).
- After creating object, call any of the nonlinear_regression by providing the order of model equation.
- Each nonlinear_regression method will return the list of coefficients. The number of coefficients in the list will be same as the order provided while calling regression method.

Following example shows how to integrate nonlinear_regression module with other component.

- Example1: Determine the coefficient of 4 order Polynomial regression.
```
regression = NonLinearRegression(Xin, Yin) 
coefficient = regression.polynomial(4)
```
 
      where
      Xin - List of Independent input
      Yin - List of Dependent Input
      4 - Order of polynomial regression equation
      
This will return coefficients list [B0, B1, B2, B3]

- Example2: Determine the coefficient of Sinusoidal of order 4
```
regression = NonLinearRegression(Xin, Yin)
coefficient = regression.sinusoidal(4)
```

This will return coefficients list [B0, B1, B2, B3]

Please note we support only 4 coefficients for Sinusoidal Model


- Example3: Determine the coefficient of Exponential of order 4.
```
regression = NonLinearRegression(Xin, Yin)
coefficient = regression.exponential(2)
```

This will return coefficients list [B0, B1]

Please note we support only 2 coefficients for Exponential Model

#### Requirement:
    1. python 2.7
    2. sympy package - to calculate the differentiation of sin or exp expression.
    To install sympy package, please use following commands
    $ pip install sympy
    Note: In the absense of sympy package only polynomial regression can be performed.