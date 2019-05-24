import requests
import re
from pyquery import PyQuery as pq
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
}
pageRequest = 'https://v.youku.com/page/playlist?showid={0}&isSimple=false&page={1}'

def getVideoDir(url):
    videoCsv = open('video.csv', 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(videoCsv)

    content = requests.get(url, headers=headers).text

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
                aDom = item('a.sn')
                link = 'https:'+ aDom.attr['href']

                print('【{2}】【{0}】【{1}】'.format(title,link, videoIndex))
                csv_writer.writerow((videoIndex,title,link))

                videoIndex += 1
            pageIndex += 1
        except Exception as e:
            print(e)
            break

    videoCsv.close()
    print('=======finish======')



videoUrl = 'https://v.youku.com/v_show/id_XMjcxNDk2NTkyNA';

if __name__ == "__main__":
    getVideoDir(videoUrl)
    pass

