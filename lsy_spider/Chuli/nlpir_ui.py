# -*- coding: UTF-8 -*-
import sys
import logging
sys.path.append('D:\\Python27\\Scripts')
sys.path.append('D:\\Python27\\Lib')
import math
from pymongo import MongoClient
from ctypes import *
import time
import random
import datetime
from STOPWORD import STOP
import cmath
from bson.objectid import ObjectId
import os
import copy
#NLPIR2014 Lib File (NLPIR64, NLPIR32, libNLPIR64.so, libNLPIR32.so),
#Change this when you are not using a Win64 environment:
libFile = './nlpir/NLPIR64.dll'

Bool_TFIDF=False
Bool_Kmeans=False
TopicDatabasename=""
# 排名前列的词序
CP=[]
# 排名前列的初始微博ID
FIRST_OBJID={}
CORE_ID_A={}
CORE_VECTOR_A={}
CORE_ID_B={}
CORE_VECTOR_B={}
# 不需要的词
NT = ["vshi", "vyou", "r", "rr", "rz", "rzt", "rzs", "rzv", "ry", "ryt", "rys", "ryv", "rg", "m", "mq",
		  "vf", "vx", "vi", "vl", "vg", "p", "pba", "pbei", "c", "cc", "u", "uzhe", "ule", "uguo", "ude1", "ude2",
		  "ude3", "usuo", "udeng", "uyy", "udh", "uls", "uzhi", "ulian", "e", "y", "o", "h", "k", "xu", "w",
		  "wkz", "wky", "wyz", "wyy", "wj", "ww", "wt", "wd", "wf", "wn", "wm","ws","wp", "wb", "wh",
		  "d"]
#　不需要的平台
Tools_NT = ("四川手机营业厅", "手机淘宝", "粉丝红包", "微博会员中心", "微博等级", "豆瓣", "echo回声", "生日动态"
		, "秒拍网页版", "皮皮时光机", "微卡券", "美图M6·自拍大明星", "粉丝服务平台", "互粉赏金榜", "微博直播组件", "人民微管家"
		,"秒拍安卓版", "微博问答", "摩卡幻想", "一直播", "政务直通车", "微话题", "微博音乐", "能量榜"
		, "微博红包", "QQ音乐", "91手机娱乐", "最佳蹲坑读物","秒拍客户端","美女达人","微博电影","美图秀秀Android版"
		,"微博桌面","微博活动","网易云音乐","鹿晗愿望季","贪吃蛇大作战","Mark_我的电影清单","全民K歌","求收养站内版"
	    ,"海淘1号","互粉派对","随手拍APP","微博品牌活动","自拍大明星•美图M6s","携程旅行","秒拍HD","58同城客户端"
		,"微博支付积分","FT中文网","everyday","一闪Onetake","微博众筹","粉丝红包财神卡PK","知乎客户端","百度知道手机客户端"
		,"支付宝","美拍","手机NBA中文官网","微盘","扇贝新闻","唱吧","探探","爱图购官网","陌陌","比较简单的大冒险","Netfits云墙"
		,"未通过审核应用","微电视","短信","虾米音乐移动版","微博体育","喜马拉雅_FM","微博达人","音乐人","搜狐视频"
		,"微公益","微访谈","百度分享","微博运动","手机淘宝","粉丝红包","你好美食Android","美图T8•双像素黑科技","乐视商城客户端","优酷土豆"
		,"哔哩哔哩","360安全平台","千牛","bShare分享","微管家","微博社区管理中心","勋章馆","唱吧","粉丝红包财神卡PK","秒拍HD"
		,"FindJapan","优酷土豆","微博等级","梦想直播live","科握","秒拍网页版","宝宝树孕育","番茄快点","微博支付积分"
		,"捕鱼达人2游戏","借贷宝","酷我音乐","全民K歌","爱马克","亲宝宝","快手","宜搜小说","乐视视频"
		,"新浪邮箱", "微盘","微盘","微博会员" , "喜马拉雅网", "手机淘宝", "豆瓣FM", "微博活动","短信")
dll =  CDLL(libFile)
def loadFun(exportName, restype, argtypes):
    global dll
    f = getattr(dll,exportName)
    f.restype = restype
    f.argtypes = argtypes
    return f

class ENCODING:
    GBK_CODE        =   0               #默认支持GBK编码
    UTF8_CODE       =   GBK_CODE+1      #UTF8编码
    BIG5_CODE       =   GBK_CODE+2      #BIG5编码
    GBK_FANTI_CODE  =   GBK_CODE+3      #GBK编码，里面包含繁体字

