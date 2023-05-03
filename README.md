# THUD

## Overview
### Source Code
The source codes for each step can be found in their respective folders.

More details on these source codes can be found in the following sections.

### Datasets
The raw dataset can be found in the [`data_html`](https://github.com/LeStolz/THUD/tree/main/step1_data_crawling/data_html) folder.
The processed dataset can be found in the [`data`](https://github.com/LeStolz/THUD/tree/main/step2_data_processing/data) folder.

More details on these datasets can be found in the following sections.

### References
References can be found in the [`THUD.bib`](https://github.com/LeStolz/THUD/blob/main/step4_writing/THUD.bib) file.

## Step 1 Data Crawling
### Purpose
The purpose of the step is to parse the acquired htmls and crawl additional pricing and date data.

### Input
The input of this step are the files in the [`data_html`](https://github.com/LeStolz/THUD/tree/main/step1_data_crawling/data_html) folder.

These files are acquired from PassMark's
[CPU](https://www.cpubenchmark.net/CPU_mega_page.html) and
[GPU](https://www.videocardbenchmark.net/GPU_mega_page.html) datasets
and after performing the following steps:
1. Select all columns and show all entries of the tables
2. Sort data by price so we can easily remove products without price
3. Copy the html files to
[`cpu.html`](https://github.com/LeStolz/THUD/blob/main/step1_data_crawling/data_html/cpu.html) and
[`gpu.html`](https://github.com/LeStolz/THUD/blob/main/step1_data_crawling/data_html/gpu.html) respectively inside the
[`data_html`](https://github.com/LeStolz/THUD/tree/main/step1_data_crawling/data_html) folder
4. Remove products without price

### Output
The output of this step are the files in the [`data_csv`](https://github.com/LeStolz/THUD/tree/main/step1_data_crawling/data_csv) folder.

These files are acquired from running [`step 1's main.py`](https://github.com/LeStolz/THUD/blob/main/step1_data_crawling/main.py) which performs the following steps:
1. Parse the htmls into a
[`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) while also extracting each row's urls
2. These urls are then used to crawl the pricing history, relase price and release date data
3. Output the
[`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)
into a csv file inside the [`data_csv`](https://github.com/LeStolz/THUD/tree/main/step1_data_crawling/data_csv) folder

More details can be found at [`step 1's main.py`](https://github.com/LeStolz/THUD/blob/main/step1_data_crawling/main.py).

## Step 2 Data Processing
### Purpose
The purpose of the step is to process the acquired data from step 1.

### Input
The input of this step are the files in the [`data_csv`](https://github.com/LeStolz/THUD/tree/main/step1_data_crawling/data_csv) folder.

### Output
The output of this step are the files in the [`data`](https://github.com/LeStolz/THUD/tree/main/step2_data_processing/data) folder.

These files are acquired from running [`step 2's main.py`](https://github.com/LeStolz/THUD/blob/main/step2_data_processing/main.py) which performs the following steps:
1. Drop irrelevant or derived columns
2. Process data types of columns
3. Process null rows
4. Remove irrelevant rows
5. Recalculate derived columns

More details can be found at [`step 2's main.py`](https://github.com/LeStolz/THUD/blob/main/step2_data_processing/main.py).

## Step 3 Data Analyzing
### Purpose
The purpose of the step is to analyze the acquired data from step 2.

### Input
The input of this step are the files in the [`data`](https://github.com/LeStolz/THUD/tree/main/step2_data_processing/data) folder.

### Output
The output of this step are the files in the [`analytics`](https://github.com/LeStolz/THUD/tree/main/step3_data_analyzing/analytics) folder
or appear on screen using [`matplotlib`](https://matplotlib.org/).
The outputs that appear on screen can be found in [`step4_writting`](https://github.com/LeStolz/THUD/tree/main/step4_writing) in the form of png files.

These results are acquired from running [`step 3's main.py`](https://github.com/LeStolz/THUD/blob/main/step3_data_analyzing/main.py) which performs the following steps:
1. Read and preprocess data
2. Profile data
3. Plot scatters
4. Plot averages
5. Perform regression analysis and calculate its R2 value

More details can be found at [`step 3's main.py`](https://github.com/LeStolz/THUD/blob/main/step3_data_analyzing/main.py).

## Step 4 Writing
### Purpose
The purpose of the step is to write about the results gathered from step 3.

### Input
The input of this step are:
- The files in the [`analytics`](https://github.com/LeStolz/THUD/tree/main/step3_data_analyzing/analytics) folder
- The png files in the [`step4_writting`](https://github.com/LeStolz/THUD/tree/main/step4_writing) folder
- The [`THUD.bib`](https://github.com/LeStolz/THUD/blob/main/step4_writing/THUD.bib) file which is used for citing

### Output
The output of this step is the [`THUD.pdf`](https://github.com/LeStolz/THUD/blob/main/step4_writing/THUD.pdf) file
compiled from the [`THUD.tex`](https://github.com/LeStolz/THUD/blob/main/step4_writing/THUD.tex) file.
