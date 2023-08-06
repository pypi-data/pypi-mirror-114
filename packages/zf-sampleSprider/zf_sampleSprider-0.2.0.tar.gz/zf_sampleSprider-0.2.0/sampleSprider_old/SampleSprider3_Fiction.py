# coding=utf-8
# 从新笔趣阁爬取诡秘之主小说的所有章节 并下载到本地txt文件 2021-04-07
# 从新笔趣阁爬取任意一本小说的所有章节 优化 2021-04-09
# 解决编码不一致导致的错误 2021-04-13

from bs4 import BeautifulSoup
import requests
import sys

def getOneChapter(url):
    try:
        r= requests.get(url)
    except BaseException:
        getOneChapter(url)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text,'lxml')
    tag_div_contents=soup.body.find_all(attrs={'id':'content'})[0]
    return tag_div_contents.text.replace('    ','\n')#.replace('\xa0','')

def main(url='https://www.vbiquge.com/76_76449/',name='万界天尊'):
    path='D://'+name+'.txt'
    # 文件默认的是gkb编码，而页面编码是utf-8，所以会产生部分字符转换异常的情况，需统一
    file=open(path,'w',encoding='utf-8')
    pre_url='https://www.vbiquge.com'
    # 目录地址
    r= requests.get(url)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text,'lxml')

    tag_div_box_con=soup.find_all('div',attrs={'id':'list'})[0]
    # 顺利找到目录所在标签对
    tag_dd_chapters=tag_div_box_con.find_all('dd')
    try:
        for tag_dd_chapter in tag_dd_chapters:
            # 小说章节题目
            str_title=tag_dd_chapter.string
            # 小说各章节地址
            url_chapter=tag_dd_chapter.a.attrs['href']
            url=pre_url+url_chapter

            print(str_title,end='')
            file.write(str_title+'\n')
            file.write(getOneChapter(url))
            file.write('\n-------------------------------------------------------------------------------------------------------------\n')
            print('\t'+'下载完成')
    finally:
        file.close()