class POSMap:
    ICT_POS_MAP_SECOND  = 0 #计算所二级标注集
    ICT_POS_MAP_FIRST   = 1 #计算所一级标注集
    PKU_POS_MAP_SECOND  = 2 #北大二级标注集
    PKU_POS_MAP_FIRST   = 3	#

POS = {
	"n": {  #1.	名词  (1个一类，7个二类，5个三类)
		"n":"名词",
		"nr":"人名",
		"nr1":"汉语姓氏",
		"nr2":"汉语名字",
		"nrj":"日语人名",
		"nrf":"音译人名",
		"ns":"地名",
		"nsf":"音译地名",
		"nt":"机构团体名",
		"nz":"其它专名",
		"nl":"名词性惯用语",
		"ng":"名词性语素"
	},
	"t": {  #2.	时间词(1个一类，1个二类)
		"t":"时间词",
		"tg":"时间词性语素"
	},
	"s": {  #3.	处所词(1个一类)
		"s":"处所词"
	},
	"f": {  #4.	方位词(1个一类)
		"f":"方位词"
	},
	"v": {  #5.	动词(1个一类，9个二类)
		"v":"动词",
		"vd":"副动词",
		"vn":"名动词",
		"vshi":"动词“是”",
		"vyou":"动词“有”",
		"vf":"趋向动词",
		"vx":"形式动词",
		"vi":"不及物动词（内动词）",
		"vl":"动词性惯用语",
		"vg":"动词性语素"
	},
	"a": {  #6.	形容词(1个一类，4个二类)
		"a":"形容词",
		"ad":"副形词",
		"an":"名形词",
		"ag":"形容词性语素",
		"al":"形容词性惯用语"
	},
	"b": {  #7.	区别词(1个一类，2个二类)
		"b":"区别词",
		"bl":"区别词性惯用语"
	},
	"z": {  #8.	状态词(1个一类)
		"z":"状态词"
	},
	"r": {  #9.	代词(1个一类，4个二类，6个三类)
		"r":"代词",
		"rr":"人称代词",
		"rz":"指示代词",
		"rzt":"时间指示代词",
		"rzs":"处所指示代词",
		"rzv":"谓词性指示代词",
		"ry":"疑问代词",
		"ryt":"时间疑问代词",
		"rys":"处所疑问代词",
		"ryv":"谓词性疑问代词",
		"rg":"代词性语素"
	},
	"m": {  #10.	数词(1个一类，1个二类)
		"m":"数词",
		"mq":"数量词"
	},
	"q": {  #11.	量词(1个一类，2个二类)
		"q":"量词",
		"qv":"动量词",
		"qt":"时量词"
	},
	"d": {  #12.	副词(1个一类)
		"d":"副词"
	},
	"p": {  #13.	介词(1个一类，2个二类)
		"p":"介词",
		"pba":"介词“把”",
		"pbei":"介词“被”"
	},
	"c": {  #14.	连词(1个一类，1个二类)
		"c":"连词",
		"cc":"并列连词"
	},
	"u": {  #15.	助词(1个一类，15个二类)
		"u":"助词",
		"uzhe":"着",
		"ule":"了 喽",
		"uguo":"过",
		"ude1":"的 底",
		"ude2":"地",
		"ude3":"得",
		"usuo":"所",
		"udeng":"等 等等 云云",
		"uyy":"一样 一般 似的 般",
		"udh":"的话",
		"uls":"来讲 来说 而言 说来",
		"uzhi":"之",
		"ulian":"连 " #（“连小学生都会”）
	},
	"e": {  #16.	叹词(1个一类)
		"e":"叹词"
	},
	"y": {  #17.	语气词(1个一类)
		"y":"语气词(delete yg)"
	},
	"o": {  #18.	拟声词(1个一类)
		"o":"拟声词"
	},
	"h": {  #19.	前缀(1个一类)
		"h":"前缀"
	},
	"k": {  #20.	后缀(1个一类)
		"k":"后缀"
	},
	"x": {  #21.	字符串(1个一类，2个二类)
		"x":"字符串",
		"xx":"非语素字",
		"xu":"网址URL"
	},
	"w":{   #22.	标点符号(1个一类，16个二类)
		"w":"标点符号",
		"wkz":"左括号", 	#（ 〔  ［  ｛  《 【  〖 〈   半角：( [ { <
		"wky":"右括号", 	#） 〕  ］ ｝ 》  】 〗 〉 半角： ) ] { >
		"wyz":"全角左引号", 	#“ ‘ 『
		"wyy":"全角右引号", 	#” ’ 』
		"wj":"全角句号",	#。
		"ww":"问号",	#全角：？ 半角：?
		"wt":"叹号",	#全角：！ 半角：!
		"wd":"逗号",	#全角：， 半角：,
		"wf":"分号",	#全角：； 半角： ;
		"wn":"顿号",	#全角：、
		"wm":"冒号",	#全角：： 半角： :
		"ws":"省略号",	#全角：……  …
		"wp":"破折号",	#全角：——   －－   ——－   半角：---  ----
		"wb":"百分号千分号",	#全角：％ ‰   半角：%
		"wh":"单位符号"	#全角：￥ ＄ ￡  °  ℃  半角：$
	}
}

