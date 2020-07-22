from moviepy.editor import VideoFileClip, concatenate_videoclips
import requests
import os
import re
import time
import math
import json
from fake_useragent import UserAgent

_urlList = []
videoList = []

# header = {
#     'User-Agent': UserAgent("chrome").rget,
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#     "accept-encoding": "gzip, deflate, sdch, br",
#     "accept-language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
#     "cache-control": "no-cache"
# }
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'v.douyin.com',
    'Sec-Fetch-Dest': 'document',
    "Sec-Fetch-Mode": 'navigate',
    'Sec-Fetch-Site': 'none',
    'Upgrade-Insecure-Requests': '1',
    "cache-control": "no-cache",
    'User-Agent': UserAgent("chrome").rget,
}


# 读取文本文件
class ReadTxt(object):
    def __init__(self):
        if (os.path.isfile("foo.txt")):
            for line in open("foo.txt", "r", encoding='utf-8'):
                print(line)
                _urlList.append(line.strip('\n'))
        else:
            print("没有找到列表文件。")
        self.findList()

    # 匹配所有超链接
    def findList(self):
        # findall() 查找匹配正则表达式的字符串
        for line in _urlList:
            searchObj = re.search('https(.*)\/', line, re.M | re.I)
            if searchObj:
                url = searchObj.group()
                print(url)
                info, session = self.findViedoUrl(url)
                self.Download(info, session)
            else:
                url = ""
                print("正则表达式没有找到抖音短链接")

    # 打开链接获取真实视频和图片地址
    def findViedoUrl(self, url):
        session = requests.Session()
        res = session.get(url=url, timeout=5, headers=header, allow_redirects=False)

        print(res.status_code, " 打开状态 ", res.encoding)
        res.encoding = 'utf-8'
        print(res.headers['Location'])
        if (res.status_code == 302):
            url = res.headers['Location']
            items = url.split('/')
            # print(items)
        else:
            print("网址打开错误：没有返回302正确地址：", res.status_code)
        item_id = items[5]
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.iesdouyin.com',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

        }
        print(headers)
        url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + item_id
        res = session.get(url=url)
        res.encoding = 'utf-8'
        print(type(res.text),type(res.content))
        # n = json.dumps(res.text)
        n = json.loads(res.text)
        print(type(n))

        playAddr = n['item_list'][0]['video']['play_addr']['url_list'][0]
        cover = n['item_list'][0]['video']['origin_cover']['url_list'][0]
        filename = n['item_list'][0]['share_info']['share_title']

        return {
                   "playAddr": playAddr,
                   "cover": cover,
                   'filename': filename,
               }, session

    num = 0

    # 下载视频和图片
    def Download(self, info, session):
        self.num += 1
        head = {
            'User-Agent': UserAgent("chrome").rget,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, sdch, br",
            "accept-language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
            "cache-control": "no-cache"
        }
        try:
            videoBin = session.get(info['playAddr'], timeout=20, headers=head)
        except Exception as e:
            print("url地址：", info['playAddr'], "\n", "错误信息：", e)
            return
        print(videoBin.status_code, " 视频状态 ")
        filename = info['filename']
        mp4name = ""
        for i in range(0, 4 - len(str(self.num))):
            mp4name += "0"
        mp4name += str(self.num)
        if (os.path.exists('video') == False):
            print("创建目录 video")
            os.mkdir('video')  # 创建目录
        with open('video/%s.mp4' % (mp4name), 'wb') as fb:  # 将下载的视频保存到对应的文件夹中
            fb.write(videoBin.content)
            videoBin = session.get(info['cover'], timeout=5)
            with open('video/%s.jpg' % (filename), 'wb') as fb:  # 将下载的图片保存到对应的文件夹中
                fb.write(videoBin.content)
        time.sleep(2)


# 合并视频
class Merge(object):
    def __init__(self, w, h):
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

                    video = VideoFileClip(filePath).resize((w, h))

                    # 添加到数组
                    L.append(video)
        print(L)
        # 拼接视频
        final_clip = concatenate_videoclips(L)

        # 生成目标视频文件
        final_clip.to_videofile("./target.mp4", fps=30, remove_temp=False)
