from numpy.linalg import inv
from arima.utils import correlation, toeplitz


class AutoRegression:

	def __init__(self, index=None, data=None):
		if data and isinstance(data, list):
			self.data = data
		else:
			raise ValueError('Provide input for data as list')

		if index and isinstance(index, list):
			self.index = index
		else:
			raise ValueError('Provide input for index as list')

		self.output = []

	def __str__(self):
		print(self.output)

	def lag(self, num=None):
		"""
		Generate nth lag of the time series data
		:param num: Number of the lag needed
		:return: Time series lagged num times
		"""
		if isinstance(num, int):
			return self.data[num:] if num >= 0 else self.data[:num]
		else:
			raise ValueError('Pass value of lag number as integer')

	def auto_correlation(self, num_lags=None):
		"""
		Compute Auto Correlation on the data
		:param num_lags: Number of lags to auto correlate on
		:return:
		"""
		corr_values = []
		for cur_lag in range(num_lags):
			corr_values.append(correlation(self.lag(cur_lag), self.lag(-1 * cur_lag)))
		return corr_values

	def seasonal_difference(self, time_period=None):
		"""
		Compute seasonal differencing of the data
		:param time_period: Seasonality period
		:return: Seasonal differenced time series
		"""
		non_seasonal = []
		for i, val in enumerate(self.data):
			diff = (val - self.data[i + time_period]) if (i + time_period) < len(self.data) else 0
			non_seasonal.append(diff)
		return non_seasonal

	def yule_walker_phi_estimate(self, p):
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
		ac = self.auto_correlation(p + 1)
		r_upper = toeplitz(ac[:p])
		r = ac[1: p+1]
		phi = inv(r_upper).dot(r)
		return phi

	def fit(self):
		pass


def test():
	import pandas as pd
	import matplotlib.pyplot as plt
	df = pd.read_csv('/home/vishnudev/Documents/khanapur_flow.csv')
	df['date'] = df['Year'].astype(str) + '-' + df['Month'].astype(str)
	ar = AutoRegression(index=df['date'].to_list(), data=df['Avg Discharge'].to_list())
	ar.data = ar.seasonal_difference(time_period=12)
	phi = ar.yule_walker_phi_estimate(3)
	print(phi)
	from statsmodels.tsa.arima_model import ARIMA
	order = (3, 0, 0)
	ars = ARIMA(ar.data, order)
	# values = ar.auto_correlation(num_lags=40)
	# plt.bar(range(len(values)), values)
	# significance = 1.96 / len(ar.data) ** 0.5
	# plt.axhline(y=significance)
	# plt.axhline(y=-significance)
	# plt.show()


if __name__ == '__main__':
	test()

