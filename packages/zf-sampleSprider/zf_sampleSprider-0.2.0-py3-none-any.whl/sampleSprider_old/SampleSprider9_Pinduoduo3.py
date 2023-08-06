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
                shengyu=jiaoshui2.text
                log.info('还剩余{}水'.format(shengyu))
                if int(str(shengyu).strip('g'))<10:
                    log.error('剩余水不足，停止浇水。。。')
                    return 2
                jiaoshui2.click()
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

# 领取左方的30分钟满水盆
class click_shuipen(object):
    def __call__(self, driver):
        try:
            shuipen=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[2]/div[1]/div[1]/div/div[3]/div/div[1]/img')
            shuipen.click()
            try:
                time.sleep(1)
                try:
                    weimanyig=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[92]/div/div[2]/div[2]/div[5]')
                except BaseException:
                    weimanyig=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[94]/div/div[2]/div[2]/div[5]')
                weimanyig.click()
                log.error('水盆未满1g不可领取')
                return 2
            except BaseException:
                log.info('领取水盆里的水滴成功。。。。')
                return 1
        except BaseException:
            return False

# 领取树右方的每日圆水瓶
class click_yuanping(object):
    def __call__(self, driver):
        try:
            try:
                yuanping=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[2]/div[1]/div[6]/div[3]/div/div/div[4]/div')
            except BaseException:
                try:
                    yuanping=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[2]/div[1]/div[6]/div[3]/div/div/div[4]/div/div[5]/div/span[2]')
                except BaseException:
                    driver.find_element_by_xpath('//*[@id="fruit-container"]/div[2]/div[1]/div[6]/div[3]/div/div/div[4]')
            ActionChains(driver).move_to_element(yuanping).click().perform()
            try:
                try:
                    yijiaoshui=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[172]/div/div[2]/button')
                    yijiaoshui.click()
                    log.error('今日已领取过圆瓶里的水滴了。。。。')
                    return 2
                except BaseException:
                    time.sleep(1)
                    yijiaoshui=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[171]/div/div[2]/button')
                    yijiaoshui.click()
                    try:
                        chacha=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[75]/div/div[2]/div/div[2]/div/div/img')
                        chacha.click()
                        log.error('剩余水滴不足')
                        return True
                    except BaseException:
                        log.error('今日已领取过圆瓶里的水滴了。。。。')
                        return 2
            except BaseException:
                log.info('领取圆瓶里的水滴成功。。。。')
                return 1
        except BaseException:
            return False

# 打卡集水滴
class click_daka(object):
    def __call__(self, driver):
        try:
            try:
                daka=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div/div[3]')
            except BaseException:
                daka=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div')
            daka.click()
            try:
                daka_next=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[139]/div/div[2]/div[4]/div[3]')
            except BaseException:
                daka_next=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[138]/div/div[2]/div[4]/div[3]')
            daka_next.click()
            chacha=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[138]/div/div[2]/div[1]/div/div/img')
            chacha.click()
            if daka_next.text == '今日已打卡':
                log.error('今日已打卡...')
            else:
                log.info('打卡集水滴成功。。。。')
            return True
        except BaseException:
            return False

# 每日三餐开福袋
class click_sancanfudai(object):
    def __call__(self, driver):
        try:
            sancanfudai=driver.find_element_by_xpath('//*[@id="14"]')
            ActionChains(driver).move_to_element(sancanfudai).click().perform()
            qujiaoshui=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[35]/div[2]/div[4]/button')
            qujiaoshui.click()
            log.info('三餐福袋领取成功。。。。')
            return True
        except BaseException:
            return False

# 浇水竞赛
class click_jiaoshuijingsai(object):
    def __call__(self, driver):
        try:
            jiaoshuijingsai=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[1]/div[1]/div[3]/div[1]/div/div/div/div[1]/img')
            ActionChains(driver).move_to_element(jiaoshuijingsai).click().perform()
            log.info('点击浇水竞赛.....')

            state=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[118]/div[1]/div/div[3]/div[2]/div[2]/div[2]')
            state_text=state.text
            if state_text!='待完成':
                state.click()
                log.info('浇水竞赛前三名奖励领取成功')
            chacha=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[9]/div[32]/div[118]/div[1]/div/div[3]/div[1]/div[2]/div/div/img')
            chacha.click()
            log.error('浇水竞赛未达到前三名....')
            return True
        except BaseException:
            return False

