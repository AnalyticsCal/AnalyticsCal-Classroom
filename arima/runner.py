import numpy as np
from matplotlib import pyplot as plt
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.stattools import innovations_algo, acovf

from arima.auto_regression import AutoRegression
from arima.moving_average import MovingAverage
from data_load import load_csv_file


def get_data(csv_list, precision=3):
	headers = csv_list[0]
	data = csv_list[1:]
	print(f"Headers are: {', '.join(headers)}")
	# time_column_index = headers.index(input('Enter column to consider as time index: '))
	# data_column_index = headers.index(input('Enter column to consider as data: '))
	time_column_index = 0
	data_column_index = 1
	time_column = [v[time_column_index] for v in data]
	data_column = [round(float(v[data_column_index]), precision) for v in data]
	return time_column, data_column


def init_ar(time, data):
	print(f'Number of data points are {len(data)}')
	# lags = int(input('Enter number of lags to consider: '))
	lags = 100
	if 0 <= lags <= len(data):
		ar = AutoRegression(index=time, data=data, lags=lags)
	else:
		raise ValueError(f'Lag must be between 0 and {len(data)}')
	return ar


def check_seasonality():
	response = input('Is the data seasonal? (Y/N): ')
	if response.upper() == 'Y':
		seasonal_period = int(input('Enter seasonality period: '))
		return seasonal_period
	elif response.upper() == 'N':
		return None
	else:
		raise ValueError('Invalid response!')


def data_plot(x, y, x_label, y_label, title, n=None, plt_type='line', significance=None):
	n = n if n else len(x)
	if plt_type == 'line':
		plt.plot(x[:n], y[:n])
	elif plt_type == 'bar':
		plt.bar(x[:n], y[:n])
	else:
		raise NotImplementedError
	plt.title(title)
	plt.xticks(x[:n], rotation=90)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.grid(True)
	if significance:
		plt.axhline(significance)
		plt.axhline(-1 * significance)
	plt.show()


def check_diff():
	response = input('Is the data stationary? (Y/N): ')
	if response.upper() == 'Y':
		return False
	elif response.upper() == 'N':
		return True
	else:
		raise ValueError('Invalid response!')


def do_diff(ar, period):
	diffed = ar.difference(period)
	ar.data = diffed
	non_seasonal_acf = ar.auto_correlation(diffed, 40)
	data_plot(
		x=range(len(non_seasonal_acf)),
		y=non_seasonal_acf,
		x_label='Lag',
		y_label='Correlation',
		title='Plot of ACF of differenced data',
		n=50,
		plt_type='bar',
		significance=(1.96 / (len(diffed)) ** 0.5)
	)
	return ar, diffed


def run(csv_list):
	time, data = get_data(csv_list)

	data_plot(time, data, 'Time', 'Discharge', 'Plot of raw data', n=40)
	ar = init_ar(time, data)

	raw = ar.auto_correlation(ar.data, 40)
	data_plot(
		range(len(raw)), raw, 'Lag', 'Correlation', 'Plot of ACF of raw data',
		n=40,
		plt_type='bar',
		significance=(1.96 / (len(raw))**0.5)
	)

	period = check_seasonality()
	if period:
		ar, non_seasonal = do_diff(ar, period)
	else:
		non_seasonal = ar.data

	d = 0
	diff = non_seasonal
	while True:
		is_needed = check_diff()
		if is_needed:
			d += 1
			ar, diff = do_diff(ar, 1)
		else:
			break

	ar.data = diff

	pacf = ar.yule_walker_pacf()
	data_plot(
		range(len(pacf)), pacf, 'Lags', 'Correlation', 'PACF', plt_type='bar', significance=(1.96 / (len(pacf)) ** 0.5)
	)

	p = int(input('Enter value of p: '))
	phi = ar.yule_walker_estimate(p)
	print(f'The AR({p}) equation is')
	print(' + '.join([f'({round(phi_i, 4)}) * y(t-{i+1})' for i, phi_i in enumerate(phi)]), '+ residues')

	out = ar.predict(phi)
	print(len(data), len(out))

	out = out + [0] * (len(data) - len(out))

	plt.plot(time, data)
	plt.plot(time, out)
	plt.show()

	# o = AR(data, time)
	# ou = o.fit()
	# print(ou.params)
	# plt.plot(time, data)
	# plt.plot(time, list(o.predict(ou.params)) + [0] * 15)
	# plt.show()

	# ma = MovingAverage(time, data, 100)
	# theta = ma.innovations_algorithm(3)
	# ma_params = [theta[i, :i] for i in range(1, 3 + 1)]
	# print(ma_params)


csv = load_csv_file('/home/vishnudev/Desktop/khanapur_flow.csv')
run(csv)
