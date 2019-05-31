import moviepy
import imageio
import requests
import re
import os
import sys
import tqdm
import time

# 92.22
def test1():
    os.system(r'.\tools\ffmpeg.exe -i .\TestData\2.ts -y .\TestData\2.mp4')

def test2():
    # ffmpeg -c:v h264_cuvid -i 1.mp4 -s 1280:720 -r 29.97 -b:v 600k -c:v h264_nvenc  1-1.mp4 

    # Supported hwaccels: cuda dxva2 qsv d3d11va qsv cuvid   ,  -hwaccel 
    #os.system(r'.\tools\ffmpeg.exe -hwaccel dxva2  -y -i .\TestData\2.ts  .\TestData\2.mp4')
    
    # 104
    # os.system(r'.\tools\ffmpeg.exe -hwaccel dxva2 -y -i .\TestData\2.ts .\TestData\2.mp4')

    # 105
    # os.system(r'.\tools\ffmpeg.exe -hwaccel auto  -y -i .\TestData\2.ts .\TestData\2.mp4')
    os.system(r'.\tools\ffmpeg.exe -y -i .\TestData\2.ts -c:v h264_amf .\TestData\2.mp4')
    
    #-c:v h264_amf 
    pass    

t1 = time.time()

#test1()
test2()

t2 = time.time()

print(t2-t1)