def usefile_nlpir(str):
    G = getFileOrderByUpdate2("C:\\lsy_spider\\lsy_spider\\Chuli\\log")
    F = open(G, 'a')
    F.write(str + '\n')
    F.close()
def getFileOrderByUpdate2(path):
    '''
    @功能：获取目录文件，根据文件更新时间排序
    '''
    path = unicode(path , "utf8")
    file_list = os.listdir(path)
    path_dict = {}
    for i in range(len(file_list)):
        path_dict[file_list[i]] = os.path.getmtime(os.path.join(path, file_list[i]))
    #按时间大小排序
    sort_list = sorted(path_dict.items(), key=lambda e:e[1], reverse=True)
    # 按降序输出文件名，及文件大小
    # print "###################"
    # for i in range(len(sort_list)):
        # print sort_list[i][0], sort_list[i][1]
    return "C:\\lsy_spider\\lsy_spider\\Chuli\\log\\"+sort_list[0][0]

class SegAtom(Structure):
    _fields_ = [("start", c_int32), ("length", c_int32),
        ("sPOS", c_char * 40),      ("iPOS", c_int32),
        ("word_ID", c_int32),       ("word_type", c_int32), ("weight", c_int32)
    ]

def translatePOS(sPOS):
    global POS
    if sPOS=='url': sPOS = 'xu'
    c = sPOS[0]
    return POS[c][sPOS]

Init = loadFun('NLPIR_Init',c_int, [c_char_p, c_int, c_char_p])
Exit = loadFun('NLPIR_Exit',c_bool, None)
ParagraphProcess = loadFun('NLPIR_ParagraphProcess',c_char_p, [c_char_p, c_int])
ParagraphProcessA = loadFun('NLPIR_ParagraphProcessA',POINTER(SegAtom), [c_char_p, c_void_p, c_bool])
#ParagraphProcessAW = loadFun('NLPIR_ParagraphProcessAW',None, [c_int, POINTER(SegAtom)])
FileProcess = loadFun('NLPIR_FileProcess',c_double, [c_char_p, c_char_p, c_int])
ImportUserDict = loadFun('NLPIR_ImportUserDict',c_uint, [c_char_p])
AddUserWord = loadFun('NLPIR_AddUserWord', c_int, [c_char_p])
SaveTheUsrDic = loadFun('NLPIR_SaveTheUsrDic', c_int, None)
DelUsrWord = loadFun('NLPIR_DelUsrWord',c_int, [c_char_p])
GetUniProb = loadFun('NLPIR_GetUniProb', c_double, [c_char_p])
IsWord = loadFun('NLPIR_IsWord',c_bool, [c_char_p])
GetKeyWords = loadFun('NLPIR_GetKeyWords',c_char_p, [c_char_p, c_int, c_bool])
GetFileKeyWords = loadFun('NLPIR_GetNewWords',c_char_p, [c_char_p, c_int, c_bool])
GetNewWords = loadFun('NLPIR_GetNewWords', c_char_p, [c_char_p, c_int, c_bool])
GetFileNewWords = loadFun('NLPIR_GetFileNewWords',c_char_p, [c_char_p, c_int, c_bool])
FingerPrint = loadFun('NLPIR_FingerPrint',c_ulong, [c_char_p])
SetPOSmap = loadFun('NLPIR_SetPOSmap',c_int, [c_int])
#New Word Identification
NWI_Start = loadFun('NLPIR_NWI_Start', c_bool, None)
NWI_AddFile = loadFun('NLPIR_NWI_AddFile',c_bool, [c_char_p])
NWI_AddMem = loadFun('NLPIR_NWI_AddMem',c_bool, [c_char_p])
NWI_Complete = loadFun('NLPIR_NWI_Complete', c_bool, None)
NWI_GetResult = loadFun('NLPIR_NWI_GetResult',c_char_p, [c_int])
NWI_Result2UserDict = loadFun('NLPIR_NWI_Result2UserDict',c_uint, None)

if not Init('',ENCODING.UTF8_CODE,''):
    print("Initialization failed!")
    exit(-111111)

'''
if not SetPOSmap(3): #POSMap.ICT_POS_MAP_SECOND
    print("Setting POS Map failed!")
    exit(-22222)
'''

