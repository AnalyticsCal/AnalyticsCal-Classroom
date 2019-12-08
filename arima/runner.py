from tkinter.simpledialog import askstring

from statsmodels.tsa.innovations.arma_innovations import arma_innovations
from arima.auto_regression import AutoRegression
from matplotlib import pyplot as plt

from arima.utils import lag
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


def init_ar(time, data, lags=None):
	lags = lags if lags else len(data)
	if 0 <= lags <= len(data):
		ar = AutoRegression(index=time, data=data, lags=lags)
	else:
		raise ValueError(f'Lag must be between 0 and {len(data)}')
	return ar


def check_seasonality():
	response = askstring('Seasonality', 'Is the data seasonal? (Y/N): ')
	if response.upper() == 'Y':
		seasonal_period = int(askstring('Seasonality', 'Enter seasonality period: '))
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
	plt.tick_params(labelsize=10)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.grid(True)
	if significance:
		plt.axhline(significance)
		plt.axhline(-1 * significance)
	plt.show()
	return plt


def check_diff():
	response = input('Is the data stationary? (Y/N): ')
	if response.upper() == 'Y':
		return False
	elif response.upper() == 'N':
		return True
	else:
		raise ValueError('Invalid response!')


def ordinal(n):
	try:
		s = ['st', 'nd', 'rd'][(n - 1) % 10]
		if (n - 10) % 100 // 10:
			return str(n) + s
	except IndexError:
		pass
	return str(n) + 'th'


def do_diff(ar, period):
	diffed = ar.difference(period)
	ar.data = diffed
	non_seasonal_acf = ar.auto_correlation(diffed, 40)
	plt.clf()
	data_plot(
		x=range(len(non_seasonal_acf)),
		y=non_seasonal_acf,
		x_label='Lag',
		y_label='Correlation',
		title=f'Plot of ACF of {ordinal(ar.d if ar.d else period)} differenced data',
		n=50,
		plt_type='bar',
		significance=(1.96 / (len(diffed)) ** 0.5)
	)
	return ar, diffed


def predict_using_arima(data_list, phi, residue_list, theta):
	theta_values = []
	final_values = []
	phi_values = []
	
	for i, phi_i in enumerate(phi):
		lag_data = ([0] * i) + lag(data_list, i)
		phi_values.append([phi_i * x for x in lag_data])
	
	for i, theta_i in enumerate(theta):
		lag_data = ([0] * i) + lag(residue_list, i)
		theta_values.append([theta_i * x for x in lag_data])
	
	for pi, ti in zip(phi_values, theta_values):
		final_values.append(sum(pi) - sum(ti))
	
	# output = [abs(sum(elements)) for elements in zip(*value)]
	return final_values


def run(csv_list):
	time, data = get_data(csv_list)
	
	data_plot(time, data, 'Time', 'Discharge', 'Plot of raw data', n=40)
	ar = init_ar(time, data)
	
	raw = ar.auto_correlation(ar.data, 40)
	data_plot(
		range(len(raw)), raw, 'Lag', 'Correlation', 'Plot of ACF of raw data',
		n=40,
		plt_type='bar',
		significance=(1.96 / (len(raw)) ** 0.5)
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
	
	pacf = ar.yule_walker_pacf(100)
	data_plot(
		range(len(pacf)), pacf, 'Lags', 'Correlation', 'PACF', plt_type='bar', n=40,
		significance=(1.96 / (len(pacf)) ** 0.5)
	)
	
	p = int(input('Enter value of p: '))
	phi = pacf[:p]
	print(f'The AR({p}) equation is')
	print(' + '.join([f'({round(phi_i, 4)}) * y(t-{i + 1})' for i, phi_i in enumerate(phi)]), '+ residues')
	
	ar.data = ar.predict(phi)
	out = ar.difference(period, rev=True)
	
	plt.plot(time[:len(out)], data[:len(out)])
	plt.plot(time[:len(out)], out)
	plt.show()
	
	# o = AR(data, time)
	# ou = o.fit()
	# print(ou.params)
	# plt.plot(time, data)
	# plt.plot(time, list(o.predict(ou.params)) + [0] * 15)
	# plt.show()
	
	# ma params
	q = int(input('Enter value of q: '))
	
	if q:
		ma_params, mse = arma_innovations(out)
		theta = ma_params[:q]
		print('MA Equation is:')
		print(' + '.join([f'({round(theta_i, 4)}) * e(t-{i + 1})' for i, theta_i in enumerate(theta)]))
		
		# Calculate Error
		residues = []
		
		for y, y_cap in zip(data, out):
			residues.append(y - y_cap)
		
		data_plot(time[:len(residues)], residues, 'Time', 'Residues', 'Plot of residues', n=40)
		
		# Final Predicted Output
		# final_output = predict_using_arima(data, phi, residues, theta)
		pass

# arma_innovations

# csv = load_csv_file('E:\Github/khanapur_flow.csv')
# run(csv)
