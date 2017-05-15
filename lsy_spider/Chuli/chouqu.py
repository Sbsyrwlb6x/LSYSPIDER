# -*- coding: UTF-8 -*-
from pymongo import MongoClient
import datetime
def panduan(needtime,systemtime,pubtime):
    if "-" in pubtime:
        truetime=pubtime.split(":")[0]+":"+str(pubtime).split(":")[1]
    elif "月" in pubtime:
        truetime=systemtime.split("-")[0]+"-"+pubtime.split("月")[0]+"-"+pubtime.split("月")[1].split("日")[0]+" "+pubtime.split(" ")[1]
    elif "今天" in pubtime:
        truetime=systemtime.split(" ")[0]+" "+pubtime.split(" ")[1]
    elif "前" in pubtime:
        truetime=datetime.datetime(int(systemtime.split("-")[0]),int(systemtime.split("-")[1]),int(systemtime.split("-")[2].split(" ")[0]),int(systemtime.split("-")[2].split(" ")[1].split(":")[0]),int(systemtime.split(":")[1]),0)
        amin=datetime.timedelta(minutes=int(pubtime.split("分钟前")[0]))
        truetime=truetime-amin
        truetime=str(truetime).split(":")[0]+":"+str(truetime).split(":")[1]
    if needtime==truetime[0:13]:
        print True
    else:
        print False
if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db_from = client["0412"]
    db_to = client["houqi"]
    panduan("2017-04-11 02","2017-04-11 02:29","03月25日 19:38")
    panduan("2017-04-11 02","2017-04-11 02:29", "2分钟前")
    panduan("2017-04-11 02","2017-04-11 02:29", "今天 02:26")
    panduan("2017-04-11 02","2017-04-11 02:29", "今天 11:20")
    panduan("2016-12-02 02","2017-04-11 02:29", "2016-12-02 15:49:15")