def seg(paragraph):
    result = ParagraphProcess(paragraph, c_int(1))
    atoms = [i.strip().split('/') for i in result.split(' ') if len(i)>=1 and i[0]!=' ']
    atoms = [(a[0],a[1]) for a in atoms if len(a[0])>0]
    return atoms

def segment(paragraph):
    count = c_int32()
    result = ParagraphProcessA(paragraph, byref(count),c_bool(True))
    count = count.value
    atoms = cast(result, POINTER(SegAtom))
    return [atoms[i] for i in range(0,count)]

def Seg(paragraph):
    atoms = segment(paragraph)
    for a in atoms:
        if len(a.sPOS) < 1: continue
        i = paragraph[a.start: a.start + a.length]#.decode('utf-8')#.encode('ascii')
        yield (i, a.sPOS)

# 判断微博是否是需要时间的
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
        return True
    else:
        return False

# 计算前num个高频率分词，保存到CP list中
def cipinqianlie_tf(needtime,num):
	usefile_nlpir(u"----提取关键词模块----")
	usefile_nlpir(u"start...")
	global CP
	CP=[]
	client = MongoClient('localhost', 27017)
	db_from2 = client["TF-IDF"]
	post = db_from2[needtime]
	res = post.find().limit(num).sort("TF-IDF", -1)
	for item in res:
		CP.append(item["word"].encode('utf8'))
	usefile_nlpir(u"end")
def cipinqianlie(needtime,num):
	usefile_nlpir(u"----高频词汇模块----")
	usefile_nlpir(u"start...")
	global CP
	CP=[]
	client = MongoClient('localhost', 27017)
	db_from2=client["cipin"]
	post=db_from2[needtime]
	res=post.find().limit(num).sort("num",-1)
	for item in res:
		CP.append(item["word"].encode('utf8'))
	usefile_nlpir(u"end")
# 计算每条微博自身的向量
def calculate_vector2(needtime):
	usefile_nlpir(u"----计算自身向量模块----")
	usefile_nlpir(u"start...")
	client=MongoClient('localhost',27017)
	db=client["houqi"]
	post=db[needtime]
	global CP
	for item in post.find():
		split_num=item["Split_Num"]
		vector=[0]*len(CP)
		split_content=[]
		for i in range(split_num):
			if (item["Split_Content"].split(" ")[i].encode("utf8")) in CP:
				vector[CP.index(item["Split_Content"].split(" ")[i].encode("utf8"))]=1
			else:
				continue
		post.update({"_id": item["_id"]}, {"$set": {"Vector":vector}})
	usefile_nlpir(u"end")
# 计算每条微博自身的向量
def calculate_vector(needtime):
	usefile_nlpir(u"----计算自身向量模块----")
	usefile_nlpir(u"start...")
	client=MongoClient('localhost',27017)
	db=client["houqi"]
	post=db[needtime]
	global CP
	for item in post.find():
		split_num=item["Split_Num"]
		vector=[0]*len(CP)
		split_content=[]
		for i in range(split_num):
			if (item["Split_Content"].split(" ")[i].encode("utf8")) in CP:
				vector[CP.index(item["Split_Content"].split(" ")[i].encode("utf8"))]+=1
			else:
				continue
		post.update({"_id": item["_id"]}, {"$set": {"Vector":vector}})
	usefile_nlpir(u"end")
