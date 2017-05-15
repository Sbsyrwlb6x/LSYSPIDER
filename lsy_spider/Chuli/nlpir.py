# -*- coding: UTF-8 -*-
import sys
sys.path.append('D:\\Python27\\Scripts')
sys.path.append('D:\\Python27\\Lib')
from pymongo import MongoClient
from ctypes import *
import time
import datetime
from STOPWORD import STOP
import cmath
from bson.objectid import ObjectId
import os
import copy
#NLPIR2014 Lib File (NLPIR64, NLPIR32, libNLPIR64.so, libNLPIR32.so),
#Change this when you are not using a Win64 environment:
libFile = './nlpir/NLPIR64.dll'
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
ImportUserDict('./nlpir/NLPIR_ImportUserDict.txt')
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
        truetime=pubtime.split(":")[0]+":"+str(pubtim2e).split(":")[1]
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
def cipinqianlie(needtime,num):
	client = MongoClient('localhost', 27017)
	db_from2=client["cipin"]
	post=db_from2[needtime]
	res=post.find().limit(num).sort("num",-1)
	for item in res:
		CP.append(item["word"].encode('utf8'))

# 计算每条微博自身的向量
def calculate_vector(needtime):
	client=MongoClient('localhost',27017)
	db=client["houqi"]
	post=db[needtime]
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
# 计算每条微博与其他微博的相似度，并且选出初始的微话题
def calculate_Similarity(needtime):
	global CORE_VECTOR_A
	global CORE_VECTOR_B
	global CORE_ID_A
	global CORE_ID_B
	client=MongoClient('localhost',27017)
	db=client["houqi"]
	post =db[needtime]
	similarity=[]
	i=0
	j=0
	numlist={}
	all=[]
	for x in post.find():
		similarity=[0.0]*post.find().count()
		j=0
		num=0
		for y in post.find():
			if i==j:
				similarity[j]=-1
			else:
				similarity[j]=calculate_two_vector(x["Vector"],y["Vector"])
				all.append(similarity[j])
				if similarity[j]>0.60:
					num+=1
			j=j+1
		i+=1
		numlist[str(x["_id"])]=num
	s=sorted(numlist.items(),lambda x,y:cmp(x[1],y[1]),reverse=True)
	print s[0:50]
	i=0
	# 找到大于阈值0.7，排名前10的微博作为初始微博
	for x in s[0:50]:
		for y in post.find():
			if str(y["_id"])==str(x[0]):
				CORE_VECTOR_A[i]=y["Vector"]
				CORE_ID_A[i]=[]
				CORE_ID_A[i].append(x[0])
		i+=1
	print "CORE_VECTOR_A:"
	print CORE_VECTOR_A
	print "CORE_ID_A:"
	print CORE_ID_A
	for x in post.find():
	 	if str(x["_id"]) in FIRST_OBJID:
	 		post.update({"_id": x["_id"]}, {"$set": {"First_Flag": 1}})
	 	else:
	 		post.update({"_id": x["_id"]}, {"$set": {"First_Flag": 0}})

	biaoshici=""
	cipin_and_num={}
	tweets_num=0
	time=needtime.split(" ")[1]
	tweets_ids=[]

	client = MongoClient('localhost', 27017)
	db_from = client["houqi"]
	db_to = client["topic"]
	post_from = db_from[needtime]
	post_to = db_to[needtime]
	times=1
	while 1:
		print "Another time: "+str(times)
		# print "A:"
		# print CORE_ID_A
		# print "B:"
		# print CORE_ID_B
		CORE_ID_B=copy.deepcopy(CORE_ID_A)
		CORE_VECTOR_B=copy.deepcopy(CORE_VECTOR_A)

		for x in post_from.find():
			temp={}
			index=0
			for y in CORE_VECTOR_A.values():
				temp[index]=calculate_two_vector(x["Vector"],y)
				index+=1
			# 计算和哪个核心微博最相似
			tempsort = sorted(temp.items(), lambda i, j: cmp(i[1], j[1]), reverse=True)
			CORE_ID_A[tempsort[0][0]].append(str(x["_id"]))
		# for x in range(10):
		#  	print len(CORE_ID_A[x])
		#  	print CORE_ID_A[x]
		for x in range(50):
			# 找到vector的长度
			for z in CORE_VECTOR_A.values():
				temp=[0]*len(z)
				break
			IDs=CORE_ID_A[x]
			# 求和取平均值
			for y in IDs:
				for vector in post_from.find({"_id":ObjectId(y)}):
					temp = [temp[i] + vector["Vector"][i] for i in range(len(temp))]
			temp=[temp[i]/float(len(CORE_ID_A[x])) for i in range(len(temp))]
			#设置新的中心向量
			CORE_VECTOR_A[x]=temp
			# print "CORE_VECTOR_A:"
			# print temp
		print "A:"
		print CORE_VECTOR_A
		# print "B:"
		# print CORE_ID_B
		# if CORE_ID_A!=CORE_ID_B:
		# 	times=times+1
		# 	continue
		# else:
		# 	break
		f=True
	 	for x in range(50):
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
		if f or times>1:
			files=open('./result/'+needtime+'.txt','w')
			files.write(str(CORE_ID_A))
			files.close()
			break
		else:
			times=times+1
			continue
