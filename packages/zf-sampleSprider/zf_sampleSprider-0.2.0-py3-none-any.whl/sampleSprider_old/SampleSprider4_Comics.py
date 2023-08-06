# coding=utf-8
# 爬取动漫之家漫画网 （动态加载） 2021-04-07
# 编码 改进 2021-04-08

from bs4 import BeautifulSoup
import requests
import re
from urllib.request import urlretrieve
import os
import sys

# 爬取一章的漫画图片
def getOneChapter(url,chapterName,name):
    r= requests.get(url)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text,'lxml')
    # 该页面采取动态加载，反爬手段之一，图片地址散落在script里，，用正则找出三段url
    str_script_oneChapter=soup.find_all('script',attrs={'type':'text/javascript'})[0].string
    str_first_url=re.findall('\|+(\d{4})\|+',str_script_oneChapter)[0]
    str_second_url=re.findall('\|(\d{5})\|',str_script_oneChapter)[0]
    str_third_urls=re.findall('(\d{13,14})\|',str_script_oneChapter)
    # 我们这时已经得到 所有图片连接的地址 ，但是是乱序的，需要排一下序
    str_third_urls.sort()

    # 用作图片的名称使用，因为现在单张图片没有名字
    pic_name=1
    for str_third_url in str_third_urls:
        url_pic='https://images.dmzj1.com/img/chapterpic/'+str_first_url+'/'+str_second_url+'/'+str_third_url+'.jpg'
        downloadPic(url_pic,chapterName,pic_name,name)
        pic_name=pic_name+1

# 下载该url下的图片
def downloadPic(url_pic,chapterName,pic_name,name):
    # 因为windows下有一些特殊字符不能作为目录名，所以需剔除
    chapterName=re.sub('[.|\\|/|:|*|?|"|<|>|\|]','',chapterName)
    path='D://{}/{}'.format(name,chapterName)
    # 因为不能写入未创建的目录，所以需要先创建目录
    mkdir(path)
    # 防止连接断开，进行重连操作
    try:
        urlretrieve(url_pic,path+'/{}.jpg'.format(pic_name))
    except BaseException:
        print(chapterName+'\t'+'连接失败，正在重新连接。。。。')
        downloadPic(url_pic,chapterName,pic_name)

# 创建目录
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path.encode('utf-8'))

def main(url='https://www.dmzj.com/info/yaoshenji.html',name='妖神记'):
    r= requests.get(url)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text,'lxml')

    tag_ul_allChapters=soup.find_all('ul',attrs={'class':'list_con_li autoHeight'})[1]
    tag_a_allChapters=tag_ul_allChapters.find_all('a')
    # 目前一切顺利 已经找到每一章节 的地址和名称 标签对
    for tag_a_allChapter in tag_a_allChapters:
        # 章节url
        str_url_chapter=tag_a_allChapter.attrs['href']
        # 章节名称
        str_title_chapter=tag_a_allChapter.find_all('span',attrs={'class':'list_con_zj'})[0].text
        getOneChapter(str_url_chapter,str_title_chapter,name)
        print(str_title_chapter+'\t'+'下载完成。')