import csv
import os

#输出数据写入CSV文件
data = [
    ("Mike", "male", 24),
    ("Lee", "male", 26),
    ("Joy", "female", 22)
]

#Python3.4以后的新方式，解决空行问题
with  open('write.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for list in data:
        print(list)
        csv_writer.writerow(list)