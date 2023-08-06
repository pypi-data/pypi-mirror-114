# coding=utf-8
# 初步学习python爬虫 先学习requests模块 2021-03-22
import requests

if __name__=="__main__":
    url1="https://www.baidu.com"
    url2="https://tieba.baidu.com/f"
    # # 谷歌浏览器用户代理
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    # # iphone Safari浏览器代理
    # headers1={'user-agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'}
    #
    #
    # r1=requests.get(url1,headers=headers1)
    # print(r1.status_code)
    # r1.encoding="UTF-8"
    # print(r1.text)
    # print(r1.headers['content-type'])
    # print(r1.encoding)

    # r2=requests.get(url2,params={"kw":"赛博朋克2077"})
    # print(r2.status_code)
    # print(r2.text)
    # print(r2.url)


    # r2=requests.head(url1)
    # print(r2.text)
    # print(r2.status_code)
    # print(r2.headers['content-type'])
    # print(r2.encoding)

    # r3=requests.post(url1)
    # print(r3.status_code)
    # print(r3.text)
    # print(r3.encoding)

    # r4=requests.options(url1)
    # print(r4.status_code)
    # print(r4.text)
    # print(r4.url)

    # r = requests.get('https://api.github.com/events/404')
    # print(r.status_code)
    # print(r.raise_for_status())
    # print(r.text)
    # print(r.json())
    # print(r.content)

    url3="https://httpbin.org/post"
    url4="https://httpbin.org/get"
    # r=requests.post(url3,json={'key1':'value1','key2':'value2'},headers=headers)
    # print(r.text)

    # r=requests.post(url3,data={'key1':'value1','key2':'value2'})
    # print(r.text)

    # r=requests.get(url4)
    # print(r.text)
    # print(r.headers)

    url5 = 'http://dp.58corp.com/data-develop/task-list'
    url6='https://httpbin.org/cookies'

    cookies=dict(Cookie="wmda_uuid=7e9f46c2f9586cebac861571355b237d; wmda_new_uuid=1; wmda_visited_projects=%3B12590408761269; DP_SESSION_ID=74b789b3-5a3a-49ab-9346-0b61e754e742; SSO_SESSION_ID=ST-3722946-3HolqHNvdxt00mEoOgNG-passport-58corp-com; wmda_session_id_12590408761269=1616485499262-abc8b58f-de86-23de")
    cookies1=dict(cookies_are='working')


    r= requests.get(url5, headers=headers)
    print(r.status_code)
    print(r.text)

    # s=requests.session()
    # r=s.get(url1,headers=headers)
    # print(r.text)
    # print(r.cookies)
