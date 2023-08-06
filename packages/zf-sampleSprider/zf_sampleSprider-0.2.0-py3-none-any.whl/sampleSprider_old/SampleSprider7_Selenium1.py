# coding=utf-8
# 用request方式实现免密登录 2021-04-15

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests

desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities['pageLoadStrategy']='none'
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
    selenium_cookies=[
        {'domain': '.tieba.baidu.com', 'expiry': 1621043898, 'httpOnly': True, 'name': 'STOKEN', 'path': '/', 'secure': False, 'value': '4dd187b74496abb206bcadec7b194361e316aec330f6d0f9ed2f026a5c4419a6'},
        {'domain': '.baidu.com', 'expiry': 1877651897, 'httpOnly': True, 'name': 'BDUSS_BFESS', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'MySjBDUGRmTX5oWlZxOTJzS0pTZDNNY1pwcUdaeTNlYkhIVGJyN0dKNjVLcDlnRVFBQUFBJCQAAAAAAAAAAAEAAADrkk43tfG~zMLWwKowAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALmdd2C5nXdgND'},
        {'domain': '.tieba.baidu.com', 'httpOnly': False, 'name': 'Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948', 'path': '/', 'secure': False, 'value': '1618451888'},
        {'domain': '.tieba.baidu.com', 'expiry': 1649987887, 'httpOnly': False, 'name': 'Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948', 'path': '/', 'secure': False, 'value': '1618451888'},
        {'domain': '.baidu.com', 'expiry': 1877651897, 'httpOnly': True, 'name': 'BDUSS', 'path': '/', 'secure': False, 'value': 'MySjBDUGRmTX5oWlZxOTJzS0pTZDNNY1pwcUdaeTNlYkhIVGJyN0dKNjVLcDlnRVFBQUFBJCQAAAAAAAAAAAEAAADrkk43tfG~zMLWwKowAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALmdd2C5nXdgND'},
        {'domain': '.baidu.com', 'expiry': 1649987886, 'httpOnly': False, 'name': 'BAIDUID_BFESS', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'B58886C02FFA16885AC661DCD59D8B38:FG=1'},
        {'domain': '.baidu.com', 'expiry': 1649987886, 'httpOnly': False, 'name': 'BAIDUID', 'path': '/', 'secure': False, 'value': 'B58886C02FFA16885AC661DCD59D8B38:FG=1'}
    ]

    requests_cookies={}
    for cookie in selenium_cookies:
        requests_cookies[cookie['name']] = cookie['value']

    r= requests.get('https://tieba.baidu.com/', headers=headers, cookies=requests_cookies)
    print(r.text)
