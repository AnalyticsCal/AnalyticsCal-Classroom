import matplotlib.pyplot as plt
from numpy.linalg import inv

from linear_algebra import LinearAlgebra
from arima.utils import correlation, toeplitz


class AutoRegression:

	def __init__(self, index=None, data=None, lags=None):
		"""
		Constructor for auto regression
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

		self.phi_estimates = []

	def __str__(self):
		print(self.output)

	@staticmethod
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

	def auto_correlation(self, data, lags):
		"""
		Compute Auto Correlation on the data
		:param data: Input data to find correlations on
		:return: Auto correlations
		"""
		corr_values = []
		for cur_lag in range(lags):
			corr_values.append(correlation(self.lag(data, cur_lag), self.lag(data, -1 * cur_lag)))
		return corr_values

	def difference(self, n):
		a = self.data
		b = a[n:]
		return [(x - y) for x, y in zip(a, b)]

	def seasonal_difference(self, time_period=None):
		"""
		Compute seasonal differencing of the data
		:param time_period: Seasonality period
		:return: Seasonal differenced time series
		"""
		non_seasonal = []
		for i, val in enumerate(self.data):
			if (i + time_period) < len(self.data):
				diff = (val - self.data[i + time_period])
				non_seasonal.append(diff)
		return non_seasonal

	def yule_walker_pacf(self):
		pacf = [1]
		for k in range(1, self.lags + 1):
			pacf.append(self.yule_walker_estimate(k)[-1])
		return pacf

	def yule_walker_estimate(self, p):
		"""
		Yule Walker estimation of coefficients of AR model
		The final form of YW equation is used i.e.

			phi = R^-1 . r
			where;
				R = Toeplitz array of r0, r1, r2, r3 ... r base p-1
				r = (p x 1) sized array of r1, r2, r3 ... r base p
				phi = array of phi1, phi2 ... phi base p

		:param p: Order of the auto-regression model
		:return: Estimated Values of phi
		"""
		ac = self.auto_correlation(self.data, p + 1)
		r_upper = toeplitz(ac[:p])
		r = ac[1: p+1]
		# la = LinearAlgebra(len(r_upper))
		# r_upper_inv = la.getMatrixInverse(r_upper)
		# phi = la.getMatrixMultiplication(r_upper_inv, r)
		# return phi
		return inv(r_upper).dot(r)

	@staticmethod
	def plot(self, x, y, plot_type='line', significance=None):
		if plot_type == 'line':
			plt.plot(x, y)
		elif plot_type == 'bar':
			plt.bar(x, y)

		if significance:
			plt.axhline(y=significance)
			plt.axhline(y=-significance)

		plt.show()

	def fit(self):
		pass


def test():
	import pandas as pd
	df = pd.read_csv('/home/vishnudev/Documents/khanapur_flow.csv')
	df['date'] = df['Year'].astype(str) + '-' + df['Month'].astype(str)
	ar = AutoRegression(index=df['date'].to_list(), data=df['Avg Discharge'].to_list())
	from statsmodels.tsa.stattools import pacf_yw
	ar.data = ar.seasonal_difference(time_period=12)
	# print(ar.yule_walker_pacf(3))
	# print(pacf_yw(ar.data, 3))
	# values = ar.auto_correlation(num_lags=40)
	# ar.plot(range(len(values)), values, 'bar')
	# ar.data = ar.seasonal_difference(time_period=12)
	# significance = 1.96 / len(ar.data) ** 0.5
	# values = ar.auto_correlation(num_lags=40)
	# ar.plot(range(len(values)), values, 'bar', significance)
	# ar.data = ar.difference(1)
	# values = ar.auto_correlation(num_lags=40)
	# ar.plot(range(len(values)), values, 'bar', significance)
	# phi = ar.yule_walker_phi_estimate(3)
	# print(phi)
	# plt.bar(range(len(values)), values)
	# significance = 1.96 / len(ar.data) ** 0.5
	# plt.axhline(y=significance)
	# plt.axhline(y=-significance)
	# plt.show()


if __name__ == '__main__':
	test()

