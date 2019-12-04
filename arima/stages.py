from tkinter import simpledialog

from tkinter import *

from arima.runner import get_data, data_plot, init_ar
from data_load import load_csv_file

root = Tk()
frame = Frame(root)
frame.pack()


SEASONAL_DIFFERENCE = {
	'title': 'Seasonal Difference',
	'question': 'Do you want to go back? (yes/no)'
}

csv = load_csv_file('/mnt/beta/Personal/IISc/khanapur_flow.csv')
time, data = get_data(csv)


def data_change(lags):
	data_plot(time, data, 'Time', 'Discharge', 'Plot of raw data', n=int(lags))
	ar = init_ar(time, data, lags)
	return ar


def load_data(time_list, data_list):
	# lags = int(simpledialog.askstring('Lags', 'Enter number of lags'))
	btn = Button(frame, text='Change Lags!', command=data_change(10))


def stationary():

	if simpledialog.askstring(SEASONAL_DIFFERENCE['title'], SEASONAL_DIFFERENCE['question']).lower() == 'yes':
		print('DO')


load_data(time, data)
# stationary()


root.mainloop()
