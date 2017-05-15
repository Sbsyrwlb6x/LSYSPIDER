# encoding=utf-8

import os
import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lsy_spider.weiboID import getFileOrderByUpdate
K=getFileOrderByUpdate("C:\\lsy_spider\\lsy_spider\\log")
from yumdama import identify
from lsy_spider.weiboID import usefile
# 验证码输入方式:
# 1:手动输入     2:云打码
IDENTIFY = 2
cap = dict(DesiredCapabilities.PHANTOMJS)
cap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
)
logger = logging.getLogger(__name__)
handler=logging.FileHandler(K)
logging.getLogger("selenium").setLevel(logging.WARNING)
myWeiBo = [
     ('xunkao973338@163.com', 'js7105349'),
     ('rtt128512566@163.com', 'eqh938ttul9'),
     # ('17088529470', 'hh001122'),
     # ('1088614990', 'hh001122'),
     # ('17088617274', 'hh001122'),
     # ('17088022427', 'hh001122'),
     # ('17087640334', 'hh001122'),
     # ('17090256164', 'hh001122'),
     # ('18961614189', 'hh001122'),
     # ('17702506581', 'hh001122'),
     # ('15358810196', 'pp334455'),
     # ('17751689804', 'pp334455'),
     # ('13172057781', 'pp334455'),
     # ('17192522906', 'pp334455'),
     # ('17087682366', 'pp334455'),
     # ('17019992245', 'pp334455'),
     # ('17182564138','ss334455'),
     # ('17182503544','ss334455'),
     # ('17074798480','ss334455'),
     # ('17182564139','ss334455'),
     # ('17182584485','ss334455'),
     # ('17182566547','ss334455'),
     # ('17182574869','ss334455'),
     # ('17182504677','ss334455'),
     # ('18127596460','ss334455'),

]

def getCookie(account, password):
    try:
        browser = webdriver.PhantomJS(desired_capabilities=cap)
        browser.get("https://weibo.cn/login/")
        time.sleep(1)
        failure = 0
        # 尝试三次
        while "微博" in browser.title and failure < 3:
            print 'try again %d' % failure
            failure += 1
            # 找到用户名输入
            browser.save_screenshot("login.png")
            username = browser.find_element_by_name("mobile")
            username.clear()
            username.send_keys(account)
            # 找到密码输入 唯一定位用xpath
            psd = browser.find_element_by_xpath('//input[@type="password"]')
            psd.clear()
            psd.send_keys(password)
            try:
                code = browser.find_element_by_name("code")
                code.clear()
                if IDENTIFY == 1:
                    code_txt = raw_input("请查看路径下新生成的login.png，然后输入验证码:")
                else:
                    from PIL import Image
                    # 唯一定位验证码图片
                    img = browser.find_element_by_xpath('//form[@method="post"]/div/img[@alt="请打开图片显示"]')
                    # Style:CSSStyleDeclaration
                    x = img.location["x"]
                    y = img.location["y"]
                    im = Image.open("login.png")
                    im.crop((x, y, 100 + x, y + 22)).save("yundama.png")  # 剪切出验证码
                    print 'yundama'
                    usefile('\n'+'yundama')
                    code_txt = identify()  # 验证码打码平台识别
                code.send_keys(code_txt.decode())
            except Exception, e:
                pass

            commit = browser.find_element_by_name("submit")
            commit.click()
            time.sleep(5)

        cookie = {}
        if "我的首页" in browser.title:
            for elem in browser.get_cookies():
                cookie[elem["name"]] = elem["value"]
            strs=u"获取Cookie成功!( 账号:%s )" % account+'\n'
            print strs
            logger.warning(strs)
        #dict转化成str格式
        return json.dumps(cookie)
    except Exception, e:
        strs=u"获取 %s 的Cookie失败!" % account+'\n'
        print strs
        logger.warning(strs)
        print e
        return ""
    finally:
        try:
            browser.quit()
        except Exception, e:
            pass


# 获取所有账号的Cookie，存入redis
# 如果redis已有该账号的Cookie，则不再获取
def initCookie(rconn, spiderName):
    for weibo in myWeiBo:
        if rconn.get("%s:Cookies:%s--%s" % (spiderName, weibo[0], weibo[1])) is None:  # 'lsy_spider:Cookies:账号--密码'，为None即不存在。
            cookie = getCookie(weibo[0], weibo[1])
            print cookie
            if len(cookie) > 0:
                rconn.set("%s:Cookies:%s--%s" % (spiderName, weibo[0], weibo[1]), cookie)
                print "!!!!!!!!!!!!!!!!!!!!!"
    cookieNum = "".join(rconn.keys()).count("lsy_spider:Cookies")
    strs=u"Cookie的数量为:%s个........." % cookieNum+'\n'
    print strs
    logger.warning(strs)
    if cookieNum == 0:
        print strs
        strs=u'系统停止运行，Cookie数量为0...'+'\n'
        logger.warning(strs)
        os.system("pause")


#更新一个cookie
def updateCookie(Text, rconn, spiderName):
    acc = Text.split("--")[0]
    pas = Text.split("--")[1]
    cookie = getCookie(acc, pas)
    if len(cookie) > 0:
        strs=u"账号:%s 的Cookie成功更新!" % acc+'\n'
        print strs
        logger.warning(strs)
        rconn.set("%s:Cookies:%s" % (spiderName, Text), cookie)
    else:
        strs=u"账号:%s 的Cookie失败!已经删除" % Text+'\n'
        logger.warning(strs)
        print strs
        removeCookie(Text, rconn, spiderName)

#删除一个cookie
def removeCookie(Text, rconn, spiderName):
    rconn.delete("%s:Cookies:%s" % (spiderName, Text))
    cookieNum = "".join(rconn.keys()).count("SinaSpider:Cookies")
    strs=u"剩余微博账号数量:%s个........." % cookieNum+'\n'
    print strs
    logger.warning(strs)
    if cookieNum == 0:
        strs=u"系统停止运行，Cookie数量为0"+'\n'
        print strs
        logger.warning(strs)
        os.system("pause")
