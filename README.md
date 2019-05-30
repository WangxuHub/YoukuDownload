# YoukuDownload

#### 介绍
优酷视频下载

#### 实现思路
使用selenium模拟用户登录和观看视频，捕获.m3u8(视频文件)、.ass(字幕文件)。最后将.m3u8下载转换为.ts文件，使用ffmpeg进行.ts文件和.ass字幕文件整合

#### 使用说明
首先输入优酷的vip账号，重命名 youkuAccount.demo.py 为 youkuAccount.py，将优酷账号密码填入对应的位置

##### 抓取单个视频
<pre>py main.py</pre>

