# coding=utf-8
# 从ok资源网下载视频，可惜的是 该网站的资源已失效 下载找到资源网再下载 2021-04-13

import requests
from bs4 import BeautifulSoup
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

sys.argv =[sys.argv[0],'越狱第一季']

search_name=sys.argv[1]
search_url='http://haozy.cc/index.php'
search_parameters={
    'm':'vod-search'
}
search_headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Referer':'http://haozy.cc/',
    'Origin':'http://haozy.cc',
    'Host':'haozy.cc'
}
search_data={
    'wd':search_name,
    'submit':'search'
}

def downloadAllVideo(url):
    r= requests.get(url)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text,'lxml')
    print(soup.prettify())


def main():
    r= requests.post(search_url, params=search_parameters, headers=search_headers, data=search_data)
    r.encoding='utf-8'

    soup=BeautifulSoup(r.text,'lxml')
    list_span_video=soup.find_all('span',class_='xing_vb4')
    if list_span_video.__len__()==0:
        log.error("未找到该资源")
    else:
        str_href_video=list_span_video[0].find_all('a')[0].attrs['href']
        downloadAllVideo(search_url+str_href_video)
