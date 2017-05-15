# -*- coding: utf-8 -*-
import sys
import os
import datetime
import webbrowser
from pymongo import MongoClient
from lsy_spider.weiboID import getFileOrderByUpdate2
from lsy_spider.weiboID import getFileOrderByUpdate
from PyQt4 import QtCore, QtGui, uic,QtWebKit
from PyQt4.QtGui import QMessageBox
from bson.objectid import ObjectId
from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import QUrl
# reload(sys)
# sys.setdefaultencoding('utf8')
now = datetime.datetime.now()
TT = "C:\\lsy_spider\\lsy_spider\\log\\" + now.strftime('%Y-%m-%d %H%M%S') + ".txt"
NPRILTT= "C:\\lsy_spider\\lsy_spider\\Chuli\\log\\" + now.strftime('%Y-%m-%d %H%M%S') + ".txt"
Datebase_name=""
Needtime=""
TFIDFbool=0
Kmeansbool=0
numcu=20
qtCreatorFile = "C:\\lsy_spider\\UI\\UI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyBrowser(QtGui.QWidget):

    def __init__(self, parent = None):
        super(MyBrowser, self).__init__(parent)
        self.createLayout()
        self.createConnection()

    def search(self):
        address = str(self.addressBar.text())
        if address:
            if address.find('://') == -1:
                address = 'http://' + address
            url = QUrl(address)
            self.webView.load(url)

    def createLayout(self):
        self.setWindowTitle("keakon's browser")

        self.addressBar = QtGui.QLineEdit()
        self.goButton = QtGui.QPushButton("&GO")
        bl = QtGui.QHBoxLayout()
        bl.addWidget(self.addressBar)
        bl.addWidget(self.goButton)

        self.webView = QWebView()

        layout = QtGui.QVBoxLayout()
        layout.addLayout(bl)
        layout.addWidget(self.webView)

        self.setLayout(layout)

    def createConnection(self):
        self.connect(self.addressBar, QtCore.SIGNAL('returnPressed()'), self.search)
        self.connect(self.addressBar, QtCore.SIGNAL('returnPressed()'), self.addressBar, QtCore.SLOT('selectAll()'))
        self.connect(self.goButton, QtCore.SIGNAL('clicked()'), self.search)
        self.connect(self.goButton, QtCore.SIGNAL('clicked()'), self.addressBar, QtCore.SLOT('selectAll()'))
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
        os.system('python C:\lsy_spider\lsy_spider\Chuli\\nlpir_ui.py %s %s %s %s %d'%(Datebase_name,Needtime,TFIDFbool,Kmeansbool,numcu))
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
class MyPage(QtWebKit.QWebPage):
    def __init__(self, parent=None):
        super(MyPage, self).__init__(parent)
    def triggerAction(self, action, checked=False):
        if action == QtWebKit.QWebPage.OpenLinkInNewWindow:
            self.createWindow(QtWebKit.QWebPage.WebBrowserWindow)

        return super(MyPage, self).triggerAction(action, checked)

class MyWindow(QtWebKit.QWebView):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.myPage = MyPage(self)
        self.setPage(self.myPage)
    def createWindow(self, windowType):
        if windowType == QtWebKit.QWebPage.WebBrowserWindow:
            self.webView = MyWindow()
            self.webView.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

            return self.webView

        return super(MyWindow, self).createWindow(windowType)
class NewDialog(QtGui.QWidget):
    def __init__(self,parent=None):
        super(NewDialog, self).__init__(parent)
    def display(self,ID,database):
        self.MyTable=QtGui.QTableWidget()
        self.MyTable.setColumnCount(2)
        self.MyTable.setRowCount(13)
        self.MyTable.setHorizontalHeaderLabels([u'Key', u'Value'])
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.MyTable)
        self.setLayout(layout)
        client=MongoClient("localhost",27017)
        db=client[str(database)]
        post=db["Information"]
        i=0
        for x in post.find({"_id":str(ID)}):
            for key in x:
                self.MyTable.setItem(i, 0, QtGui.QTableWidgetItem(key))
                self.MyTable.setItem(i, 1, QtGui.QTableWidgetItem(unicode(x[key])))
                i=i+1
        self.MyTable.setColumnWidth(0, 150)
        self.MyTable.setColumnWidth(1, 300)
