"""
data selection:
  considered:
	michael:
		https://www.kaggle.com/datasets/michaelbryantds/cpu-and-gpu-product-data?resource=download
		does not have price

	dataworld:
		https://data.world/fiftin/intel-processors
		does not have price over all products, only concerns intel processors

	wiki:
		https://en.wikipedia.org/wiki/List_of_AMD_graphics_processing_units
		https://en.wikipedia.org/wiki/List_of_Intel_processors
		https://en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units
		inconsistent format, thus hard to crawl automatically or manually

  settled on:
	passmark:
		https://www.cpubenchmark.net/CPU_mega_page.html
		https://www.videocardbenchmark.net/GPU_mega_page.html
		does not have price, but price can be crawled

data acquisition:
  preparing the data:
	1. select all columns and show all entries of the table
	2. sort data by price so we can easily remove products without price
	3. copy the html file to cpu.html and gpu.html respectively
	4. remove products without price because no price -> no launch date -> useless

  crawling the data:
"""


import pandas as pd
import regex as re
import bs4
import requests


def read_html_table(file, url: str, columns: list) -> pd.DataFrame:
	deformat = lambda string: ' '.join(string.split())

	doc: bs4.BeautifulSoup = bs4.BeautifulSoup(file, 'html.parser')

	rows = doc.tbody.find_all('tr')

	return pd.DataFrame(
		columns=columns,
		data=[
			[deformat(col.text) for col in row.find_all('td')] +
			[url + row.find('td', {'class': 'sorting_1'}).find('a')['href']]
			for row in rows
		]
	)


count: int = 0
def read_html_prices(file) -> list:
	global count
	print(count)
	count += 1

	doc: bs4.BeautifulSoup = bs4.BeautifulSoup(file, 'html.parser')
	prices = doc.find(string=re.compile('var dataArray'))
	price = doc.find(string=re.compile('Last Price Change'))

	prices: list = re.findall(r"{x: (\d+), y: (\d+.?\d+)}+", prices.parent.text) if prices else []

	price: list = [price.parent.parent.text] if price else []

	return prices + price


def crawl_data(html: str, html_url: str, columns: list, csv: str) -> None:
	with requests.Session() as session:
		with open(html, 'r', encoding='utf-8', newline='') as file:
			table: pd.DataFrame = read_html_table(file, html_url, columns)

		table['Prices'] = [
			read_html_prices(session.get(row['URL']).text)
			for index, row in table.iterrows()
		]

		table['Price'] = [
			row['Prices'].pop() if row['Prices'] else None
			for index, row in table.iterrows()
		]

		table['Release Date'] = [
			row['Prices'][0][0] if row['Prices'] else None
			for index, row in table.iterrows()
		]

		table.to_csv(csv, encoding='utf-8', index=False)


def main() -> None:
	crawl_data(
		'step1_data_crawling\data_html\cpu.html',
		'https://www.cpubenchmark.net/',
		[
			'', 'Name', 'Number of Sockets', 'Cores', 'Price', 'Mark', 'Value',
			'Thread Mark', 'Thread Value', 'TDP (W)', 'Power Perf.', 'Test Date', 'Socket', 'Category', 'URL'
		],
		'step1_data_crawling\data_csv\cpu.csv'
	)
	crawl_data(
		'step1_data_crawling\data_html\gpu.html',
		'https://www.videocardbenchmark.net/',
		['', 'Name', 'Price', 'G3D Mark', 'Value', 'G2D Mark', 'TDP (W)', 'Power Perf.', 'Test Date', 'Category', 'URL'],
		'step1_data_crawling\data_csv\gpu.csv'
	)


if __name__ == '__main__':
	main()