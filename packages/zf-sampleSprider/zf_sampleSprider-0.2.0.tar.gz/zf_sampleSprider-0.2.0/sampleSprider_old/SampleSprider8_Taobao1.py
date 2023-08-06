# coding=utf-8
# 先用selenium模拟登录淘宝网，拿到cookies 2021-04-16
# 将cookies保存在本地文件中 2021-04-22
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from sampleSprider.Common.Info import Taobao
headers = {
    'authority': 'gma.alicdn.com',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'image',
    'referer': 'https://a1.alicdn.com/',
    'accept-language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://a1.alicdn.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Origin': 'https://cart.taobao.com',
    'Pragma': 'no-cache',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Sec-WebSocket-Key': 'pgWIzG+W79r6suOOQTMNQQ==',
    'Upgrade': 'websocket',
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    'Cache-Control': 'no-cache',
    'Connection': 'Upgrade',
    'Sec-WebSocket-Version': '13',
    'if-none-match': 'W/"1efe-gibOP5kr+x7GzP3kayA6Wzcii4g"',
    'if-modified-since': 'Wed, 18 Jan 2017 08:06:30 GMT',
    'pragma': 'no-cache',
    'content-type': 'text/plain',
    'origin': 'https://cart.taobao.com',
}


def main():
    try:
        options=webdriver.ChromeOptions()
        for header in headers:
            options.add_argument('{}="{}"'.format(header,headers[header]))
        driver=webdriver.Chrome('D://谷歌驱动/chromedriver.exe')
        driver.get('https://cart.taobao.com/cart.htm?spm=a1z02.1.1997525049.1.U6BJfg&from=mini&ad_id=&am_id=&cm_id=&pm_id=1501036000a02c5c3739')

        username=driver.find_element_by_xpath('//*[@id="fm-login-id"]')
        username.send_keys(Taobao[0])
        password=driver.find_element_by_xpath('//*[@id="fm-login-password"]')
        password.send_keys(Taobao[1])
        password.send_keys(Keys.RETURN)

        time.sleep(5)
        print(driver.get_cookies())

        path='D://SampleSprider/'
        os.makedirs(path,exist_ok=True)
        with open(path+'taobao_cookies.txt','w') as file:
            file.write(driver.get_cookies().__str__())
        driver.quit()
    except BaseException:
        main()
