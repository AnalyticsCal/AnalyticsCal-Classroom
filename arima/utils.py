from fractions import Fraction

from linear_algebra import LinearAlgebra


def mean(x):
    """
    Calculate the mean of a array of numbers
    :param x: Input array of numbers
    :return: Mean
    """
    return sum(x) / len(x)


def sd(x):
    """
    Calculate standard deviation of an array
    :param x: Input array of numbers
    :return: Standard deviation
    """
    x_mean = mean(x)
    return (
               sum((x_i - x_mean) ** 2 for x_i in x) / (len(x) - 1)
           ) ** 0.5


def toeplitz(x):
    """
    The Toeplitz matrix has constant diagonals.
    :param x: Input row array
    :return: toeplitz matrix
    """
    t = []
    for i in range(len(x)):
        row = []
        for j in range(len(x)):
            if i < j:
                row.append(x[j-i])
            elif i == j:
                row.append(x[0])
            else:
                row.append(x[i-j])
        t.append(row)
    return t


def covariance(x, y):
    """
    Calculate the joint variability of two variables i.e. covariance
    :param x: Input array x
    :param y: Input array y
    :return: Covariance value
    """
    x_mean = mean(x)
    y_mean = mean(y)
    diff_x_mean = (x_i - x_mean for x_i in x)
    diff_y_mean = (y_i - y_mean for y_i in y)
    sum_xy_diff = sum(a * b for a, b in zip(diff_x_mean, diff_y_mean))
    return sum_xy_diff / (len(x) - 1)


def correlation(x, y):
    """
    Calculate Correlation Coefficient between two variables
    :return: Value of correlation coefficient that lies between -1 and +1
    """
    return covariance(x, y) / (sd(x) * sd(y))


def lag(data, num=None):
    """
    Generate nth lag of the time series data
    :param data: Input data
    :param num: Number of the lag needed
    :return: Time series lagged num times
    """
    if isinstance(num, int):
        return data[num:] if num >= 0 else data[:num]
    else:
        raise ValueError('Pass value of lag number as integer')


def auto_covariance(data, lags=None):
    """
    Compute Auto Correlation on the data
    :param data: Input data to find correlations on
    :param lags: Number of lags to limit output
    :return: Auto correlations
    """
    lags = lags if lags else len(data) - 1
    cov_values = []
    for cur_lag in range(lags):
        cov_values.append(covariance(lag(data, cur_lag), lag(data, -1 * cur_lag)))
    return cov_values


def test():
    x = [1, 2, 3, 4]
    print(toeplitz(x))


if __name__ == '__main__':
    test()
