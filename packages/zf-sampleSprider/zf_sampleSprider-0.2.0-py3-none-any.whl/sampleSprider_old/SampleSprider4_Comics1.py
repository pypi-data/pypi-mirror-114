# coding=utf-8
# 发现只能用于爬取一本漫画，在获取正则过程中有问题，更改代码，直接手撸JavaScript 2021-04-09
# 成功明白获取图片链接的规则，但是分为两种情况：一章只有一张图片;一章有多张图片，甚至字符串数组超过36. 2021-04-12
# 我去 有些漫画部分章节链接 本身就连不通 2021-04-12
# 存在章节数靠后的章节连接失败的情况，日后改进吧 2021-04-13

from bs4 import BeautifulSoup
import requests
import re
from urllib.request import urlretrieve
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


# 该程序设置了运行参数,主程序不再改动，从数组第二个参数开始设置，分别为漫画章节目录地址 漫画名字
# sys.argv =[sys.argv[0],'https://www.dmzj.com/info/dengpaozhixin2.html','灯泡之心']
#sys.argv =[sys.argv[0],'https://www.dmzj.com/info/yaoshenji.html','妖神记']
# sys.argv =[sys.argv[0],'https://www.dmzj.com/info/aaguziyaoruxuejuedouxueyuandeyangzi.html','【AA】咕哒子要入学决斗学院的样子']

# 爬取一章的漫画图片
def getOneChapter(url,chapterName,name):
    r= requests.get(url)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text,'lxml')
    # 该页面采取动态加载，反爬手段之一，图片地址散落在script里，，用正则找出三段url
    list_script_oneChapter=soup.find_all('script',attrs={'type':'text/javascript'})
    # 部分章节资源出错
    if list_script_oneChapter.__len__()==0:
        log.error('{} 链接出错'.format(chapterName))
        return ;
    else:
        str_script_oneChapter=list_script_oneChapter[0].string

    tuple_oneChapter=re.findall("return p}.*{(.*)}.*',(\d+),(\d+),'(.*)'\.split",str_script_oneChapter)[0]

    list_rules=tuple_oneChapter[0].split(',')[2].split(':')[1].strip('"').split('\\\\/')
    radix=tuple_oneChapter[1]
    len=tuple_oneChapter[2]
    list_part_url=tuple_oneChapter[3].split('|')

    url_pic='https://images.dmzj1.com/'
    # 用作图片的名称使用，因为现在单张图片没有名字
    pic_name=1
    for list_rule in list_rules:
        if '.' in list_rule:
            list_finally_url=list_rule.split('\\\\')[0].split('.')
            url_pic+=list_part_url[sixtyTwoToDecimal(list_finally_url[0])]+'.'+list_part_url[sixtyTwoToDecimal(list_finally_url[1])]
            downloadPic(url_pic,chapterName,pic_name,name)
            pic_name+=1
            url_pic='https://images.dmzj1.com/img/'
        else:
            url_pic=url_pic+list_part_url[sixtyTwoToDecimal(list_rule)]+'/'

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
        log.error(chapterName+'\t'+url_pic+'连接失败，正在重新连接。。。。')
        downloadPic(url_pic,chapterName,pic_name,name)

# 创建目录
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path.encode('utf-8'))

# 六十二进制 转 十进制
def sixtyTwoToDecimal(n):
    n_len=len(n)
    if n_len==1:
        return oneCharToInt(n)

    res=0
    for i in range(0,n_len):
        res+=pow(62,n_len-1-i)*oneCharToInt(n[i:i+1])
    return res

# 一个字符 六十二进制 转 十进制
def oneCharToInt(n):
    ascii_n=ord(n)
    if ascii_n>=48 and ascii_n<=57:
        return ascii_n-48
    elif ascii_n>=97 and ascii_n<=122:
        return ascii_n-87
    elif ascii_n>=65 and ascii_n<=90:
        return ascii_n-29


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
        log.info(str_title_chapter+'\t'+'下载完成。')