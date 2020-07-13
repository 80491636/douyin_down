from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
import sys
from mainwindow import Ui_MainWindow
from VideoEdit import ReadTxt, Merge
import time

class mywindow(QMainWindow, Ui_MainWindow):
    def  __init__ (self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        w = self.w_txt.setText("720")
        h = self.h_txt.setText("1280")
        self.notice_label.setText("请将需要下载的视频分享链接放到当前目录下foo.txt文件中。")
        self.log_label.setText("准备就绪")
    # 开始下载
    def start_bt(self):
        self.log_label.setText("开始下载")

        self.thread_1 = ThreadDemo()
        self.thread_1.trigger.connect(self.print_in_textEdit)
        self.thread_1.start()
        
        self.log_label.setText("下载完成")

    def merge_bt(self):
        self.log_label.setText("正在合并视频")
        w = self.w_txt.text()
        h = self.h_txt.text()
        mer = Merge(w,h)
        self.log_label.setText("视频合并完成")

    def print_in_textEdit(self, msg):
        # time.sleep(5)
        self.log_label.setText(msg)
        self.thread_1.exit()

class ThreadDemo(QThread):
    trigger = pyqtSignal(str)
 
    def __init__(self):
        super(ThreadDemo, self).__init__()
 
    def run(self):
        # for i in range(10):
        #     print(i)
        #     self.trigger.emit(str(i))
        #     time.sleep(1)
        readt = ReadTxt()


if __name__ == "__main__":
    # 启动窗口
    app = QApplication(sys.argv)
    MainWindow = mywindow()
    MainWindow.setWindowTitle("抖音下载拼接助手1.0")
    MainWindow.down_btn.clicked.connect(MainWindow.start_bt)
    MainWindow.merge_btn.clicked.connect(MainWindow.merge_bt)
    MainWindow.show()
    sys.exit(app.exec_())
    
