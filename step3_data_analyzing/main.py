"""
analyzing data:
	1. read and preprocess data
	2. profile data
	3. plot scatters
	4. plot avgs
	5. regression R2
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas.api.types import is_numeric_dtype


def profile(data: pd.DataFrame, analytics_file: str) -> None:
	from ydata_profiling import ProfileReport

	data_view: pd.DataFrame = data

	data_view['Release Date'] = data_view['Release Date'].apply(lambda date: date.timestamp())

	ProfileReport(
		data_view,
		tsmode=True,
		correlations={
			'auto': {'calculate': False},
			'pearson': {'calculate': True}
		},
		missing_diagrams={
			'bar': False,
			'heatmap': False,
			'matrix': False
		}
	).to_file(analytics_file)


def apply_log_scale(data: pd.DataFrame) -> None:
	from math import log2

	for column in data:
		if not 'Date' in column and (data[column].dtype == 'int64' or data[column].dtype == 'float64'):
			data[column] = data[column].apply(lambda value: log2(value))


def preprocess(data_file: str) -> pd.DataFrame:
	data: pd.DataFrame = pd.read_csv(data_file)

	data['Release Date'] = data['Release Date'].apply(lambda date: pd.to_datetime(date, format='%Y-%m-%d'))

	return data


def adjust_plot() -> plt.subplot:
	plt.rc('font', size=24)
	plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
	plt.tick_params(which='major', width=2, length=8)
	plt.tick_params(which='minor', width=2, length=4)
	ax = plt.subplot(1, 1, 1)
	plt.setp(ax.spines.values(), linewidth=2)
	return ax


def plot_scatters(data: pd.DataFrame, count: int, color: str) -> None:
	plt.subplots_adjust(left=0.3, right=0.7, top=0.99, bottom=0.03)
	plt.rc('axes', labelsize=14)

	for column in data:
		if is_numeric_dtype(data[column]) and not 'Thread' in column and not 'G2D' in column:
			ax = plt.subplot(5, 2, count)
			ax.set_ylabel(column)
			if count >= 9:
				ax.set_xlabel('Release Date')

			ax.tick_params(axis='both', which='both', left=False, right=False, labelleft=False)
			plt.scatter(data['Release Date'], data[column], color=color)
			count += 2


def plot(data: pd.DataFrame, date_column: str, column: str, color: str, label: str, ylabel: str) -> None:
	adjust_plot()

	data.plot(x=date_column, y=column, kind='line', color=color, label=label, ylabel=ylabel, linewidth=4)

	plt.legend()


def plot_model(
	data: pd.DataFrame, date_column: str, column: str, degree: int, color: str, label: str, ylabel: str,
	bottom: int, top: int
) -> None:
	data = data.reset_index()
	x = data[date_column].apply(lambda date: date.to_timestamp().timestamp()).to_numpy()
	y = data[column].to_numpy()

	line_coeffs = np.polyfit(x, y, 1)
	poly_coeffs = np.polyfit(x, y, degree)
	line = np.poly1d(line_coeffs)
	poly = np.poly1d(poly_coeffs)

	xx = np.linspace(x.min(), x.max() + 31_536_000, 1_000)
	dd = [pd.to_datetime(x, unit='s') for x in xx]
	dd2 = [pd.to_datetime(d, unit='s') for d in x]

	ax = adjust_plot()
	plt.subplots_adjust(left=0.09, right=0.96, top=0.98, bottom=0.11)

	plt.plot(dd, poly(xx), color=color, linewidth=2, linestyle='dotted')
	plt.plot(dd, line(xx), color=color, linewidth=4, label=label)
	plt.scatter(dd2, data[column], color=color)

	ax.set_xlabel(date_column)
	ax.set_ylabel(ylabel)
	ax.set_xlim(left=17_167, right=19_723)
	ax.set_ylim(bottom=bottom, top=top)

	plt.legend()

	yhat = poly(x)
	ybar = np.sum(y) / len(y)
	ssreg = np.sum((yhat - ybar) ** 2)
	sstot = np.sum((y - ybar) ** 2)

	print(ssreg / sstot)


def get_avg_data(data: pd.DataFrame, date_column: str, column: str) -> pd.DataFrame:
	return data.groupby(pd.PeriodIndex(data[date_column], freq='Q'))[column].mean(numeric_only=True)


def get_pricing_data(data: pd.DataFrame) -> pd.DataFrame:
	from ast import literal_eval

	pricess = data['Prices'].apply(literal_eval).to_list()
	pricing_pricess = []
	pricing_datess = []

	for prices in pricess:
		pricing_pricess += [price[1] for price in prices]
		pricing_datess += [pd.to_datetime(price[0], format='%Y-%m-%d') for price in prices]

	return pd.DataFrame({'Date': pricing_datess, 'Price': pricing_pricess})


def profile_data(data_file: str, analytics_file: str) -> None:
	data: pd.DataFrame = preprocess(data_file)
	apply_log_scale(data)
	profile(data, analytics_file)


def analyze_datas(cpu_data_file: str, gpu_data_file: str) -> None:
	cpu_data: pd.DataFrame = preprocess(cpu_data_file)
	gpu_data: pd.DataFrame = preprocess(gpu_data_file)

	plot_scatters(cpu_data, 1, 'tab:blue')
	plot_scatters(gpu_data, 2, 'tab:orange')
	plt.show()

	# cpu_avg_pricing_data: pd.DataFrame = get_avg_data(get_pricing_data(cpu_data), 'Date', 'Price')
	# gpu_avg_pricing_data: pd.DataFrame = get_avg_data(get_pricing_data(gpu_data), 'Date', 'Price')
	# plot(cpu_avg_pricing_data, 'Date', 'Price', 'tab:blue', 'CPU', 'Average Price')
	# plot(gpu_avg_pricing_data, 'Date', 'Price', 'tab:orange', 'GPU', 'Average Price')

	# cpu_data = cpu_data[cpu_data['Mark'] != cpu_data['Mark'].max()]
	# cpu_data = cpu_data[cpu_data['Mark'] != cpu_data['Mark'].max()]
	# plot_model(
	# 	get_avg_data(cpu_data, 'Release Date', 'Mark'),
	# 	'Release Date', 'Mark', 7, 'tab:blue', 'CPU Mark', 'Average Mark', 0, 70000
	# )
	# plot_model(
	# 	get_avg_data(gpu_data, 'Release Date', 'G3D Mark'),
	# 	'Release Date', 'G3D Mark', 7, 'tab:orange', 'GPU G3D Mark', 'Average Mark', 0, 70000
	# )

	# plt.show()


def main() -> None:
	# profile_data('step2_data_processing\data\cpu.csv', 'step3_correlation_calculating\\analytics\cpu.html')
	# profile_data('step2_data_processing\data\gpu.csv', 'step3_correlation_calculating\\analytics\gpu.html')
	analyze_datas('step2_data_processing\data\cpu.csv', 'step2_data_processing\data\gpu.csv')


if __name__ == '__main__':
	main()