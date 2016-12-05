#coding:utf-8
import requests
import re
import os
from bs4 import BeautifulSoup
import string
from lxml import etree


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
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'http://m.benzi8.com'
}

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
    #r = getsource(imgUrl)
    session = requests.Session()
    r = session.get(imgUrl, headers=setting.myHeaders, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    #with open(filename, 'wb') as f:
    #    for chunk in r.iter_content(chunk_size=1024):
    #        if chunk:
    #            f.write(chunk)
    #            f.flush()
    #    f.close()
    return filename
setting = NetWorkSetting()
imgUrl = "http://bz.caimanba.com/uploads/2016/1204bz3/bz90.jpg"
filename = 1
path = 1
topicid = 1
downloadImageFile(imgUrl, filename, path, topicid)