# 幸运红包
class click_xingyunhongbao(object):
    def __call__(self, driver):
        try:
            xingyunhongbao=driver.find_element_by_xpath('//*[@id="progress-bar-id"]/div/div[2]/div/div/div/div[2]/div[2]/img')
            xingyunhongbao.click()
            log.info('正在点击幸运红包 。。。')
            return True
        except BaseException:
            return False

class click_toushui(object):
    def __call__(self, driver):
        try:
            toushui=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[2]/div[1]/div[3]/div/div[4]/div[2]/img')
            toushui.click()
            log.info('点击偷水。。。')
            return True
        except BaseException:
            return False

class visit_friends(object):
    def __call__(self, driver):
        try:
            friends_list=driver.find_element_by_xpath('//*[@id="friendList"]').find_elements_by_class_name('friend-list-item')
            for friend in friends_list:
                friend_name=friend.find_element_by_class_name('friend-name').text
                if friend_name != '删除好友':
                    friend.click()
                    try:
                        WebDriverWait(driver,5).until(click_toushui())
                    except BaseException:
                        driver.get(url)

            log.info('访问所有好友成功...')
            huijia=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/img')
            huijia.click()
            return True
        except BaseException:
            return False

# 领化肥
class click_linghuafei(object):
    def __call__(self, driver):
        try:
            linghuafei=driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[1]/div[1]/div[2]/div/div[3]/div[2]/img')
            linghuafei.click()
            log.info('正在点击 领化肥。。。')
            time.sleep(1)
            try:
                linghuafei_daka=driver.find_element_by_xpath('//*[@id="missionlist-36069"]/div[3]/div/button')
                linghuafei_daka.click()
                log.info('成功打卡领化肥。。。')
            except BaseException:
                log.error('已打卡，稍后再点。。。')

            liulan=driver.find_element_by_xpath('//*[@id="missionlist-36029"]/div[3]/div[2]/button')
            liulan.click()

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

    current_hour=time.strftime("%H", time.localtime())
    log.info('当前时间为{}点。。。'.format(current_hour))
    if int(current_hour) in (7,8,9,12,13,14,18,19,20,21):
        try:
            WebDriverWait(driver,3).until(click_sancanfudai())
        except BaseException:
            log.error('未弹出三餐福袋或已领取过。。。')

    # log.info('开始做任务。。。')
    # WebDriverWait(driver,5).until(click_lingshuidi())
    # WebDriverWait(driver,5).until(click_meirishuidi())
    #
    # driver.find_element_by_xpath('//*[@id="fruit-container"]/div[4]/div/div/div[2]/div[2]/div[2]/div[3]/div[4]').find_element_by_class_name('title')

    try:
        WebDriverWait(driver,5).until(click_shuipen())
    except BaseException:
        log.error('界面找不到集水器。。。')

    try:
        WebDriverWait(driver,5).until(click_yuanping())
    except BaseException:
        log.error('界面找不到圆瓶。。。')

    try:
        WebDriverWait(driver,5).until(click_linghuafei())
    except BaseException:
        log.error('界面找不到领化肥。。。')

    try:
        WebDriverWait(driver,5).until(click_daka())
        driver.get(url)
    except BaseException:
        log.error('界面找不到打卡集水滴')

    try:
        WebDriverWait(driver,5).until(click_jiaoshuijingsai())
    except BaseException:
        log.error('界面找不到浇水竞赛')

    try:
        WebDriverWait(driver,5).until(visit_friends())
    except BaseException:
        log.error('界面找不到好友列表')

    for i in range(0,100000):
        try:
            res=WebDriverWait(driver,5).until(click_jiaoshui())
            if res==2:
                break
            log.info('正在点击浇水第{}次。。。'.format(i))
        except BaseException:
            driver.get(url)

    driver.get(url)
    try:
        WebDriverWait(driver,4).until(click_xingyunhongbao())
        driver.get(url)
    except BaseException:
        log.error('界面找不到幸运红包')