"""
REGRESSION R2 MSE MAE RMSE

analyzing data:
	1. calculate general metrics
	2. calculate correlation

	3. count number of each types of cpu and gpu
	4. histogram by year
	5. plot everything by date

correlation calculating:
"""


import pandas as pd


def calculate_general_metrics(data: pd.DataFrame) -> None:
	print(data.describe())


def calculate_correlation(data: pd.DataFrame) -> None:
	print(data.corr(numeric_only=True))


def analyze_data(data: pd.DataFrame, analytics_file: str) -> None:
	# calculate_general_metrics(data)
	calculate_correlation(data)


def main() -> None:
	analyze_data(pd.read_csv('step2_data_processing\data\cpu.csv'), 'step3_correlation_calculating\\analytics\cpu.txt')
	analyze_data(pd.read_csv('step2_data_processing\data\gpu.csv'), 'step3_correlation_calculating\\analytics\gpu.txt')


if __name__ == '__main__':
	main()