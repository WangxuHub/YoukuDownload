import os
import sys
import time
from threading import Thread

import lib.videoDownload as videoDownload
import lib.chromeCatch as chromeCatch
# 抓取优酷视频

videoGroupName = '火影忍者《博人传》'
videoHomeUrl = 'https://v.youku.com/v_show/id_XMjcwMTA4Mzg2MA==.html'

def start():
    videoHelper = videoDownload.VideoDownload(videoGroupName, videoHomeUrl)

    # 如果不存在文件，则初始化csv文件
    if not os.path.exists(videoHelper.getCsvFile()):
        videoHelper.initVideoCsv()
        print('初始化csv文件 {0} 完成'.format(videoHelper.getCsvFile()))

    chromeCatch.ChromeCatch.login()
    time.sleep(3)

    # 下载m3u8 和 ass 文件
    def downloadM3u8():
        while True:
            curVideoItem = videoHelper.getUnDownLoadM3u8Item()
            if len(curVideoItem) == 0:
                break

            chromeHandler = chromeCatch.ChromeCatch(
                curVideoItem[0], curVideoItem[1], curVideoItem[2], videoGroupName)

            try:
                chromeHandler.downloadVideoMidFile()
                curVideoItem.append('m3u8')
            except Exception as e:
                curVideoItem.append('fail:'+e)

            videoHelper.updateDownLoadItem(curVideoItem)

    def downloadTs():
        while True:
            curVideoItem = videoHelper.getUnDownLoadTsItem()
            if len(curVideoItem) == 0:
                break

            videoIndex = curVideoItem[0]
            videoName = curVideoItem[1]
            
            m3u8File = videoHelper.getFileM3u8Path(videoIndex, videoName)
            tsFile = videoHelper.getFileTsPath(videoIndex, videoName)

            try:
                curVideoItem.append('downloading')
                videoHelper.updateDownLoadItem(curVideoItem)

                videoHelper.downloadTs(m3u8File, tsFile)
                curVideoItem[4] = 'ts'
            except Exception as e:
                curVideoItem[4]('fail:'+str(e))

            videoHelper.updateDownLoadItem(curVideoItem)
    
    def convertTsToMp4():
        while True:
            curVideoItem = videoHelper.getUnConvertTsItem()
            if len(curVideoItem) == 0:
                break

            try:
                curVideoItem.append('converting')
                videoHelper.updateDownLoadItem(curVideoItem)

                videoHelper.convertTsToMp4(curVideoItem[0], curVideoItem[1])
                curVideoItem[5]('mp4')
            except Exception as e:
                curVideoItem[5]('fail:'+e)

            videoHelper.updateDownLoadItem(curVideoItem)

    downloadM3u8()

    
    threadCount = 1

    threads = []
    for i in range(threadCount):
        # TODO: 线程锁未加上，出现了数据竞争
        threads.append(Thread(target=downloadTs))

    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

    convertTsToMp4()
    print('======================finish=======================')
    # downloadTs()
    print('视频下载完毕')

if __name__ == "__main__":
    if len(sys.argv) >1:
        videoGroupName = sys.argv[1]
        videoHomeUrl = sys.argv[2]

    start()


