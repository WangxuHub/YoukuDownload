import moviepy
import imageio
import os

# imageio.plugins.ffmpeg.download()

def m3u8ToMp4():
    cmdStr ='.\tools\ffmpeg.exe -protocol_whitelist "file,http,https,rtp,udp,tcp,tls"  -i .\TestData\demo.m3u8 .\hy\demo.mp4'
    os.system()
    pass