# 计算每条微博与其他微博的相似度，并且选出初始的微话题,开始聚类
def calculate_Kmeansplus(needtime):
	global Bool_Kmeans
	global Bool_TFIDF
	global TopicDatabasename
	TopicDatabasename = needtime
	if Bool_Kmeans==True:
		TopicDatabasename+=":Kmeans"
	else:
		TopicDatabasename+=":Kmeans++"
	if Bool_TFIDF==True:
		TopicDatabasename += ":useTFIDF"
	else:
		TopicDatabasename += ":noTFIDF"
	TopicDatabasename+=":"+sys.argv[1]
	usefile_nlpir(u"----Kmeans++聚类模块----")
	usefile_nlpir(u"start")
	global CORE_VECTOR_A
	global CORE_VECTOR_B
	global CORE_ID_A
	global CORE_ID_B
	CORE_ID_A = {}
	CORE_VECTOR_A = {}
	CORE_ID_B = {}
	CORE_VECTOR_B = {}
	num_cu=int(sys.argv[5])
	client = MongoClient('localhost', 27017)
	db = client["houqi"]
	temp=[]
	post = db[needtime]
	for x in post.find({},{"_id":1}):
		temp.append(str(x["_id"]))
	CORE_ID_A[0]=[]
	fir=random.choice(temp)
	CORE_ID_A[0].append(fir)
	CORE_VECTOR_A[0]=post.find_one({"_id":ObjectId(fir)})["Vector"]
	print CORE_ID_A

	for i in range(num_cu-1):
		sum=0
		sumtemp={}
		for x in post.find():
			if list(str(x["_id"])) in CORE_ID_A.values():
				continue
			else:
				# 数据库中的一个x和中心集每个点 计算欧拉距离，最近的保存在temp中
				# CORE_ID_A={0:[”a“],1:[”b“],2:[”c“]}
				temp=[]
				for y in CORE_ID_A.values():
					temp.append(calculate_two_vector_ol(x["Vector"],post.find_one({"_id":ObjectId("".join(y))})["Vector"]))
				sumtemp[str(x["_id"])]=sorted(temp)[0]
				sum+=sorted(temp)[0]
		ran=random.uniform(0,sum)
		for x in sumtemp:
			ran=ran-sumtemp[x]
			if ran<=0:
				CORE_ID_A[i+1]=[]
				CORE_ID_A[i+1].append(x)
				CORE_VECTOR_A[i+1]=[]
				CORE_VECTOR_A[i+1]=(post.find_one({"_id":ObjectId(x)})["Vector"])
				print len(CORE_VECTOR_A)
				break
	print CORE_ID_A
	print CORE_VECTOR_A
	for x in post.find():
	 	if list(str(x["_id"])) in CORE_ID_A.values():
	 		post.update({"_id": x["_id"]}, {"$set": {"First_Flag": 1}})
	 	else:
	 		post.update({"_id": x["_id"]}, {"$set": {"First_Flag": 0}})

	usefile_nlpir(u"初始聚类中心计算完成")
	client = MongoClient('localhost', 27017)
	db_from = client["houqi"]
	db_to = client["topic"]
	post_from = db_from[needtime]
	post_to = db_to[TopicDatabasename]
	times = 1
	while 1:
		print "Time: " + str(times)
		usefile_nlpir(u"第" + str(times) + u"次聚类开始")
		CORE_ID_B = copy.deepcopy(CORE_ID_A)
		CORE_VECTOR_B = copy.deepcopy(CORE_VECTOR_A)
		for x in post_from.find():
			temp = {}
			index = 0
			for y in CORE_VECTOR_A.values():
				temp[index] = calculate_two_vector_cos(x["Vector"], y)
				index += 1
			# 计算和哪个核心微博最相似
			# reverse=False 从小到大
			tempsort = sorted(temp.items(), lambda i, j: cmp(i[1], j[1]), reverse=True)
			# 移除原来的id，放到新的族中
			for N in range(len(CORE_ID_A)):
				if str(x["_id"]) in CORE_ID_A[N]:
					CORE_ID_A[N].remove(str(x["_id"]))
					break
			CORE_ID_A[tempsort[0][0]].append(str(x["_id"]))
		for x in range(num_cu):
			# 找到vector的长度
			for z in CORE_VECTOR_A.values():
				temp = [0] * len(z)
				break
			IDs = CORE_ID_A[x]
			# 求和取平均值
			for y in IDs:
				for vector in post_from.find({"_id": ObjectId(y)}):
					temp = [temp[i] + vector["Vector"][i] for i in range(len(temp))]
			for i in range(len(temp)):
				if (temp[i]) != 0:
					temp[i] = temp[i] / float(len(CORE_ID_A[x]))
				else:
					temp[i] = 0
     		# 设置新的中心向量
			CORE_VECTOR_A[x] = temp
		# print "A:"
		# print CORE_VECTOR_A
		f = True
		for x in range(num_cu):
			a = [int(CORE_VECTOR_A[x][i] * 100) for i in range(len(CORE_VECTOR_A[x]))]
			b = [int(CORE_VECTOR_B[x][i] * 100) for i in range(len(CORE_VECTOR_B[x]))]
			# print "a:"
			# print a
			# print "b:"
			# print b
			if a != b:
				f = False
				break
			else:
				continue
		if f or times > 30:
			files = open('./result/' + needtime + '.txt', 'w')
			usefile_nlpir(u"聚类完成！将结果存入数据库中...")
			for x in range(num_cu):
				post_to.insert({"id": x, "IDS": CORE_ID_A[x], "Keyword": keyword(CORE_ID_A[x], needtime),
								"Vector": CORE_VECTOR_A[x]})
			# files.close()
			usefile_nlpir(u"end")
			break
		else:
			times = times + 1
			continue
