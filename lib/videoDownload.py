import csv
import os
import requests
import re
from pyquery import PyQuery as pq

class VideoDownload:
    def __init__(self, videoGroupName, videoUrl):
        self.__videoGroupName = videoGroupName
        self.__videoUrl = videoUrl

    # 获取当前保存视频下载进度的csv名称
    def getCsvFile(self):
        '''
            获取当前保存视频下载进度的csv名称
        '''
        return 'download/' + self.__videoGroupName + '/video.csv'

    # 获取未下载的视频
    def getUnDownLoadItem(self):
        '''
            获取未下载的影集
        '''

        csvFile = self.getCsvFile()

        curRow = []
        with open(csvFile, 'r', newline='', encoding='utf-8') as videoCsv:
            csv_reader = csv.reader(videoCsv)

            for item in csv_reader:
                if len(item) == 3:
                    curRow = item
                    break

        return curRow

    # 更新当前视频下载的进度
    def updateDownLoadItem(self, row):
        '''
            更新已经下载好的视频记录
        '''
        csvFile = self.getCsvFile()
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

    # 初始化视频csv状态集合
    def initVideoCsv(self):
        '''
            初始化视频csv状态集合
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        }
        pageRequest = 'https://v.youku.com/page/playlist?showid={0}&isSimple=false&page={1}'

        csvFile = self.getCsvFile()

        csvDir = os.path.dirname(csvFile)

        if not os.path.isdir(csvDir):
            os.makedirs(csvDir)

        videoCsv = open(csvFile, 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(videoCsv)

        content = requests.get(self.__videoUrl, headers=headers).text

        showid = re.search('showid: \'(.*)\',',content).group(1)

        videoIndex = 1
        pageIndex = 1
        while True:
            try:
                jsonData = requests.get(pageRequest.format(showid, pageIndex)).json()
                htmlContent = jsonData['html']
                
                doc = pq(htmlContent)

                list = doc('div.item.item-cover')

                if list == None:
                    break

                for item in list.items():
                    title = item.attr['title']
                    link = 'https:'+ item('a.sn').attr['href']

                    safeFileName = self.__safeFileName(title)
                    csv_writer.writerow((videoIndex, safeFileName, link))

                    videoIndex += 1
                pageIndex += 1
            except:
                pass

        videoCsv.close()

    def __safeFileName(self, fileName):
        retStr = re.sub('[\/:*?"<>|]','-', fileName) #去掉非法字符  
        
        return retStr




