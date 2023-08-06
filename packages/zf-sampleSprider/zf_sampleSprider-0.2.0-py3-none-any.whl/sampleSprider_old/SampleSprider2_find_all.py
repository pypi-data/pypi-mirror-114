# coding=utf-8
# 学习遍历、查找结点 2021-04-07
import requests
from bs4 import BeautifulSoup

def main():
    r= requests.get('https://www.vbiquge.com/15_15338/8549128.html')
    r.encoding='utf-8'
    str_html=r.text
    soup=BeautifulSoup(str_html,'lxml')

    div=soup.body.div
    # print(soup.prettify())

# 1.contents 将直接子节点以List[Tag]形式返回 需注意偶数(或奇数)下标值为'\n'
    # print(soup.body.contents)
    # print(soup.body.div.contents)
    # print(soup.body.script.contents)
    # print(type(div.contents[1]))  # <class 'bs4.element.Tag'>
    # print(div.contents[1])
    # print(div.contents[3])
    # print(div.contents[5])

    # for i in soup.body.div.contents:
    #     print(i)

# 2.find_all()  find_all(name, attrs, recursive, text, limit, **kwargs)：
    # (1) name:返回所有相应name标签的List[Tag]
    # 给定字符串
    # print(div.find_all('div'))
    # print(div.find_all('li'))

    # 给定正则表达式
    # print(div.find_all(re.compile('a|li')))
    # print(div.find_all(re.compile('\wi\w\d*')))

    # 传递列表
    # print(div.find_all(['h1','li']))

    # (2) attrs:定义一个字典，返回包含该属性的Tag列表
    # print(div.find_all(attrs={'class':'header'}))

    # (3) recursive 默认为True,会对soup的所有子节点进行查找，若设置为False，则只会查找直接子节点
    # print(div.find_all('script'))
    # print(div.find_all('script',recursive=False))

    # (4) text 给定值内容，可以是字符串，正则，列表 只返回标签值，无标签对
    # print(div.find_all(text='新笔趣阁'))
    # print(div.find_all(text=re.compile('[\u4e00-\u9fa5]*一章'))) # [\u4e00-\u9fa5]是简体中文utf-8的范围
    # print(div.find_all(text=['新笔趣阁','永久书架']))

    # (5) limit 限制返回个数
    # print(div.find_all('li'))
    # print(div.find_all('li',limit=2))