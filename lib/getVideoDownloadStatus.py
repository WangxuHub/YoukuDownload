import csv
import os

csvFile = 'video.csv'

def getUnDownLoadItem():
    '''
        获取未下载的影集
    '''
    
    curRow = []
    videoCsv = open(csvFile, 'r', newline='', encoding='utf-8')
    csv_reader = csv.reader(videoCsv)

    for item in csv_reader:
        if len(item) == 3:
            curRow = item
            break

    videoCsv.close()
    return curRow

def updateDownLoadItem(row):
    '''
        更新已经下载好的视频记录
    '''
    csvData = []
     
    with open(csvFile, 'r', newline='', encoding='utf-8') as videoCsv:
        csv_reader = csv.reader(videoCsv)

        for item in csv_reader:
            csvData.append(item)

    csvData[int(row[0])-1] = row
    
    with open(csvFile, 'w', newline='', encoding='utf-8') as videoCsv:
        csv_writer = csv.writer(videoCsv)

        for item in csvData:
            csv_writer.writerow(item)

# if not os.path.exists(csvFile):
#     return

    # csvData = []
    # for item in csv_reader:
    #     csvData.append(item)

# csvData[match].append('asdasdasd')

# tempCsvFile = 'video.csv'
# tmepVideoCsv = open(csvFile, 'w', newline='', encoding='utf-8')
# csv_reader = csv.reader(videoCsv)

# for item in csvData:
#     csv_writer.writerow(item)

data = getUnDownLoadItem()
print(data)

data.append('xzcxzcxzc')
updateDownLoadItem(data)
