# coding=utf-8
# 利用获取的cookies，完成模拟登录淘宝网（cookies如果过期了，需要重新用Taobao1获取下cookies） 2021-04-16
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from sampleSprider.Common.Info import Paypal
from selenium.webdriver.common.action_chains import ActionChains
import time

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

with open('D://SampleSprider/taobao_cookies.txt','r') as file:
    cookies=eval(file.read())

class click_jiesuan(object):
    def __call__(self,driver):
        try:
            if driver.title.__contains__('确认订单'):
                return True
            else:
                span_jiesuan.click()
                return False
        except BaseException:
            return False

class enter_mima(object):
    def __call__(self,driver):
        try:
            span_mima=driver.find_element_by_xpath('//*[@id="payPassword_container"]/div/span')
            return span_mima
        except BaseException:
            return False


def main():
    options=webdriver.ChromeOptions()
    for header in headers:
        options.add_argument('{}="{}"'.format(header,headers[header]))
    driver=webdriver.Chrome('D://谷歌驱动/chromedriver.exe')
    driver.maximize_window()
    driver.get('https://cart.taobao.com/cart.htm?spm=a1z02.1.1997525049.1.U6BJfg&from=mini&ad_id=&am_id=&cm_id=&pm_id=1501036000a02c5c3739')

    for cookie in cookies:
        driver.add_cookie(cookie)

    #driver.refresh()
    driver.get('https://cart.taobao.com/cart.htm?spm=a1z02.1.1997525049.1.U6BJfg&from=mini&ad_id=&am_id=&cm_id=&pm_id=1501036000a02c5c3739')

    time.sleep(3)
    # 全选按钮
    label_all_select=driver.find_element_by_xpath('//*[@id="J_SelectAll1"]/div/label')
    label_all_select.click()

    # 结算按钮
    span_jiesuan=driver.find_element_by_xpath('//*[@id="J_Go"]/span')
    WebDriverWait(driver,20).until(click_jiesuan())

    # 提交订单按钮
    a_tijiao=driver.find_element_by_xpath('//*[@id="submitOrderPC_1"]/div/a[2]')
    a_tijiao.click()

    # 默认选择支付宝
    # 输入支付宝密码
    span_mima=WebDriverWait(driver,20).until(enter_mima())

    ActionChains(driver).move_to_element(span_mima).click().send_keys(Paypal[0]).perform()

    # 确认付款
    input_fukuan=driver.find_element_by_xpath('//*[@id="J_authSubmit"]')
    input_fukuan.click()