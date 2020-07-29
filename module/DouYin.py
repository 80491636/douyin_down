#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DouYin.py    
@Contact :   80491636@qq.com
@Modify Time :   2020/7/28 15:41 
--------------------------------------
'''
import json,time
import os, requests
from moviepy.editor import VideoFileClip, concatenate_videoclips
from PyQt5.QtCore import QThread, pyqtSignal


class SplitJson(QThread):
    trigger = pyqtSignal(list)

    def __init__(self, _path):
        super(SplitJson, self).__init__()
        self.path = _path
        self.videos_list = os.listdir(_path)  # 获取文件夹内所有json包名

    def run(self):
        datas = []
        for videos in self.videos_list:  # 循环json列表，对每个json包进行操作
            a = open(self.path + '{}'.format(videos), encoding='utf-8')  # 打开json包
            content = json.load(a)['aweme_list']  # 取出json包中所有视频

            for video in content:  # 循环视频列表，选取每个视频
                print(video)
                dict = {}
                dict['aweme_id'] = video['aweme_id']

                try:
                    dict['sec_uid'] = video['music']['sec_uid']
                except Exception as e:
                    dict['sec_uid'] = 'None'

                dict['uid'] = video['author']['uid']
                dict['short_id'] = video['author']['short_id']
                dict['nickname'] = video['author']['nickname']  # 用户名称
                dict['title'] = video['desc']  # 视频标题
                dict['signature'] = video['author']['signature']  # 视频简介
                dict['avatar_larger'] = video['author']['avatar_larger']['url_list'][0]  # 缩略图地址
                dict['video_url'] = video['video']['play_addr']['url_list'][0]  # 获取视频url，每个视频有6个url，我选的第5个
                datas.append(dict)

        self.trigger.emit(datas)


class Download(QThread):
    trigger = pyqtSignal(str,list)

    def __init__(self, _datas, _path):
        super(Download, self).__init__()
        self.datas = _datas  # 获取文件夹内所有json包名
        self.path = _path
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}

    def run(self):

        if type(self.datas) == dict:
            self.datas = [self.datas]
            self.down(self.datas)
        else:
            self.down(self.datas)
        self.trigger.emit("视频下载完成",self.datas)

    def down(self, _list):
        for data in _list:
            video_url = data['video_url']
            file_name = data['title']
            img_url = data['avatar_larger']
            try:
                videoMp4 = requests.request('get', video_url, headers=self.headers).content  # 获取视频二进制代码
            except Exception as e:
                print("下载视频遇到错误：",e)
            with open(self.path + '{}.mp4'.format(file_name), 'wb') as f:  # 以二进制方式写入路径，记住要先创建路径
                f.write(videoMp4)  # 写入
                print('视频:{}下载完成'.format(file_name))  # 下载提示
            try:
                imgJpg = requests.request('get', img_url, headers=self.headers).content  # 获取图片二进制代码
            except Exception as e:
                print("下载图片遇到错误：",e)
            with open(self.path + '{}.jpg'.format(file_name), 'wb') as f:  # 以二进制方式写入路径，记住要先创建路径
                f.write(imgJpg)  # 写入
                print('图片:{}下载完成'.format(file_name))  # 下载提示


# 合并视频
class JoinVideo(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, _w, _h, _path):
        super(JoinVideo, self).__init__()
        # 定义一个数组
        self.L = []
        self.width = _w
        self.height = _h
        self.path = _path

    def run(self):

        # 访问 video 文件夹 (假设视频都放在这里面)
        for root, dirs, files in os.walk(self.path):
            print(root)
            # 按文件名排序
            files.sort()
            # 遍历所有文件
            for file in files:
                # 如果后缀名为 .mp4
                if os.path.splitext(file)[1] == '.mp4':
                    # 拼接成完整路径
                    filePath = os.path.join(root, file)
                    # 载入视频

                    video = VideoFileClip(filePath).resize((self.width, self.height))

                    # 添加到数组
                    self.L.append(video)
        print(self.L)
        # 拼接视频
        final_clip = concatenate_videoclips(self.L)

        # 生成目标视频文件
        file_name = time.strftime("%Y-%m-%d%H%M%S", time.localtime())
        final_clip.to_videofile( self.path + file_name + ".mp4", fps=30, remove_temp=False)
        self.trigger.emit("视频拼接完成")
