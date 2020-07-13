'''
@Author: your name
@Date: 2020-06-16 14:48:04
'''
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(392, 279)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.notice_label = QtWidgets.QLabel(self.centralwidget)
        self.notice_label.setGeometry(QtCore.QRect(20, 20, 351, 31))
        self.notice_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.notice_label.setObjectName("notice_label")
        self.down_btn = QtWidgets.QPushButton(self.centralwidget)
        self.down_btn.setGeometry(QtCore.QRect(240, 80, 75, 23))
        self.down_btn.setObjectName("down_btn")
        self.merge_btn = QtWidgets.QPushButton(self.centralwidget)
        self.merge_btn.setGeometry(QtCore.QRect(240, 130, 75, 23))
        self.merge_btn.setObjectName("merge_btn")
        self.w_txt = QtWidgets.QLineEdit(self.centralwidget)
        self.w_txt.setGeometry(QtCore.QRect(90, 80, 91, 20))
        self.w_txt.setText("")
        self.w_txt.setObjectName("w_txt")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 61, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 130, 61, 16))
        self.label_3.setObjectName("label_3")
        self.h_txt = QtWidgets.QLineEdit(self.centralwidget)
        self.h_txt.setGeometry(QtCore.QRect(90, 130, 91, 20))
        self.h_txt.setText("")
        self.h_txt.setObjectName("h_txt")
        self.log_label = QtWidgets.QLabel(self.centralwidget)
        self.log_label.setGeometry(QtCore.QRect(20, 160, 351, 61))
        self.log_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.log_label.setObjectName("log_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 392, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.notice_label.setText(_translate("MainWindow", "TextLabel"))
        self.down_btn.setText(_translate("MainWindow", "开始下载"))
        self.merge_btn.setText(_translate("MainWindow", "合成视频"))
        self.label_2.setText(_translate("MainWindow", "视频宽度:"))
        self.label_3.setText(_translate("MainWindow", "视频高度:"))
        self.log_label.setText(_translate("MainWindow", "TextLabel"))
