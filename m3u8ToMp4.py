import moviepy
import imageio
import requests
import re
import os
import sys
import tqdm

# imageio.plugins.ffmpeg.download()

def m3u8ToMp4():
    cmdStr ='.\tools\ffmpeg.exe -protocol_whitelist "file,http,https,rtp,udp,tcp,tls"  -i .\TestData\demo.m3u8 .\hy\demo.mp4'
    os.system()
    pass

def downloadTs(m3u8File, saveTsFile):
    m3u6Content = ''
    with open(m3u8File, 'r') as f:
        m3u6Content = f.read()
    
    tsLinkArr = re.findall( r'(http.*)', m3u6Content, re.I|re.M)
    
    dir = os.path.dirname(saveTsFile)
    if not os.path.isdir(dir):
        os.makedirs(dir)

    name = os.path.basename(m3u8File)
    for index,item  in enumerate(tsLinkArr):
        tsContent = requests.get(item).content
        if index == 0:
            with open(saveTsFile, 'wb') as f:
                f.write(tsContent)
        else:
            with open(saveTsFile, 'ab+') as f:
                f.write(tsContent)
        
        done = (index+1) / len(tsLinkArr) * 100
        processLength = int(done/2)
        sys.stdout.write("\r%s:[%s%s] %d%%" % (name, '█' * processLength, ' ' * (50 - processLength), done))
        sys.stdout.flush()


downloadTs('TestData/demo.m3u8', 'hy/tsDownload/demo.ts')
