import urllib.request
import re
from bs4 import BeautifulSoup
import shutil
import time
import os


headers = { #伪装为浏览器抓取
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }


os.chdir(r'd:\Learn_English\Anglo-link\Advanced\Conversation\Study')
download_log=open("download_log.txt",'a+')

url = "https://app.anglo-link.com/public/pedia/audio/advanced/conversation/"
req = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(req)
doc=html.read().decode('gbk','ignore').encode('utf-8')
soup = BeautifulSoup(doc,"html5lib")
a_link = soup.find_all("a")
a_link_re=r'(?<=href=\")[a-z]+.*?\/(?=\")'   #正则表达式filter目录地址
dir_link=re.findall(a_link_re,str(a_link))
dir_links=[url+link for link in dir_link]       #生成器生成完整子目录地址

for link in dir_links[1:]:
    print(link)
    child_dir=link+"/study/british/mixed/"
    req_last = urllib.request.Request(child_dir, headers=headers)
    mp3_html = urllib.request.urlopen(req_last)
    doc_last = mp3_html.read().decode('gbk','ignore').encode('utf-8')
    soup_last = BeautifulSoup(doc_last,"html5lib")


    a_link_mp3 = soup_last.find_all(href=re.compile(".mp3"))
    a_link_mp3_re=r'(?<=href=\").*?\.mp3(?=\")'
    mp3_links=re.findall(a_link_mp3_re,str(a_link_mp3))

    for mp3_link in mp3_links:
        download_link=child_dir+mp3_link
        file_name=mp3_link
        try:
            with urllib.request.urlopen(download_link) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            print(file_name+" succeed to download")
        except:
            print(file_name+" failed to download")
            download_log.write(file_name+'\n')
