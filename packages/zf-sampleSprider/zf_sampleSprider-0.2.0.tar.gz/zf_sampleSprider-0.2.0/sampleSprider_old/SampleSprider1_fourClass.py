# coding=utf-8
# 简单爬取小说网站资源 2021-03-31
# 1.先下载读取工具urllib(内置，无需下载)和requests（第三方库）   pip install requests
# 2.下载解析工具 Beautiful Soup和lxml   pip install beautifulsoup4|pip install lxml
# 3.学习四大对象 2021-03-31，2021-04-07
import requests
from bs4 import BeautifulSoup

def main():
    r= requests.get('https://www.vbiquge.com/15_15338/8549128.html')
    r.encoding='utf-8'
    str_html=r.text
#     str_html=html = """
# <html>
# <head>
# <title>Jack_Cui</title>
# </head>
# <body>
# <p class="title" name="blog"><b>My Blog</b></p>
# <li><!--注释--></li>
# <a href="http://blog.csdn.net/c406495762/article/details/58716886" class="sister" id="link1">Python3网络爬虫(一)：利用urllib进行简单的网页抓取</a><br/>
# <a href="http://blog.csdn.net/c406495762/article/details/59095864" class="sister" id="link2">Python3网络爬虫(二)：利用urllib.urlopen发送数据</a><br/>
# <a href="http://blog.csdn.net/c406495762/article/details/59488464" class="sister" id="link3">Python3网络爬虫(三)：urllib.error异常</a><br/>
# </body>
# </html>
# """

    # 建议给定解析器类型 "lxml","lxml-xml", "html.parser", "html5lib"或者"html", "html5", "xml"
    soup=BeautifulSoup(str_html,'lxml')

    # 美化输出
    # print(soup.prettify())

# 1.Tag 对应标签 获取相应标签，不过只能获取第一个匹配到的标签
    # print(type(soup.title))  #<class 'bs4.element.Tag'>
    # print(soup.title)
    # print(soup.head)
    # print(soup.head.title)
    # print(soup.a)

    # Tag类有两个属性，name和attrs, name返回标签名;attrs返回该标签所有属性的字典
    # print(type(soup.title.name))  # <class 'str'>
    # print(type(soup.title.attrs)) # <class 'dict'>
    # print(soup.title.name)
    # print(soup.title.attrs)

    # print(soup.meta)
    # print(soup.meta.name)
    # print(soup.meta.attrs)

# 2.NavigableString  获取标签的值
    # print(type(soup.title.string))  # <class 'bs4.element.NavigableString'>
    # print(soup.title.string)

# 3.BeautifulSoup  代表一整个文档 可以视作特殊的Tag, 其也有name和attrs属性
    # print(type(soup))   # <class 'bs4.BeautifulSoup'>
    # print(soup.name)    # [document]
    # print(soup.attrs)   # {}

# 4.Comment 一个特殊的Navigable String类型 代表标签中的值为注释 当.string输出时，会自动去掉注释，所以有时需要手动处理
    # print(type(soup.li))     # <class 'bs4.element.Tag'>
    # print(soup.li)           # <li><!--注释--></li>
    # print(type(soup.li.string))  # <class 'bs4.element.Comment'>
    # print(soup.li.string)    # 注释
    # if type(soup.li.string).__name__=='Comment':
    #     print("<!--{}-->".format(soup.li.string))

