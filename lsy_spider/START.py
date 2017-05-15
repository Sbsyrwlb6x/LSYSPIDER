# -*- coding: utf-8 -*-
import sys
import os
import datetime
from pymongo import MongoClient
from lsy_spider.weiboID import K
from lsy_spider.weiboID import getFileOrderByUpdate
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QMessageBox

now = datetime.datetime.now()
TT = "C:\\lsy_spider\\lsy_spider\\log\\" + now.strftime('%Y-%m-%d %H%M%S') + ".txt"
NPRILTT= "C:\\lsy_spider\\lsy_spider\\Chuli\\log\\" + now.strftime('%Y-%m-%d %H%M%S') + ".txt"
Datebase_name=""
Needtime=""
TFIDFbool=0
qtCreatorFile = "C:\\lsy_spider\\UI\\UI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CleanRedisThread(QtCore.QThread):
    '''新线程清空Redis'''
    trigger = QtCore.pyqtSignal(int)
    def __init__(self,parent=None):
        super(CleanRedisThread, self).__init__(parent)
    def run(self):
        #  cmdline.execute("scrapy crawl lsy_spider".split())
        if(os.system("python C:\\lsy_spider\\lsy_spider\\Clean.py"))==0:
            self.trigger.emit(0)
        else:
            self.trigger.emit(1)


class NlpirThread(QtCore.QThread):
    '''新线程开启Nlpir'''
    trigger = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(NlpirThread, self).__init__(parent)
    def run(self):
        #  cmdline.execute("scrapy crawl lsy_spider".split())
        os.system('python C:\lsy_spider\lsy_spider\Chuli\\nlpir_ui.py %s %s %s'%(Datebase_name,Needtime,TFIDFbool))

        self.trigger.emit()

class SpiderThread(QtCore.QThread):
    '''新线程开启Spider'''
    trigger = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(SpiderThread, self).__init__(parent)
    def run(self):
        #  cmdline.execute("scrapy crawl lsy_spider".split())
        os.system('python C:\lsy_spider\launch.py')
        self.trigger.emit()
class RedisThread(QtCore.QThread):
    '''新线程开启redis'''
    trigger = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(RedisThread, self).__init__(parent)
    def run(self):
        os.system('redis-server.exe')
        self.trigger.emit()
class Redis_2_Thread(QtCore.QThread):
    '''新线程关闭redis'''
    trigger = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(Redis_2_Thread, self).__init__(parent)
    def run(self):
        os.system('redis-cli shutdown')
        self.trigger.emit()
class MyDialog(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.runredisandspider)
        self.pushButton_2.clicked.connect(self.cleanredis)
        self.pushButton_3.clicked.connect(self.addcommobox1)
        # self.comboBox.activated.connect(self.commobox1)
        self.pushButton_4.clicked.connect(self.start_nlpir)
    def start_nlpir(self):
        global Datebase_name
        global TFIDFbool
        global Needtime
        if  self.comboBox.currentText()=="":
            QMessageBox.about(self,u"警告",u"请选择数据库")
        else:
            reply = QMessageBox.question(self, u'确认', u'是否选择了数据库'+self.comboBox.currentText()+u'进行分词',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply==QMessageBox.Yes:
                Datebase_name=self.comboBox.currentText()
                Needtime = str(self.dateEdit.date().year())+"-"+str(self.dateEdit.date().month())\
                       +"-"+str(self.dateEdit.date().day())+"="+str(self.spinBox.value()).zfill(2)
                if self.checkBox.isChecked():
                    TFIDFbool=1
                self.Thread1 = NlpirThread()
                self.Thread1.start()

    def addcommobox1(self):
        client = MongoClient('localhost', 27017)
        typelist=client.database_names()
        typelist.remove("admin")
        typelist.remove("cipin")
        typelist.remove("houqi")
        typelist.remove("Sinanew")
        typelist.remove("XXXX")
        typelist.remove("local")

        print typelist
        for i in typelist:
            self.comboBox.addItem(i)
    def test(self):
        print ""
    def cleanredis(self):
        self.Thread1=RedisThread()
        self.Thread1.start()
        self.Thread2 = CleanRedisThread()
        self.Thread2.trigger.connect(self.msg)
        self.Thread2.start()
        self.Thread3=Redis_2_Thread()
        self.Thread3.start()
    def msg(self,ls):
        if ls==0:
            QMessageBox.information(self,  # 使用infomation信息框
                                        u"info",
                                        u"成功清空redis判重队列!")
        else:
            QMessageBox.information(self,  # 使用infomation信息框
                                    u"info",
                                    u"清空redis判重队列失败!")

    def runredisandspider(self):
        self.Thread1 = RedisThread()
        self.Thread1.start()
        self.Thread2 = SpiderThread()
        self.Thread2.start()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.start()
        self.timer.timeout.connect(self.timeproc)

    def timeproc(self):
        self.cons.setText("")
        K=getFileOrderByUpdate("C:\\lsy_spider\\lsy_spider\\log")
        print "show :"+K
        f = open(K, "r")
        for line in f.readlines():
            self.cons.append(line)
        f.close()

    def closeEvent(self, event):
        '''重写关闭事件，关闭redis'''
        # if self._want_to_close:
        #     super(MyDialog, self).closeEvent(event)
        # else:
        event.accept()
        self.Thread1 = RedisThread()
        self.Thread1.start()
        os.system("redis-cli shutdown")
if __name__ == "__main__":
    F = open(TT, "w")
    F.write("#")
    F.close()
    # getFileOrderByUpdate("C:\\lsy_spider\\lsy_spider\\log")
    F = open(NPRILTT, "w")
    F.write("#")
    F.close()

    app = QtGui.QApplication(sys.argv)
    window = MyDialog()
    window.show()
    sys.exit(app.exec_())
