# -*- coding: UTF-8 -*-
__create_time__ = '2017/3/2 29:22'
__author__ = 'Maxwell'
import requests
from bs4 import BeautifulSoup
import re
import os
import urllib
import urllib2
import traceback

res = [{u"薛兆丰北大经济学课": "http://jieduclub.com/forum.php?mod=forumdisplay&fid=126&page={page}&mobile=2"},
       {u"万维钢精英日课": "http://jieduclub.com/forum.php?mod=forumdisplay&fid=42&page={page}&mobile=2"}]


def download_mp3(url, dirname, title, myheaders):
    try:
        req = requests.get(url, headers=myheaders)
        text = req.text
        pattern1 = re.compile(r'http://eggtar.qiniudn.com/forum.*\.mp3"}')  # 我们在编译这段正则表达式
        matcher1 = re.search(pattern1, text)
        if matcher1 is not None:
            url = matcher1.group()[:-2]
            filename = urllib.unquote(url).split('/')[-1]
            url = url.replace(filename, "")
            filename = urllib2.quote(filename.encode("utf-8"))
            url = url + filename
            if not os.path.exists("resource/" + dirname):
                os.makedirs("resource/" + dirname)
            filename = "resource/" + dirname + "/" + title
            urllib.urlretrieve(url, filename + ".mp3")
    except Exception, e:
        print "download_mp3:" + traceback.format_exc()


def get_all_threads(url, dirname, myheaders):
    try:
        req = requests.get(url, headers=myheaders)
        html = BeautifulSoup(req.text, 'html.parser')
        lis = html.find("ul", {"class": "pagelist"}).find_all("li")
        for item in lis:
            title = item.find("div", {"class": "title"}).text
            title = title.replace('\n', '').replace('\r', '')
            thread_url = "http://jieduclub.com/" + item.find("a").get("href")
            print title, thread_url
            has_exist = check_file_has_download(dirname, title)
            if has_exist is True:
                print "has download,break"
                break
            download_mp3(thread_url, dirname, title, myheaders)
        if has_exist is False:
            pitems = html.find("div", {"class": "pg"})
            if pitems is not None:
                pages = pitems.find_all("a")
                for page in pages:
                    cls = page.get("class")
                    if cls is not None and "nxt" == cls[0]:
                        get_all_threads("http://jieduclub.com/" + page.get("href"), dirname, myheaders)
    except Exception, e:
        print "get thread error:" + traceback.format_exc()


def check_file_has_download(dirname, title):
    if os.path.exists("resource/" + dirname) and os.path.exists("resource/" + dirname + "/" + title + ".mp3"):
        return True
    else:
        return False


if __name__ == '__main__':
    myheader = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        "Cookie": "K6Mo_2132_saltkey=lU3kxAq5; K6Mo_2132_lastvisit=1490141993; K6Mo_2132_ulastactivity=43b1pLJ7ECD0NnDf5v4rsUXP23OPq6vWhaqgop0w1dhsGbdA%2Bswg; K6Mo_2132_auth=7cc4FhsN70BF13abCB9wZ1B%2FxwwgUUA9LjA1LZAImg%2F09O9sgPRL4krykq0HVXaJJWFf7gAtTt%2B0qTKfbk859QE; K6Mo_2132_security_cookiereport=bda7gXduLrok8TU4nMv58wLsQWGNSAV8Jwl2Bd0xrN%2B3kxAwt3sM; K6Mo_2132_atarget=1; K6Mo_2132_nofavfid=1; K6Mo_2132_lip=221.217.160.2%2C1490145596; Hm_lvt_83e06e1ac8c0df79d08be12991abd0b2=1490146961; Hm_lpvt_83e06e1ac8c0df79d08be12991abd0b2=1490146961; Hm_lvt_6eb658d6102f522831d0180a2d4b5ff4=1490146961; Hm_lpvt_6eb658d6102f522831d0180a2d4b5ff4=1490146961; K6Mo_2132_lastcheckfeed=298%7C1490146915; K6Mo_2132_noticeTitle=1; tjpctrl=1490148761582; K6Mo_2132_st_p=298%7C1490147006%7C41ebe541f7a9848e988389e5dab0a58a; K6Mo_2132_viewid=tid_7732; K6Mo_2132_visitedfid=126D61D42D85D57D58D89; K6Mo_2132_lastact=1490147220%09forum.php%09forumdisplay; K6Mo_2132_st_t=298%7C1490147220%7C38edd15eadc191c22c9c47bf7d175555; K6Mo_2132_forum_lastvisit=D_89_1490146903D_58_1490146938D_57_1490146943D_127_1490146946D_62_1490146950D_85_1490146966D_42_1490147016D_45_1490147021D_60_1490147026D_61_1490147029D_126_1490147220; K6Mo_2132_sid=JD6X4d"}
    for item in res:
        for (k, v) in item.items():
            url = v.replace("{page}", "1")
            get_all_threads(url, k, myheader)
