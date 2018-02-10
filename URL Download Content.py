#方法：读取每个网页，仅下载script，单独存为一个文件

import urllib.request
import re
from bs4 import BeautifulSoup
import time
import os



headers = { #伪装为浏览器抓取
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }

os.chdir(r'D:\Learn_English\Seattle learning Academy\Transcript')   #修改文件目录

for id in list(range(0,216,1)):
    try:
        podcast="https://pronuncian.com/podcasts/episode"+str(id)
        req=urllib.request.Request(podcast,headers=headers)
        html=urllib.request.urlopen(req)
        doc=html.read().decode('gbk','ignore').encode('utf-8')  #解决gbk编码错误问题

        soup=BeautifulSoup(doc)
        div=soup.find_all('div',class_="sqs-block html-block sqs-block-html")
        transcript_re=r'<p.*.*?\</p>'
        transcript= re.findall(transcript_re, str(div))
        if transcript.__len__()>0:
            result=BeautifulSoup(transcript[0])

            filename = "TranScript" + str(id) + ".txt"
            f = open(filename, 'w+')   #打开文件
            for text in [text for text in result.stripped_strings]:   #生成器，生成文本列表
                text=text.replace(u'\xa0', '_')  #通过替换解决GBK编码错误问题
                text=text.replace(u'\u014b', '_')
                text = text.replace(u'\u026a', '_')
                text = text.replace(u'\u028a', '_')
                text = text.replace(u'\u025b', '_')
                text = text.replace(u'\xe6', '_')
                text = text.replace(u'\u0259', '_')
                text = text.replace(u'\u02a7', '_')
                text = text.replace(u'\u0283', '_')
                text = text.replace(u'\u025d', '_')
                text = text.replace(u'\u02d0', '_')
                text = text.replace(u'\xf0', '_')
                text = text.replace(u'\u02cc', '_')
                text = text.replace(u'\u02c8', '_')
                text = text.replace(u'\u025a', '_')
                text = text.replace(u'\xf1', '_')
                text = text.replace(u'\u0292', '_')
                f.write(text)       #写入文件，关闭
            f.close()
            print(str(id)+" done"+'\n')
            time.sleep(5)
        continue

    except urllib.error.HTTPError as err:
        print(str(id)+err.msg)
        continue