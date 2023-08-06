# coding=utf-8
# 使用selenium实现免密登录贴吧，并获取html 2021-04-15
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.support.ui import WebDriverWait

desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities['pageLoadStrategy']='none'

class page_source_exisits(object):
    def __call__(self,driver):
        try:
            return driver.page_source
        except BaseException:
            return False

class add_cookies(object):
    def __call__(self,driver):
        try:
            for cookie in selenium_cookies:
                driver.add_cookie(cookie)
            return True
        except BaseException:
            return False

def main():
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'tieba.baidu.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
    }

    option=webdriver.ChromeOptions()
    for header in headers.items():
        option.add_argument('{}="{}"'.format(header.__getitem__(0),header.__getitem__(1)))

    driver=webdriver.Chrome('D://谷歌驱动/chromedriver.exe',options=option)

    driver.get('https://tieba.baidu.com/')


    selenium_cookies=[
        {'domain': '.tieba.baidu.com', 'expiry': 1621043898, 'httpOnly': True, 'name': 'STOKEN', 'path': '/', 'secure': False, 'value': '4dd187b74496abb206bcadec7b194361e316aec330f6d0f9ed2f026a5c4419a6'},
        {'domain': '.baidu.com', 'expiry': 1877651897, 'httpOnly': True, 'name': 'BDUSS_BFESS', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'MySjBDUGRmTX5oWlZxOTJzS0pTZDNNY1pwcUdaeTNlYkhIVGJyN0dKNjVLcDlnRVFBQUFBJCQAAAAAAAAAAAEAAADrkk43tfG~zMLWwKowAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALmdd2C5nXdgND'},
        {'domain': '.tieba.baidu.com', 'httpOnly': False, 'name': 'Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948', 'path': '/', 'secure': False, 'value': '1618451888'},
        {'domain': '.tieba.baidu.com', 'expiry': 1649987887, 'httpOnly': False, 'name': 'Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948', 'path': '/', 'secure': False, 'value': '1618451888'},
        {'domain': '.baidu.com', 'expiry': 1877651897, 'httpOnly': True, 'name': 'BDUSS', 'path': '/', 'secure': False, 'value': 'MySjBDUGRmTX5oWlZxOTJzS0pTZDNNY1pwcUdaeTNlYkhIVGJyN0dKNjVLcDlnRVFBQUFBJCQAAAAAAAAAAAEAAADrkk43tfG~zMLWwKowAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALmdd2C5nXdgND'},
        {'domain': '.baidu.com', 'expiry': 1649987886, 'httpOnly': False, 'name': 'BAIDUID_BFESS', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'B58886C02FFA16885AC661DCD59D8B38:FG=1'},
        {'domain': '.baidu.com', 'expiry': 1649987886, 'httpOnly': False, 'name': 'BAIDUID', 'path': '/', 'secure': False, 'value': 'B58886C02FFA16885AC661DCD59D8B38:FG=1'}
    ]

    # time.sleep(10)
    # try:
    #     for cookie in selenium_cookies:
    #         driver.add_cookie(cookie)
    # except BaseException:
    #     time.sleep(10)
    #     for cookie in selenium_cookies:
    #         driver.add_cookie(cookie)

    WebDriverWait(driver,20).until(add_cookies())

    driver.refresh()

    page_source=WebDriverWait(driver,20).until(page_source_exisits())
    print(page_source)

    driver.quit()