def calculate_Kmeans(needtime):
	global Bool_Kmeans
	global Bool_TFIDF
	TopicDatabasename=needtime
	global TopicDatabasename
	if Bool_Kmeans==True:
		TopicDatabasename+=":Kmeans"
	else:
		TopicDatabasename+=":Kmeans++"
	if Bool_TFIDF==True:
		TopicDatabasename += ":useTFIDF"
	else:
		TopicDatabasename += ":noTFIDF"
	TopicDatabasename += ":" + sys.argv[1]
	usefile_nlpir(u"----Kmeans聚类模块----")
	usefile_nlpir(u"start")
	global CORE_VECTOR_A
	global CORE_VECTOR_B
	global CORE_ID_A
	global CORE_ID_B
	CORE_ID_A = {}
	CORE_VECTOR_A = {}
	CORE_ID_B = {}
	CORE_VECTOR_B = {}
	num_cu=int(sys.argv[5])
	client=MongoClient('localhost',27017)
	db=client["houqi"]
	post =db[needtime]
	similarity=[]
	i=0
	j=0
	numlist={}
	all=[]
	for x in post.find():
		print i
		similarity=[0.0]*post.find().count()
		j=0
		num=0
		for y in post.find():
			if i==j:
				similarity[j]=-1
			else:
				similarity[j]=calculate_two_vector_cos(x["Vector"],y["Vector"])
				all.append(similarity[j])
				if similarity[j]>0.60:
					num+=1
			j=j+1
		i+=1
		numlist[str(x["_id"])]=num
	s=sorted(numlist.items(),lambda x,y:cmp(x[1],y[1]),reverse=True)
	i=0
	# 找到大于阈值，排名前列的微博作为初始微博
	for x in s[0:num_cu]:
		for y in post.find():
			if str(y["_id"])==str(x[0]):
				CORE_VECTOR_A[i]=y["Vector"]
				CORE_ID_A[i]=[]
				CORE_ID_A[i].append(x[0])
		i+=1
	usefile_nlpir(u"初始族类中心计算完毕共"+str(num_cu)+u"个:")
	for x in CORE_ID_A:
		usefile_nlpir(str(x))
	print "CORE_VECTOR_A:"
	print CORE_VECTOR_A
	print "CORE_ID_A:"
	print CORE_ID_A
	for x in post.find():
	 	if list(str(x["_id"])) in CORE_ID_A.values():
	 		post.update({"_id": x["_id"]}, {"$set": {"First_Flag": 1}})
	 	else:
	 		post.update({"_id": x["_id"]}, {"$set": {"First_Flag": 0}})

	client = MongoClient('localhost', 27017)
	db_from = client["houqi"]
	db_to = client["topic"]
	post_from = db_from[needtime]
	post_to = db_to[TopicDatabasename]
	times=1
	while 1:
		usefile_nlpir(u"第"+str(times)+u"次聚类开始")
		print "Another time: "+str(times)
		CORE_ID_B=copy.deepcopy(CORE_ID_A)
		CORE_VECTOR_B=copy.deepcopy(CORE_VECTOR_A)

		for x in post_from.find():
			temp={}
			index=0
			for y in CORE_VECTOR_A.values():
				temp[index]=calculate_two_vector_cos(x["Vector"],y)
				index+=1
			# 计算和哪个核心微博最相似
			tempsort = sorted(temp.items(), lambda i, j: cmp(i[1], j[1]), reverse=True)
			# 移除原来的id，放到新的族中
			for N in range(len(CORE_ID_A)):
				if str(x["_id"]) in CORE_ID_A[N]:
					CORE_ID_A[N].remove(str(x["_id"]))
					break
			CORE_ID_A[tempsort[0][0]].append(str(x["_id"]))
		for x in range(num_cu):
			# 找到vector的长度
			for z in CORE_VECTOR_A.values():
				temp=[0]*len(z)
				break
			print CORE_ID_A
			IDs=CORE_ID_A[x]
			# 求和取平均值
			for y in IDs:
				for vector in post_from.find({"_id":ObjectId(y)}):
					temp = [temp[i] + vector["Vector"][i] for i in range(len(temp))]
			for i in range(len(temp)):
				if (temp[i])!=0:
					temp[i]=temp[i]/float(len(CORE_ID_A[x]))
				else:
					temp[i]=0
			# temp=[temp[i]/float(len(CORE_ID_A[x])) for i in range(len(temp))]
			#设置新的中心向量
			CORE_VECTOR_A[x]=temp
		print "A:"
		print CORE_VECTOR_A
		f=True
	 	for x in range(num_cu):
			a=[int(CORE_VECTOR_A[x][i]*100) for i in range(len(CORE_VECTOR_A[x]))]
			b=[int(CORE_VECTOR_B[x][i]*100) for i in range(len(CORE_VECTOR_B[x]))]
			print "a:"
			print a
			print "b:"
			print b
			if a!=b:
				f=False
				break
			else:
				continue
		if f or times>50:
			#files=open('./result/'+needtime+'.txt','w')
			#files.write(str(CORE_ID_A))
			usefile_nlpir(u"聚类完成！将结果存入数据库中...")
			for x in range(num_cu):
				post_to.insert({"id":x,"IDS":CORE_ID_A[x],"Keyword":keyword(CORE_ID_A[x],needtime),"Vector":CORE_VECTOR_A[x]})
			#files.close()
			usefile_nlpir(u"end")
			break
		else:
			times=times+1
			continue
