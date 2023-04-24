"""
1.remove testDate, url, socket
2.Nếu ko có release date và không có price thì xóa
3.Lấy từ 2017-2023
4.Chuyển kiểu dữ liệu hợp lí(release date, ) + lastPrice chuyển ngày tháng về double
5.merge price vào Prices *xóa trùng  rồi sort theo ngày tháng rồi xóa price

*Chú ý: chỗ ko có ghi Na có chỗ thì để trống
cleaning data: 
    *Hàm chuyển sang mili(s) của python + 13 = thời gian được đổi trong data (trong data giờ định dạng là 06:00:00)
    Loại bỏ các thuộc tính không cần thiết như "Test Date", "Socket", "URL", "Value", "Thread Value". Ngoài ra, loại bỏ thêm các dòng
có cả 'Release Date', 'Price' đều rỗng.
    Tiếp đến, tiến hành loại bỏ các dòng sản phẩm nằm ngoài khoảng thời gian 2017-2023 nhưng vì release date được thể hiện dưới 
đơn vị Miliseconds nên cần tiến hành chuyển chúng về kiểu datetime để cùng kiểu dữ liệu dễ dàng cho việc so sánh và loại bỏ.
    Ngoài ra, tiến hành chuyển đổi các thuộc tính về kiểu dữ liệu phù hợp.
"""


import pandas as pd
import regex as re
import datetime as dt
from datetime import datetime, timedelta
import numpy as np
import math

file_name_1 = 'C:/Users/Dell/Desktop/Python/clean/THUD/step1_data_crawling/data_csv/cpu.csv'
file_name_2 = 'C:/Users/Dell/Desktop/Python/clean/THUD/step1_data_crawling/data_csv/gpu.csv'

def cleanning_at_Price_col(df):
    Price = df['Price'].str.findall(r"\$(\d+\,?\d*\.?\d+)[\s\w]+\((\d+-\d+-\d+)\)")
    
    Price = Price.tolist()
    
    Result = []
    
    for i in  range (0, len(Price)):
        
        #convert tuple to list
        Price[i][0] = list(Price[i][0])
        #replace ',' -> '.'
        Price[i][0][0] = Price[i][0][0].replace(',', '')
        #convert string to float in each list
        Price[i][0][0] = float(Price[i][0][0])  
        
        Result.append(Price[i][0])
    
    df.drop(columns=["Price"], inplace = True)
    
    df['Price'] = Result
    
    return df

def cpu_file_handling():
    cpu = pd.read_csv(file_name_1, index_col=[0])
    
    #step 1
    cpu.drop(columns=["Test Date", "Socket", "URL", "Value", "Thread Value"], inplace=True)
    
    #step 2
    cpu.dropna(subset=['Release Date', 'Price'], how = 'all', inplace=True)
    
    #step 3
    release_date = []

    #int -> datetime
    for value in cpu['Release Date']:
        if math.isnan(value):
           release_date.append(None)
        else: 
            release_date.append(datetime.fromtimestamp(value / 1000).date())
        
    cpu.drop(columns=["Release Date"], inplace=True)
    cpu['Release Date'] = release_date
    cpu['Release Date'] = pd.to_datetime(cpu['Release Date'])
    
    cpu = cpu.loc[(cpu['Release Date'] >= '2017-01-01') & (cpu['Release Date'] < '2023-12-31')]
    
    #step 4
    cpu = cleanning_at_Price_col(cpu)
    
    #change type of Mark
    Mark = cpu['Mark'].str.replace(r',', '.', regex = True)
    cpu.drop(columns=["Mark"], inplace=True)
    cpu['Mark'] = Mark
    cpu['Mark'] = cpu['Mark'].astype(float)
    
    #change type of ThreadMark
    Thread_Mark = cpu['Thread Mark'].str.replace(r',', '.', regex = True)
    cpu.drop(columns=["Thread Mark"], inplace=True)
    cpu['Thread Mark'] = Thread_Mark
    cpu['Thread Mark'] = cpu['Thread Mark'].astype(float)
    
    
def main():
    cpu_file_handling()



if __name__ == '__main__':
	main()