def calculate_Mini(needtime):
	biaoshici=""
	cipin_and_num={}
	tweets_num=0
	time=needtime.split(" ")[1]
	tweets_ids=[]

	client = MongoClient('localhost', 27017)
	db_from = client["houqi"]
	db_to = client["topic"]
	post_from = db_from[needtime]
	post_to = db_to[needtime]

# 计算两个向量的相似度
def calculate_two_vector(a,b):
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
	db_from = client["test2"]
	db_to = client["cipin"] #统计词频
	db_to2= client["houqi"] #分词后结果
	num = 0
	db_to_post=db_to["2017-04-16 21"]
	db_to2_post=db_to2["2017-04-16 21"]
	for item in db_from.Tweets.find():
		try:
			if item["Tools"].encode('utf-8') not in Tools_NT:
				content = item["Content"].encode('utf8')
				split_content=""# 分词后字符串
				split_num=0 #分词个数
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
					db_to2_post.insert({"ID": item["ID"], "Content": content,
										"Split_Content":split_content,"Split_Num":split_num
										,"PubTime": item["PubTime"],"SystemTime": item["SystemTime"]})
				else:
					continue
		except Exception, e:
			pass

	# cipinqianlie(needtime,50)
	# print CP
	# calculate_vector(needtime)

def cmain():
	cipinqianlie("2017-04-16 21", 150)
	calculate_vector("2017-04-16 21")
	calculate_Similarity("2017-04-16 21")

if __name__ == "__main__":
    start=time.clock()
    #
    # cipinpaixu("2017-04-16 08")
    # cipinpaixu("2017-04-16 09")
    # cipinpaixu("2017-04-16 10")
    # cipinpaixu("2017-04-16 11")
    # cipinpaixu("2017-04-16 12")
    # cipinpaixu("2017-04-16 13")
    # cipinpaixu("2017-04-16 14")
    # cipinpaixu("2017-04-16 15")
    # cipinpaixu("2017-04-16 16")
    # cipinpaixu("2017-04-16 17")
    # cipinpaixu("2017-04-16 18")
    # cipinpaixu("2017-04-16 19")
    # cipinpaixu("2017-04-16 20")
    # cipinpaixu("2017-04-16 21")
    # cipinpaixu("2017-04-16 22")
    # cipinqianlie("2017-04-16 21", 150)
    # calculate_vector("2017-04-16 21")
    # calculate_Similarity("2017-04-16 21")
    #calculate_Mini("2017-04-04 20")

    end=time.clock()
    print ('Running time:%s Seconds' %(end-start))
    ImportUserDict('D.txt')
    p2 = "阿吉仔"
    p = "与此同时"
    for t in Seg(p2):
        z = '%s\t%s\t%s' % (t[0], t[1], translatePOS(t[1]))
        print z

