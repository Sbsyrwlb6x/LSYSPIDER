# -*- coding: utf-8 -*-
from pymongo import MongoClient
import time
from bson.objectid import ObjectId
start = time.clock()
client = MongoClient('localhost', 27017)
db = client["houqi"]
post = db["2017-04-14 12"]
num=0
for x in post.find():
    if u"朝鲜" and u"核" in x["Split_Content"]:
        num=num+1
print num
num=0
db=client["topic"]
post=db["2017-04-14 12:Kmeans++:noTFIDF:2017-04-24-113455"]
db2=client["houqi"]
post2=db2["2017-04-14 12"]
for x in post.find():
    if x["id"]==5:
        for y in x["IDS"]:
            print post2.find_one({"_id":ObjectId(y)})["Content"]
            if u"朝鲜" and u"核" in post2.find_one({"_id":ObjectId(y)})["Split_Content"]:
                num=num+1
print num