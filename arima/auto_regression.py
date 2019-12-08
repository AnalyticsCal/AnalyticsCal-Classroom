from arima.utils import correlation, toeplitz, lag
from numpy.linalg import inv


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

		self.sp = 0  # Seasonality Period
		self.p = None
		self.d = None
		self.phi_estimates = []
	
	def __str__(self):
		print(self.phi_estimates)
	
	def auto_correlation(self, data, lags):
		"""
		Compute Auto Correlation on the data
		:param lags: Number of lags to consider
		:param data: Input data to find correlations on
		:return: Auto correlations
		"""
		corr_values = []
		for cur_lag in range(lags):
			corr_values.append(correlation(lag(data, cur_lag), lag(data, -1 * cur_lag)))
		return corr_values
	
	def difference(self, n, rev=False):
		a = self.data
		b = a[n:]
		return [(y - x) if not rev else (y + x) for x, y in zip(a, b)]
	
	def seasonal_difference(self, time_period=None, rev=False):
		"""
		Compute seasonal differencing of the data
		:param rev: Do reverse flag
		:param time_period: Seasonality period
		:return: Seasonal differenced time series
		"""
		non_seasonal = []
		for i, val in enumerate(self.data):
			if (i + time_period) < len(self.data):
				diff = (self.data[i + time_period] + val) if rev else (self.data[i + time_period] - val)
				non_seasonal.append(diff)
		return non_seasonal
	
	def yule_walker_pacf(self, order):
		pacf = [1]
		for k in range(1, order + 1):
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
		r = [0] * (p + 1)
		r[0] = sum(x ** 2 for x in self.data) / len(self.data)
		for k in range(1, p + 1):
			r[k] = sum(x * y for x, y in zip(self.data[0:-k], self.data[k:])) / len(self.data)
		r_upper = toeplitz(r[:-1])
		r = r[1: p + 1]
		return inv(r_upper).dot(r)
	
	def predict(self, phi):
		value = []
		for i, phi_i in enumerate(phi):
			lag_data = ([0] * i) + lag(self.data, i)
			value.append([phi_i * x for x in lag_data])
		output = [abs(sum(elements)) for elements in zip(*value)]
		return output
