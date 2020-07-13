from moviepy.editor import VideoFileClip,concatenate_videoclips
import requests
import os
import re
import time
import math
from fake_useragent import UserAgent

_urlList = []
videoList = []

header = {
    'User-Agent': UserAgent("chrome").rget,
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding":"gzip, deflate, sdch, br",
    "accept-language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
    "cache-control":"no-cache"
}
# 读取文本文件
class ReadTxt(object):
    def __init__(self):
        if( os.path.isfile("foo.txt") ):
            for line in open( "foo.txt" ):   
                print(line)
                _urlList.append(line.strip('\n'))
        else:
            print("没有找到列表文件。")
        self.findList()
    # 匹配所有超链接
    def findList(self): 
        # findall() 查找匹配正则表达式的字符串
        for line in _urlList:
            searchObj = re.search( 'https(.*)\/', line, re.M|re.I)
            if searchObj:
                url =  searchObj.group()
                print(url)
                info,session = self.findViedoUrl(url)
                self.Download(info,session)
            else:
                url = ""
                print ("正则表达式没有找到抖音短链接")
    # 打开链接获取真实视频和图片地址
    def findViedoUrl(self,url):
        session = requests.Session()
        res = session.get(url = url , timeout = 5 , headers = header)
        print(res.status_code," 打开状态 ",res.encoding)
        res.encoding = 'utf-8'
        print(res.text)
        data = res.text
        
        searchObj = re.search( 'playAddr\: \"(.*)\"\,', data, re.M|re.I)
        if searchObj:
            # playAddr = searchObj.group(1).replace("/playwm/","/play/")
            playAddr = searchObj.group(1)
        else:
            playAddr = ""
        searchObj = re.search( 'cover\: \"(.*)\"', data, re.M|re.I)
        if searchObj:
            cover = searchObj.group(1)
        else:
            cover = ""
        searchObj = re.search( '\<p class=\"desc\"\>(.*?)</p>', data, re.M|re.I)
        if searchObj:
            filename = searchObj.group(1)
        else:
            filename = ""
        if filename == "":
            filename = math.floor( time.time() )
        print(
            {
            "playAddr": playAddr,
            "cover": cover,
            'filename': filename,
        }
        )
        return {
            "playAddr": playAddr,
            "cover": cover,
            'filename': filename,
        },session
    num = 0
    # 下载视频和图片
    def Download(self,info,session):
        self.num += 1
        head = {
            'User-Agent': UserAgent("chrome").rget,
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-encoding":"gzip, deflate, sdch, br",
            "accept-language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
            "cache-control":"no-cache"
        }
        videoBin = session.get( info['playAddr'],timeout=20, headers = head )
        print(videoBin.status_code," 视频状态 ")
        filename = info['filename']
        mp4name = ""
        for i in range(0, 4 - len(str(self.num)) ):
            mp4name += "0"
        mp4name += str(self.num) 
        if( os.path.exists('video') == False ):
            print("创建目录 video")
            os.mkdir('video') #创建目录
        with open('video/%s.mp4' % (mp4name),'wb') as fb: # 将下载的视频保存到对应的文件夹中
            fb.write(videoBin.content)
            videoBin = session.get( info['cover'],timeout=5, headers = header )
            with open('video/%s.jpg' % (filename),'wb') as fb: # 将下载的图片保存到对应的文件夹中
                fb.write(videoBin.content)
        time.sleep(2)

# 合并视频
class Merge(object):
    def __init__(self,w,h):
        # 定义一个数组
        L = []
        
        # 访问 video 文件夹 (假设视频都放在这里面)
        for root, dirs, files in os.walk("./video"):
            # 按文件名排序
            files.sort()
            # 遍历所有文件
            for file in files:
                # 如果后缀名为 .mp4
                if os.path.splitext(file)[1] == '.mp4':
                    # 拼接成完整路径
                    filePath = os.path.join(root, file)
                    # 载入视频
                    video = VideoFileClip(filePath).resize( (w,h) )
                    # 添加到数组
                    L.append(video)
        print(L)
        # 拼接视频
        final_clip = concatenate_videoclips(L)
        
        # 生成目标视频文件
        final_clip.to_videofile("./target.mp4", fps=30, remove_temp=False)

