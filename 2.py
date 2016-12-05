#coding:utf-8
import requests
import re
import os
from bs4 import BeautifulSoup
import string


isProxyNeeded = True


def getsource(url):
    if isProxyNeeded:
        result = session.get(url, headers=setting.myHeaders, proxies=setting.proxy)
    else:
        result = session.get(url, headers=setting.myHeaders)
    return result


def downloadImageFile(imgUrl, filename, path, topicid):
    print "enter downloadImageFile"
    extendname = imgUrl.split('.')[-1]
    filename = str(filename)
    filename += '.' + extendname
    path = str(path)
    topicid = str(topicid)
    path = "D:/pangzi2/" + path + "/" + topicid + "/"
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)
    filename = path + filename
    print "Download Image File=", filename
    print "Download Image File from=", imgUrl
    r = session.get(imgUrl, headers=setting.myHeaders, stream=True, timeout=12)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    return filename


def handletopic(topic, page, topicid):
    print "handletopic"
    picturesurl = ""
    picturenumber = 0
    topicresult = getsource(topic)
    #get topic sourc, try to check if it has more than one picture
    #if yes, download them, otherwise ignore it
    topicsoap = BeautifulSoup(topicresult.content)

    for url in topicsoap.find_all('img'):
        if url.has_attr("alt") and url.has_attr("src") and url.get("src") not in picturesurl:
            picturesurl = url.get("src")

    for number in topicsoap.find_all('a'):
        if number.get_text().find(u"共") != -1:
            temp = number.get_text()
            temp = temp[1:-1]
            index = temp.find(u"页")
            temp = temp[:index]
            picturenumber = int(temp)

    flag = picturesurl.rfind('.')
    extendname = picturesurl[flag:]
    urlprefix = picturesurl[:flag - 1]
    print extendname
    print urlprefix

    count = 1
    while count <= picturenumber:
        targetUrl = urlprefix + str(count) + extendname
        print targetUrl
        downloadImageFile(targetUrl, count, page, topicid)
        count += 1


def handlepage(page):
    print "enter handlepage"
    if page == 1:
        pageurl = setting.searchUrl
    else:
        #http://m.benzi8.com/shaonv/list_4_90.html
        pageurl = setting.prefixUrl + "list_4_" + str(page) + ".html"
    print pageurl
    #get page resource
    result = getsource(pageurl)
    pagesoap = BeautifulSoup(result.content)
    #get topics in current page
    topicid = 1
    for link in pagesoap.find_all('a'):
        #for each topic, get the source
        #if link.has_attr("class") and link.has_attr("href") and link.get("class") == "text":
        if link.has_attr("class") and link.has_attr("href"):
            topicurl = setting.prefixUrl + link.get("href")
            handletopic(topicurl, page, topicid)
            topicid += 1


class NetWorkSetting:
    def __init__(self):
        self.proxy = {
            "http": 'http://10.158.100.9:8080',
            "https": 'https://10.158.100.9:8080'}
        #self.searchUrl = 'http://m.benzi8.com/shaonv/'
        self.searchUrl = 'http://m.benzi8.com/shaonv/'
        self.prefixUrl = 'http://m.benzi8.com'
        self.myHeaders = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Referer': 'http://m.benzi8.com/shaonv/'
}


#1. get result for key word search
print "1, open home page to get all url for comics"
setting = NetWorkSetting()
session = requests.Session()
target_url = setting.searchUrl


page = 1
while page <= 1:
    handlepage(page)
    page += 1

