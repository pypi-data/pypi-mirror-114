# coding=utf-8
# 模拟登录拼多多，获取cookies 2021-04-27
from selenium import webdriver
import time

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://static.pddpic.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'Origin': 'http://mobile.pinduoduo.com',
    'sec-ch-ua-mobile': '?0',
    'authority': 'th.pinduoduo.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    'content-type': 'text/plain;charset=UTF-8',
    'accept': '*/*',
    'origin': 'http://mobile.pinduoduo.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'http://mobile.pinduoduo.com/',
    'accept-language': 'zh-CN,zh;q=0.9',
    'AccessToken': 'TDTVO6CI6S32K6UCKGJELOUUETBIFO6PWKA5JXSKB3CVX6OSF2XA1103853',
    'Content-Type': 'application/json;charset=UTF-8',
    'Pragma': 'no-cache',
}

def main(driver):
    url='http://mobile.pinduoduo.com/garden_home.html?_pdd_fs=1&_pdd_tc=676666&_pdd_sbs=1&fun_id=app_home&refer_page_el_sn=15079&refer_page_name=login&refer_page_id=10169_1619419956651_sowf5xitxz&refer_page_sn=10169'

    # cookies失效或者第一次使用
    if driver.current_url.__contains__('login.html'):
        # 手机登录
        phone_denglu=driver.find_element_by_xpath('//*[@id="first"]/div[2]/div')
        phone_denglu.click()
        phone_number=driver.find_element_by_xpath('//*[@id="user-mobile"]')
        phone_number.send_keys('13566421619')
        send_yzm=driver.find_element_by_xpath('//*[@id="code-button"]')
        time.sleep(1)
        send_yzm.click()
        yzm=input('请输入手机验证码：')
        input_yzm=driver.find_element_by_xpath('//*[@id="input-code"]')
        input_yzm.send_keys(yzm)
        denglu=driver.find_element_by_xpath('//*[@id="submit-button"]')
        denglu.click()

        time.sleep(3)
        with open('D://SampleSprider/pingduoduo_cookies.txt','w') as file:
            file.write(driver.get_cookies().__str__())
        print(driver.get_cookies())

