import numpy as np
from statsmodels.tsa.innovations.arma_innovations import arma_innovations

from arima.utils import covariance, lag


class MovingAverage:

	def __init__(self, index=None, data=None, lags=None):
		"""
		Constructor for Moving averages
		:param index: List with time index for uni-variate data
		:param data: List with data to be processed
		:param lags: Maximum lags to consider in the process
		"""
		if data and isinstance(data, list):
			self.data = data
		else:
			raise ValueError('Provide input for data as list')

		if index and isinstance(index, list):
			self.index = index
		else:
			raise ValueError('Provide input for index as list')

		self.lags = lags if lags else len(self.data)

		self.q = None

		self.theta_estimates = []

	def auto_covariance(self, data, lags=None):
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

	def innovations_algorithm(self, q, threshold=0.00001):
		acov = self.auto_covariance(self.data, q + 1)
		n = len(acov)
		max_lag = int(max(acov_i != 0 for acov_i in acov))

		v = [0] * (n + 1)
		v[0] = acov[0]

		# Retain only the relevant columns of theta
		# theta = [[0] * (max_lag + 1)] * (n + 1)
		theta = np.zeros((n + 1, max_lag + 1))
		for i in range(1, n):
			for k in range(max(i - max_lag, 0), i):
				sub = 0
				for j in range(max(i - max_lag, 0), k):
					sub += theta[k, k - j] * theta[i, i - j] * v[j]
				theta[i][i - k] = 1 / v[k] * (acov[i - k] - sub)
			v[i] = acov[0]
			for j in range(max(i - max_lag, 0), i):
				v[i] -= theta[i, i - j] ** 2 * v[j]
			# Break if v has converged
			if i >= 10:
				if v[i - 10] - v[i] < v[0] * threshold:
					# Forward fill all remaining values
					v[(i + 1):] = v[i]
					theta[(i + 1):] = theta[i]
					break

		# ma_params = [theta[i][:i] for i in range(1, q + 1)]
		return theta[:n, 1:]

	@staticmethod
	def innovations(data):
		"""
		Fallback for MA innovation algorithm
		"""
		return arma_innovations(data)