def keyword(COREID,needtime):
	client=MongoClient('localhost',27017)
	db=client["houqi"]
	post=db[needtime]
	keyw = {}
	for item in COREID:
		temp=post.find_one({"_id":ObjectId(item)})["Split_Content"].split(" ")
		for y in temp:
			if y=='':
				continue
			if y in keyw.keys():
				keyw[y]=keyw[y]+1
			else:
				keyw[y]=1
	return sorted(keyw.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
def calculate_TFIDF(needtime):
	usefile_nlpir(u"----计算TFIDF模块----")
	usefile_nlpir(u"start...")
	client = MongoClient('localhost', 27017)
	db_1 = client["cipin"]
	post1 = db_1[needtime]
	db_2 = client["houqi"]
	post2 = db_2[needtime]
	db_3 = client["TF-IDF"]
	post3 = db_3[needtime]
	# 总词数numall
	numall=0
	for y in post2.find():
		numall=numall+len(y["Split_Content"])
	print numall
	for x in post1.find():
		word=x["word"]
		# 该次在文档中刚出现的次数num
		num=x["num"]
		#print num
		#print numall
		TF=(num*1.0)/(numall*1.0)
		print TF
		# 包含该词的文档数 n
		n=0
		for y in post2.find():
			if word in y["Split_Content"].split(" "):
				n=n+1

		IDF=math.log(post2.find().count()/(n+1))
		temp=float(TF*IDF)
		if post3.find_one({"word":word})==None:
			post3.insert({"word":word,"num":num,"TF-IDF":temp})
		else:
			post3.update({"word":word},{"$set": {"num":num,"TF-IDF":temp}})
	usefile_nlpir(u"end")
# 计算两个向量的相似度(欧拉距离，越小越相似)
def calculate_two_vector_ol(a,b):
	x=sum(list(map(lambda x:(x[0]-x[1])*(x[0]-x[1]),zip(a,b)))) ** 0.5
	return x
# 计算两个向量的相似度(余弦距离，越大越相似)
def calculate_two_vector_cos(a,b):
	x=sum(list(map(lambda x:x[0]*x[1],zip(a,b))))
	y=(sum(list(map(lambda x:x[0]*x[1],zip(a,a))))) ** 0.5
	z=(sum(list(map(lambda x:x[0]*x[1],zip(b,b))))) ** 0.5
	if z==0 or y==0 or x==0:
		return 0
	else:
	    return x/(y*z)
# 分词，总函数
def cipinpaixu(needtime):
	client = MongoClient('localhost', 27017)
	dbname=needtime.split("-")[1]+needtime.split("-")[2].split(" ")[0]
	db_from = client[sys.argv[1]]
	#db_from = client["2017-04-24-113455"]
	db_to = client["cipin"] #统计词频
	db_to2= client["houqi"] #分词后结果
	num = 0
	need=needtime.split(" ")[0]+" "+str(12)
	db_to_post=db_to[need]
	db_to2_post=db_to2[need]
	for item in db_from.Tweets.find():
		try:
			if item["Tools"].encode('utf-8') not in Tools_NT:
				content = item["Content"].encode('utf8')
				split_content=""# 分词后字符串
				split_num=0 #
				if panduan(needtime, item["SystemTime"].encode('utf-8'), item["PubTime"].encode('utf-8')):
					for t in Seg(content):
						if t[1] not in NT and t[0] not in STOP:
							split_num=split_num+1
							split_content=split_content+t[0]+" "
							if db_to_post.find({"word": t[0]}).count() != 0:
								db_to_post.update({"word": t[0]}, {"$inc": {"num": 1}})
							else:
								db_to_post.insert({"word": t[0], "type": translatePOS(t[1]), "num": 1})
						else:
							continue
					if db_to2_post.find_one({"Content":content}) == None:
					    db_to2_post.insert({"ID": item["ID"], "Content": content,
										"Split_Content":split_content,"Split_Num":split_num
										,"PubTime": item["PubTime"],"SystemTime": item["SystemTime"]})
				else:
					continue
		except Exception, e:
			pass
def calculate_Topic(needtime):
	usefile_nlpir(u"----处理Topic数据----")
	usefile_nlpir(u"start")
	client=MongoClient('localhost',27017)
	db = client["topic"]
	db2 = client["houqi"]
	post2 = db2[needtime]
	post = db[TopicDatabasename]
	for x in post.find():
		print "-----------------------------------------------------------------"
		Vectormid=x["Vector"]
		temp={}
		if len(x["IDS"])!=0:
			for y in x["IDS"]:
				v=post2.find_one({"_id": ObjectId(y)})["Vector"]
				temp[y]=calculate_two_vector_cos(Vectormid,v)
			COREIDS=[]
			for t in sorted(temp.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)[0:20]:
				COREIDS.append(t[0])
			post.update({"_id": x["_id"]}, {"$set": {"COREIDS": COREIDS}})
	usefile_nlpir(u"end")
def test():
    calculate_Kmeans("2017-04-21")
    calculate_Topic("2017-04-21 12:Kmeans:noTFIDF:test2")
if __name__ == "__main__":
    #sys.argv = ['C:\\lsy_spider\\der\\Chuli\\nlpir_ui.py', 'test2', '2017-04-21=12', '0', '1',60]
	# 完整步骤
	# cipinpaixu("2017-04-04 12")
	# calculate_TFIDF("2017-04-04 12")
	# cipinqianlie_tf("2017-04-04 12", 150)
	# 　calculate_vector("2017-04-04 12")
	#  calculate_Kmeans("2017-04-14 12")
	# 12时是 113455数据库 核心微博用户
	# 11时是 所有用户 test2 数据库
    # ImportUserDict('D.txt')
    # arg=["2017-04-16","2017-04-20"]
    # for needday in arg:
		# for x in range(6, 22):
		# 	temp = needday + " " + str(x).zfill(2)
		# 	cipinpaixu(temp)
		# need = needday + " " + str(12)
		# calculate_TFIDF(need)
		# cipinqianlie_tf(need, 150)
		# calculate_vector(need)
		# calculate_Kmeans(need)
    #sys.argv=['C:\\lsy_spider\\der\\Chuli\\nlpir_ui.py', '0413', '2017-04-17=12', '0', '1']
    start=time.clock()
    global Bool_TFIDF
    global Bool_Kmeans
    global TopicDatabasename
    usefile_nlpir(u"开始分词...请勿关闭程序")
    usefile_nlpir(u"选择分词的时间段为..." + str(sys.argv[2]))
    usefile_nlpir(u"选择分词的数据库为..." + str(sys.argv[1]))
    if sys.argv[3]== "1":
        usefile_nlpir(u"是否使用TF-IDF向量...是")
        print "是否使用TF-IDF向量...是"
        Bool_TFIDF=True
    else:
		usefile_nlpir(u"是否使用TF-IDF向量...否")
		print "是否使用TF-IDF向量...否"
		Bool_TFIDF = False
    if sys.argv[4]=="1":
		usefile_nlpir(u"使用Kmeans聚类算法")
		print "使用Kmeans聚类算法"
		Bool_Kmeans=True
    else:
		usefile_nlpir(u"使用Kmeans++聚类算法")
		print "使用Kmeans++聚类算法"
		Bool_Kmeans=False

    temp=sys.argv[2].split("=")[0]+" "+sys.argv[2].split("=")[1]
    arg=[]
    arg.append(sys.argv[2].split("=")[0])
    print sys.argv
    print temp

    for needday in arg:
		usefile_nlpir(u"----分词模块----")
		usefile_nlpir(u"start...")
		for x in range(6,22):
			temp=needday+" "+str(x).zfill(2)
			cipinpaixu(temp)
		usefile_nlpir(u"end")
		need = needday+ " " + str(12)
		if Bool_TFIDF==True:
			calculate_TFIDF(need)
			cipinqianlie_tf(need, 150)
		else:
			cipinqianlie(need,150)
		calculate_vector(need)
		if Bool_Kmeans==False:
			calculate_Kmeansplus(need)
		else:
			calculate_Kmeans(need)
		calculate_Topic(need)
    end=time.clock()
    usefile_nlpir(u"共用时"+str(end-start)+u"秒...")
    print ('Running time:%s Seconds' %(end-start))

	# p2 = "Big News: @解放日报 [最右]【呼市铁路局原副局长被判死缓 最头痛藏钱】2013年12月底，呼市铁路局原副局长马俊飞因受贿被判死缓。他说最头痛藏钱，从呼和浩特到北京，马俊飞又是购房又是租房，在挥之不去的恐惧中，人民币8800万、美元419万、欧元30万、港币27万，黄金43.3公斤，逐渐堆满了两所房子…… http://t.cn/8kgR6Yi。"
	# p = "与此同时"
	# for t in Seg(p2):
	# 	z = '%s\t%s\t%s' % (t[0], t[1], translatePOS(t[1]))
	# 	print z
