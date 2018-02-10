#方法：读取每个网页，获取所有下载链接，然后逐个下载

import urllib.request
import re
import time

f = open('downloadlinks.txt', 'w+')

headers = { #伪装为浏览器抓取
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
for id in list(range(1,216,1)):
    try:
        podcast="https://pronuncian.com/podcasts/episode"+str(id)
        req=urllib.request.Request(podcast,headers=headers)
        html=urllib.request.urlopen(req)
        doc=html.read().decode('utf8')

        iframe_re='<iframe.*src=.*?\</iframe>'
        src =re.findall(iframe_re,doc)

        link_re=r'(?<=src=\").+?(?=\")'
        link=re.findall(link_re,str(src))
        print(str(id)+": ")
        print(link[0])
        f.write(str(id)+": "+str(link[0])+'\n')
        time.sleep(5)
    except urllib.error.HTTPError as err:
        print(str(id)+err.msg)
        f.write(str(id) +err.msg+'\n')
        continue
f.close()