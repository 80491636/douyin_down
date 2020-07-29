#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Main.py    
@Contact :   80491636@qq.com
@Modify Time :   2020/7/23 16:39 
--------------------------------------
'''
import os, json, requests, sys
import re

from module.SQLSer import SqlSer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from mainwindow import Ui_MainWindow
from module.DouYin import SplitJson, Download, JoinVideo


# UI类
class mywindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.count = 0
        self.textE_width.setText('576')
        self.textE_height.setText('1024')
        self.label.setText("启动成功")
        self.sql = SqlSer()

    def splitClick(self):
        '''
        分割视频
        :return:
        '''
        self.split = SplitJson('G:/抖音下载与合并/raw_data/')
        self.split.start()
        self.split.trigger.connect(self.endSplit)
        self.label.setText("分析json中...")

    def oneDownClick(self):
        '''
        下载选中视频
        :return:
        '''
        self.onedown = Download(self.datas[self.count],"G:/抖音下载与合并/down/")
        self.onedown.start()
        self.onedown.trigger.connect(self.endDwon)
        self.label.setText("正在下载视频")

    def allDownClick(self):
        '''
        下载所有视频
        :return:
        '''
        self.alldown = Download(self.datas,"G:/抖音下载与合并/down/")
        self.alldown.start()
        self.alldown.trigger.connect(self.endDwon)
        self.label.setText("正在下载所有视频")

    def joinClick(self):
        '''
        拼接视频
        :return:
        '''
        self.joinvideo = JoinVideo(self.textE_width.toPlainText(),self.textE_height.toPlainText(),"G:/抖音下载与合并/video/")
        self.joinvideo.start()
        self.joinvideo.trigger.connect(self.endDwon)
        self.label.setText("拼接视频中...")

    def listWClick(self):
        self.count = self.listWidget.currentRow()
        txt = self.listWidget.item(self.count).text()
        print(txt)

    def endSplit(self, _datas):
        print("分割JSON文件完成：", _datas)
        self.datas = _datas
        for i in range(len(_datas)):
            items = _datas[i]
            self.listWidget.addItem(items['title'])
        self.listWidget.setCurrentRow(self.count)
        self.label.setText("分割JSON文件完成...")

    def endDwon(self, _str,_list = None):
        '''
        下载结束回调
        :param _str: 函数正常结束文本
        :param _list:下载的视频数据
        :return:
        '''
        self.label.setText(_str)
        if _list == None:
            return

        for video in _list:
            aweme_id = video['aweme_id']
            try:
                sec_uid = video['sec_uid']
            except Exception as e:
                sec_uid = 'None'
            uid = video['uid']
            short_id = video['short_id']
            nickname = video['nickname']  # 用户名称
            title = video['title']  # 视频标题
            signature = video['signature']  # 视频简介
            avatar_larger = video['avatar_larger']  # 缩略图地址
            video_url = video['video_url']  # 获取视频url，每个视频有6个url，我选的第5个

            title = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", " ", title)
            signature = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", " ", signature)
            nickname = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", " ", nickname)

            self.sql.addData(aweme_id, sec_uid, uid, short_id, title, nickname, signature, avatar_larger, video_url)


if __name__ == '__main__':
    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    # QWidget部件是pyqt5所有用户界面对象的基类。他为QWidget提供默认构造函数。默认构造函数没有父类。
    w = mywindow()
    # 按钮事件
    w.btn_splitVideo.clicked.connect(w.splitClick)
    w.btn_downVideo.clicked.connect(w.oneDownClick)
    w.btn_downAll.clicked.connect(w.allDownClick)
    w.btn_joinVideo.clicked.connect(w.joinClick)
    w.listWidget.clicked.connect(w.listWClick)

    # 设置窗口的标题
    w.setWindowTitle('抖音视频下载2.0')
    # 显示在屏幕上
    w.show()
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())
