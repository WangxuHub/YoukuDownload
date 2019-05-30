import os
import sys
import time

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

    while True:
        curVideoItem = videoHelper.getUnDownLoadItem()
        if len(curVideoItem) == 0:
            break

        chromeHandler = chromeCatch.ChromeCatch(
            curVideoItem[0], curVideoItem[1], curVideoItem[2], videoGroupName)

        chromeHandler.downloadVideoMidFile()

        curVideoItem.append('m3u8')
        videoHelper.updateDownLoadItem(curVideoItem)

    print('视频下载完毕')


if __name__ == "__main__":
    if len(sys.argv) >1:
        videoGroupName = sys.argv[1]
        videoHomeUrl = sys.argv[2]

    start()


