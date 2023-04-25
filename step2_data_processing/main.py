"""
data processing:
	1. drop irrelevant or derived columns (Unnamed, Value, Thread Value, Power Perf., Test Date, Socket, URL)
	2. process data types of columns:
		2.1. remove rows with no Price
		2.2. merge Price with Prices and drop Price
		2.3. convert marks to float
	3. process null rows:
		3.1. fill TDP and Thread Mark with mean value
	4. remove irrelevant rows:
		4.1. remove rows before 2017
	5. recalculate derived columns:
		CPU:
			Value = Mark / Price
			Single Thread Value = Single Thread Mark / Price
			Power Performance = Mark / TDP

		GPU:
			Value = G3D Mark / Price
			Power Performance = G3D Mark / TDP
"""


import ast
import math
import pandas as pd
import regex as re
from time import strftime, localtime


def drop_irrelevant_columns(data: pd.DataFrame) -> None:
	data.drop(
		columns=['Unnamed: 0', 'Value', 'Thread Value', 'Power Perf.', 'Test Date', 'Socket', 'URL'],
		inplace=True, errors='ignore'
	)


def process_data_types(data: pd.DataFrame) -> None:
	to_datetime = lambda epoch: pd.to_datetime(strftime('%Y-%m-%d', localtime(epoch / 1000)), format='%Y-%m-%d')

	data.dropna(subset=['Price'], inplace=True)

	latest_prices: list = data['Price'].str.findall(r"\$(\d+\,?\d*\.?\d+)[\s\w]+\((\d+-\d+-\d+)\)").to_list()
	pricess: list = data['Prices'].apply(ast.literal_eval).to_list()

	data['Prices'] = [
		prices + ([(price[0][1], price[0][0])] if isinstance(price, list) and len(price[0]) == 2 else [])
		for (prices, price) in zip(pricess, latest_prices)
	]

	data['Prices'] = data['Prices'].apply(lambda prices: sorted(list(set([
		(
			to_datetime(int(price[0])) if price[0].isdigit() else pd.to_datetime(price[0], format='%Y-%m-%d'),
			float(price[1].replace(',', ''))
		)
		for price in prices
	]))))

	data.drop(columns=['Price'], inplace=True, errors='ignore')

	for column in data:
		if 'Mark' in column:
			data[column] = data[column].apply(lambda mark: float(str(mark).replace(',', '')))

	data['Release Date'] = data['Release Date'].apply(
		lambda epoch: to_datetime(int(epoch)) if not math.isnan(epoch) else None
	)


def process_null_rows(data: pd.DataFrame) -> None:
	data['TDP (W)'].fillna(data['TDP (W)'].mean(), inplace=True)

	if 'Thread Mark' in data:
		data['Thread Mark'].fillna(data['Thread Mark'].mean(), inplace=True)


def remove_irrelevant_rows(data: pd.DataFrame) -> None:
	data.drop(data[data['Release Date'] < pd.to_datetime('2017-01-01')].index, inplace=True)


def recalculate_derived_columns(data: pd.DataFrame) -> None:
		mark: str = 'Mark' if 'Mark' in data else 'G3D Mark'

		data['Power Perf.'] = data[mark] / data['TDP (W)']
		data['Value'] = [row[mark] / row['Prices'][0][1] for index, row in data.iterrows()]

		if 'Thread Mark' in data:
			data['Thread Value'] = [row['Thread Mark'] / row['Prices'][0][1] for index, row in data.iterrows()]


def process_data(data_file: str, cleaned_data_file: str) -> None:
	data: pd.DataFrame = pd.read_csv(data_file)

	print('drop_irrelevant_columns')
	drop_irrelevant_columns(data)

	print('process_data_types')
	process_data_types(data)

	print('process_null_rows')
	process_null_rows(data)

	print('remove_irrelevant_rows')
	remove_irrelevant_rows(data)

	print('recalculate_derived_columns')
	recalculate_derived_columns(data)

	print(data.info())

	data.to_csv(cleaned_data_file, encoding='utf-8', index=False)


def main() -> None:
	process_data(
		'step1_data_crawling\data_csv\cpu.csv',
		'step2_data_processing\data\cpu.csv'
	)
	process_data(
		'step1_data_crawling\data_csv\gpu.csv',
		'step2_data_processing\data\gpu.csv'
	)


if __name__ == '__main__':
	main()