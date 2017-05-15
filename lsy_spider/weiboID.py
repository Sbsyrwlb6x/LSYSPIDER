# encoding=utf-8
# 初始的待爬队列
import os

weiboID = [
    '1697601814', '1682207150', '1855024094', '1960785875', '1726918143', '1847582585','3304034920',
    '1653603955', '1663072851', '1887344341', '1886903325', '1323527941', '1642512402', '1420398274','5324802169',
    '5476386628', '1887344341', '5133081104', '1197863207', '3606949911', '1098512281', '1131491197', '1893801487',
    '1496846867', '2046610400', '1871721375', '1864204590', '3802580928', '1267454277', '1569569157', '2557173891',
    '2549709795', '2340145481', '372835471',  '1710546672', '1764058362', '1426865994', '2698710503', '1496863563',
    '1048355927', '2498948744', '3251309964', '2039753857','2157271672','2550481263', '1400147030', '2970968691',
    '2930744304', '1180860635','2469604487', '2164864917', '1231668867', '1582297713', '1870375273', '1660141095',
    '3312088620', '5326065595','1973589075', '1009391435', '2342740235','1646744577', '1670421223','1642591402',
    '1663072851','3975581050','5291824241','1604159432','1893892941','1784473157','1618051664','1639498782',
    '3499350813','2656274875','2022990945','1314608344'
]
#　写入文件
def usefile_nlpir(str):
    G = getFileOrderByUpdate2("C:\\lsy_spider\\lsy_spider\\Chuli\\log")
    F = open(G, 'a')
    F.write(str + '\n')
    F.close()
def usefile(str):
    G = getFileOrderByUpdate("C:\\lsy_spider\\lsy_spider\\log")
    # print "usefile"+G
    F=open(G,'a')
    # print K+"#########"
    F.write(str+'\n')
    F.close()

def getFileOrderByUpdate(path):
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
    return "C:\\lsy_spider\\lsy_spider\\log\\"+sort_list[0][0]
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

K = getFileOrderByUpdate("C:\\lsy_spider\\lsy_spider\\log")