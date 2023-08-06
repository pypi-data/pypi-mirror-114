# coding=utf-8
# 拼多多可以检测selenium脚本，以下为解决办法
# 1.在path下新增浏览器.exe目录 的环境变量
# 2.新建一个存放新环境的文件夹并映射 打开cmd  chrome.exe --remote-debugging-port=9222 --user-data-dir=“D:\data_info\selenium_data
# 3.会打开一个网页，不用关，运行下面代码即可

#define CO_MAXBLOCKS 40
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sampleSprider.SampleSprider9_Pinduoduo1 import main
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

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

with open('D://SampleSprider/pingduoduo_cookies.txt','r') as file:
    cookies=eval(file.read())

class click_jiaoshui(object):
    def __call__(self,driver):
        try:
            jiaoshui=driver.find_element_by_xpath('//*[@id="waterbottle"]/div[3]/div[1]/div/div/img')
            jiaoshui.click()
            return True
        except BaseException:
            try:
                jiaoshui2=driver.find_element_by_xpath('//*[@id="waterbottle"]/div[4]')
                jiaoshui2.click()
                return True
            except BaseException:
                return False

class click_lijicunru(object):
    def __call__(self,driver):
        try:
            lijicunru=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[57]/div/div[2]/div[3]/div/div[4]')
            lijicunru.click()
            return True
        except BaseException:
            return False

class click_zhidaole(object):
    def __call__(self,driver):
        try:
            zhidaole=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[57]/div/div[2]/div[3]/div/div[3]')
            zhidaole.click()
            return True
        except BaseException:
            return False

class fiveStates(object):
    def __call__(self,driver):
        try:
            lianxuqiandao=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[134]/div/div[2]/div[1]/div/div/img')
            lianxuqiandao.click()
            log.error('关闭 连续签到 提示成功。。。')
            return True
        except BaseException:
            try:
                huafeilibao=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[33]/div/div/div[3]/div[1]/div')
                huafeilibao.click()
                log.error('关闭 化肥礼包 提示成功。。。')
                return True
            except BaseException:
                try:
                    jiaoshuijiabei=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[169]/div/div[2]/button')
                    jiaoshuijiabei.click()
                    log.error('关闭 水满加倍 提示成功。。。')
                    return True
                except BaseException:
                    try:
                        zhuanpan=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[173]/div/div/div[2]/div/div[1]/div/div/div/img')
                        zhuanpan.click()
                        log.error('关闭 转盘抽奖 提示成功。。。')
                        return True
                    except BaseException:
                        try:
                            # 养分
                            qujiaoshui2=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[2]/div[2]/button')
                            gongxihuode2=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[2]/div[2]/div[2]').text
                            qujiaoshui2.click()
                            log.error('关闭 {} 提示成功。。。'.format(gongxihuode2))
                            return True
                        except BaseException:
                            return False

class click_lingshuidi(object):
    def __call__(self,driver):
        try:
            lingshuidi=driver.find_element_by_xpath('//*[@id="MissionListIcon"]/div/div/div[2]/img')
            lingshuidi.click()
            return True
        except BaseException:
            return False

class click_meirishuidi(object):
    def __call__(self,driver):
        try:
            meirishuidi=driver.find_element_by_xpath('//*[@id="missionlist-36155"]/div[3]/div/button')
            meirishuidi.click()
            log.info('领取每日水滴成功。。。')
            WebDriverWait(driver,5).until(close_meirishuidi())
            return True
        except BaseException:
            return False

class close_meirishuidi(object):
    def __call__(self,driver):
        try:
            close=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[77]/div/div[2]/div[2]/div/div/img')
            jixu=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[77]/div/div[2]/div[3]/div[4]/button[2]')
            jixu.click()
            log.info('关闭 每日水滴 提示成功。。。')
            return True
        except BaseException:
            return False

if __name__=='__main__':
    url='http://mobile.pinduoduo.com/garden_home.html?_pdd_fs=1&_pdd_tc=676666&_pdd_sbs=1&fun_id=app_home&refer_page_el_sn=15079&refer_page_name=login&refer_page_id=10169_1619419956651_sowf5xitxz&refer_page_sn=10169'

    options=webdriver.ChromeOptions()
    for header in headers:
        options.add_argument('{}="{}"'.format(header,headers[header]))

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  #  前面设置的端口号
    driver = webdriver.Chrome(executable_path='D://谷歌驱动/chromedriver.exe', options=chrome_options)

    log.info('开始访问拼多多果园。。。。')
    driver.get(url)
    driver.maximize_window()

    # for cookie in cookies:
    #     driver.add_cookie(cookie)

    # log.info('添加cookies后访问。。。。')
    # driver.get(url)
    # cookies失效或者第一次使用
    if driver.current_url.__contains__('login.html'):
        log.info('cookies失效或者第一次使用。。。。')
        main(driver)

    log.info('进入页面成功。。。')

    # log.info('开始做任务。。。')
    # WebDriverWait(driver,5).until(click_lingshuidi())
    # WebDriverWait(driver,5).until(click_meirishuidi())
    #
    # driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[2]/div[2]/div[3]/div[4]').find_element_by_class_name('title')


    for i in range(0,100000):
        try:
            WebDriverWait(driver,8).until(click_jiaoshui())
            log.info('正在点击浇水第{}次。。。'.format(i))
        except BaseException:
            try:
                WebDriverWait(driver,3).until(fiveStates())
            except BaseException:
                try:
                    jingxishuihu=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[3]/div[2]/div[3]/button')
                    jingxishuihu.click()
                    log.error('关闭 惊喜水壶 提示成功。。。')
                except BaseException:
                    try:
                        # 水滴
                        qujiaoshui=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[2]/div[2]/button')
                        gongxihuode=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[2]/div[2]/div[2]/div[1]/span').text
                        qujiaoshui.click()
                        log.error('关闭 {} 提示成功。。。'.format(gongxihuode))
                    except BaseException:
                        try:
                            zhuanpanfanbei=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[56]/div/div[2]/div[2]/div[3]/img')
                            zhuanpanfanbei.click()
                            WebDriverWait(driver,5).until(click_lijicunru())
                            WebDriverWait(driver,5).until(click_zhidaole())
                            log.error('关闭 送你水滴翻倍福利 提示成功。。。')
                        except BaseException:
                            try:
                                guoshuzhangguozi=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[5]/div/div[2]/div[2]')
                                guoshuzhangguozi.click()
                                log.error('关闭 果树长出果子了 提示成功。。。')
                            except BaseException:
                                try:
                                    xingyunhongbao=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[106]/div[4]/div[3]/button')
                                    xingyunhongbao.click()
                                    log.error('关闭 幸运红包 提示成功。。。')
                                except BaseException:
                                    shuidibuzu=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[76]/div/div[2]/div/div[2]/div/div/img')
                                    shuidibuzu.click()
                                    log.error('关闭 水滴 提示成功。。。')
                                    break

