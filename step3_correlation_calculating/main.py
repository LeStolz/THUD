"""
analyzing data:
	1. count number of cpu and gpu
	2. count number of each types of cpu and gpu

	3. histogram by year
	4. plot everything by date

correlation calculating:
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


def count_data(name, table):
	print(f'{name} count:', table['Name'].count())

	g = sns.catplot(data=table, x='Category', kind='count')
	g.fig.suptitle(f'{name} categories')
	g.set_xticklabels(rotation=30, ha='right')
	plt.show()

	table['Release Year'] = table['Release Date']
	g = px.histogram(table, x='Release Year', title=f'{name} categories by release year', color='Category')
	g.show()


def scatter_plot_data(name, table):
	g = px.scatter(table, x='Release Date', title=f'{name} categories by release date', color='Category')
	g.show()


def analyze_data(name, table):
	print(table.describe())


def calculate_correlation(name, table):
	sns.heatmap(table.corr(numeric_only=True))
	plt.show()


def main():
	cpu_table = pd.read_csv('step1_data_crawling\data_csv\cpu.csv')
	gpu_table = pd.read_csv('step1_data_crawling\data_csv\gpu.csv')

	# count_data('cpu', cpu_table)
	# count_data('gpu', gpu_table)

	# scatter_plot_data('cpu', cpu_table)
	# scatter_plot_data('gpu', gpu_table)

	analyze_data('cpu', cpu_table)
	analyze_data('gpu', gpu_table)

	# calculate_correlation('cpu', cpu_table)
	# calculate_correlation('gpu', gpu_table)


if __name__ == '__main__':
	main()