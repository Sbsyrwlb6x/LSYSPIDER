import datetime
from scrapy import cmdline
def runlaunch():
    cmdline.execute("scrapy crawl lsy_spider".split())
if __name__=="__main__":
    runlaunch()