class MyDialog(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.runredisandspider)
        self.pushButton_2.clicked.connect(self.cleanredis)
        self.pushButton_3.clicked.connect(self.addcommobox1)
        self.comboBox_2.activated.connect(self.combobox2)
        self.comboBox_3.activated.connect(self.combobox3)
        self.pushButton_4.clicked.connect(self.start_nlpir)
        self.pushButton_5.clicked.connect(self.addcommobox2)
        self.comboBox_4.addItem(u"Kmeans聚类算法")
        self.comboBox_4.addItem(u"Kmeans++聚类算法")
        self.tableWidget.itemClicked.connect(self.clickwidget)
        self.pushButton_6.clicked.connect(self.clickmore1)
        self.pushButton_7.clicked.connect(self.clickmore2)
        self.pushButton_8.clicked.connect(self.clickmore3)
    def clickmore3(self):
        if self.comboBox_3.currentText()=="":
            QMessageBox.about(self, u"警告", u"请选择类簇!")
            return ""
        client = MongoClient('localhost', 27017)
        db = client[str(self.comboBox_2.currentText().split(":")[3])]
        post = db["Tweets"]
        data = [[0, 0, 0]]
        for x in post.find():
            try:
                if x["PubTime"].split(" ")[0] == u"04月17日":
                    i = 0
                elif x["PubTime"].split(" ")[0] == u"04月18日":
                    i = 1
                elif x["PubTime"].split(" ")[0] == u"04月19日":
                    i = 2
                elif x["PubTime"].split(" ")[0] == u"04月20日":
                    i = 3
                elif x["PubTime"].split(" ")[0] == u"04月21日":
                    i = 4
                elif x["PubTime"].split(" ")[0] == u"04月22日":
                    i = 5
                elif x["PubTime"].split(" ")[0] == u"04月23日":
                    i = 6
                ti = int(x["PubTime"].split(" ")[1].split(":")[0])
                flag = 0
                for x in data:
                    if x[0] == i and x[1] == ti:
                        flag = 1
                        x[2] += 1
                if flag == 0:
                    data.append([i, ti, 1])
            except Exception, e:
                continue
        output = open('./html/san2.html', 'w')
        input = open('./html/san.html', 'r')
        output.write("1")

        output.close()
        output = open('./html/san2.html', 'w+')
        for line in input:
            line
            output.write(line)
            if (line == "var data = [\n"):
                for i in data:
                    output.write(str(i)+",\n")
        output.close()
        input.close()
        webbrowser.open_new_tab('file:///C:/lsy_spider/lsy_spider/Chuli/html/san2.html')
    def clickmore2(self):
        if self.comboBox_3.currentText()=="":
            QMessageBox.about(self, u"警告", u"请选择类簇!")
            return ""
        client=MongoClient('localhost',27017)
        db=client[str(self.comboBox_2.currentText().split(":")[3])]
        post=db["Information"]
        prov={}
        sum=0
        for x in post.find():
            if "Province" in x.keys():
                if x["Province"] in prov.keys():
                    prov[x["Province"]]+=1
                    sum+=1
                else:
                    prov[x["Province"]]=1
                    sum+=1
            if "City" in x.keys():
                if x["City"] in prov.keys():
                    prov[x["City"]]+=1
                    sum+=1
                else:
                    prov[x["City"]]=1
                    sum+=1
            else:
                continue
        for x in prov:
            prov[x]=int(prov[x]*1.0/25.0)
        output = open('./html/M2.html', 'w')
        input = open('./html/M.html', 'r')
        output.write("1")

        output.close()
        output = open('./html/M2.html', 'w+')
        for line in input:
            line
            output.write(line)
            if (line == "var data = [\n"):
                for i in prov:
                    output.write("{name:'%s', value:%d},\n" % (i.encode('utf8'),prov[i]))
        output.close()
        input.close()
        self.browserwin = MyWindow()
        self.browserwin.show()
        self.browserwin.load(QUrl('./html/M2.html'))
    def clickwidget(self,item):
        if self.tableWidget.currentColumn()==0:
            self.window=NewDialog()
            self.window.show()
            self.window.display(str(self.tableWidget.currentItem().text()),
                                self.comboBox_2.currentText().split(":")[3],
                                )
    def clickmore1(self):
        if self.comboBox_3.currentText()=="":
            QMessageBox.about(self, u"警告", u"请选择类簇!")
        else:
            client=MongoClient('localhost',27017)
            db=client[str(self.comboBox_2.currentText().split(":")[3])]
            post=db["Information"]
            dbhouqi=client["houqi"]
            posthouqi=dbhouqi[str(self.comboBox_2.currentText().split(":")[0])]
            dbtopic=client["topic"]
            posttopic=dbtopic[str(self.comboBox_2.currentText())]
            nan=0
            nv=0
            for x in posttopic.find({"id":int(self.comboBox_3.currentText())}):
                for id in x["IDS"]:
                    uid=posthouqi.find_one({"_id":ObjectId(id)})["ID"]
                    if  (post.find_one({"_id":uid}))["Gender"]==u"男":
                        nan+=1
                    else:
                        nv+=1
            output = open('./html/bin2.html', 'w')
            input = open('./html/bin.html', 'r')
            output.write("1")

            output.close()
            output = open('./html/bin2.html', 'w+')
            for line in input:
                line
                output.write(line)
                if (line == "                    data:[\n"):
                    output.write("{value:%d, name:'%s'},\n"%(nv,"女"))
                    output.write("{value:%d, name:'%s'},\n"%(nan,"男"))
            output.close()
            input.close()
            self.browserwin=MyWindow()
            self.browserwin.show()
            self.browserwin.load(QUrl('./html/bin2.html'))
    def clickwidget(self,item):
        if self.tableWidget.currentColumn()==0:
            self.window=NewDialog()
            self.window.show()
            self.window.display(str(self.tableWidget.currentItem().text()),
                                self.comboBox_2.currentText().split(":")[3],
                                )
    def start_nlpir(self):
        self.cons_2.clear()
        global Datebase_name
        global TFIDFbool
        global Needtime
        global Kmeansbool
        global numcu
        numcu=self.spinBox_2.value()
        if  self.comboBox.currentText()=="":
            QMessageBox.about(self,u"警告",u"请选择数据库")
        else:
            reply = QMessageBox.question(self, u'确认', u'是否选择了数据库'+self.comboBox.currentText()+u'进行分词',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply==QMessageBox.Yes:
                Datebase_name=self.comboBox.currentText()
                Needtime = str(self.dateEdit.date().year())+"-"+str(self.dateEdit.date().month()).zfill(2)\
                       +"-"+str(self.dateEdit.date().day()).zfill(2)+"="+str(self.spinBox.value()).zfill(2)
                if self.checkBox.isChecked():
                    TFIDFbool=1
                else:
                    TFIDFbool=0
                if self.comboBox_4.currentIndex()==0:
                    Kmeansbool=1
                else:
                    Kmeansbool=0

                self.Thread4 = NlpirThread()
                self.Thread4.start()
                self.timer2 = QtCore.QTimer()
                self.timer2.setInterval(3000)
                self.timer2.start()
                self.timer2.timeout.connect(self.timeproc2)
    def combobox2(self):
        client = MongoClient('localhost', 27017)
        db=client["topic"]
        post=db[str(self.comboBox_2.currentText())]
        print str(self.comboBox_2.currentText())
        self.comboBox_3.clear()
        for x in post.find():
            if "COREIDS" in x.keys():
                print x["COREIDS"]
                self.comboBox_3.addItem(str(x["id"]))
    def combobox3(self):
        self.tableWidget.clear()

        client = MongoClient('localhost', 27017)
        db=client["topic"]
        post=db[str(self.comboBox_2.currentText())]
        temp=post.find_one({"id":int(self.comboBox_3.currentText())})["COREIDS"]
        db2=client["houqi"]
        post2=db2[str(self.comboBox_2.currentText()).split(":")[0]]
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setHorizontalHeaderLabels([u'用户ID', u'发布时间', u'内容'])
        for x in range(len(temp)):
            t=post2.find_one({"_id":ObjectId(temp[x])})
            self.tableWidget.setItem(x,0,QtGui.QTableWidgetItem(str(t["ID"])))
            if " " in unicode(str(t["PubTime"])):
                time=unicode(str(t["PubTime"])).split(" ")[0]+" "+str(self.comboBox_2.currentText()).split(" ")[1].split(":")[0]+":"+unicode(str(t["PubTime"])).split(":")[1]
            self.tableWidget.setItem(x,1,QtGui.QTableWidgetItem(time))
            self.tableWidget.setItem(x,2,QtGui.QTableWidgetItem(unicode(t["Content"])))
            self.tableWidget.setColumnWidth(1, 130)
            self.tableWidget.setColumnWidth(2, 1500)
        #self.setCentralWidget(self.tableView)
    def addcommobox1(self):
        self.comboBox.clear()
        client = MongoClient('localhost', 27017)
        typelist=client.database_names()
        dontneed=["admin","cipin","houqi","Sinanew","XXXX","local","topic","test","TF-IDF"]
        typelist= list(set(typelist).difference(set(dontneed)))
        for i in typelist:
            self.comboBox.addItem(i)
    def addcommobox2(self):
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        client = MongoClient('localhost', 27017)
        db=client["topic"]
        for i in db.collection_names():
            self.comboBox_2.addItem(i)
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

    def timeproc2(self):
        self.cons_2.setText("")
        K=getFileOrderByUpdate2("C:\\lsy_spider\\lsy_spider\\Chuli\\log")
        print "show2 :"+K
        f = open(K, "r")
        for line in f.readlines():
            self.cons_2.append(unicode(line))
        f.close()
    def timeproc(self):
        self.cons.setText("")
        K=getFileOrderByUpdate("C:\\lsy_spider\\lsy_spider\\log")
        print "show :"+K
        f = open(K, "r")
        for line in f.readlines():
            self.cons.append(unicode(line))
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
    F.write("+")
    F.close()
    app = QtGui.QApplication(sys.argv)
    window = MyDialog()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("i.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    window.setWindowIcon(icon)
    window.show()
    sys.exit(app.exec_())
