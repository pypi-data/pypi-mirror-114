# coding=utf-8
# 学习selenium 2021-04-15
# 获取百度贴吧的cookie，便于使用cookie免密登录 2021-04-15
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from sampleSprider.Common.Info import Tieba

# 设置页面加载策略为 在加载完html后开始执行selenium
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"
def main():
    option=webdriver.ChromeOptions()
    option.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"')

    driver=webdriver.Chrome('D://谷歌驱动/chromedriver.exe',options=option)

    driver.get('https://tieba.baidu.com/')

    time.sleep(6)

    zhmmdl=driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__footerULoginBtn"]')
    zhmmdl.click()
    time.sleep(3)

    user_name=driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__userName"]')
    user_name.send_keys(Tieba[0])
    password=driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__password"]')
    password.send_keys(Tieba[1])
    dl=driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__submit"]')
    dl.click()

    time.sleep(5)
    cookies=driver.get_cookies()
    print(cookies)
    # select=driver.find_element_by_xpath('//*[@id="plc_frame"]/div[2]/div[2]/p[1]/select')
    # options=select.find_elements_by_tag_name('option')
    # for option in options:
    #     print(option.text)
    #     option.click()

    # 操作select元素
    # select=Select(driver.find_element_by_xpath('//*[@id="plc_frame"]/div[2]/div[2]/p[1]/select'))
    # # select.select_by_index(2)
    # options=select.all_selected_options
    # for option in options:
    #     print(option.text)

    # alert=driver.switch_to.alert
    # print(alert.text)
    # for handle in driver.window_handles:
    #     driver.switch_to.window()

    # 浏览器后退和前进
    # elem=driver.find_element_by_xpath('//*[@id="weibo_top_public"]/div/div/div[2]/input')
    # elem.send_keys('赵立坚')
    # elem.send_keys(Keys.RETURN)
    # time.sleep(2)
    # driver.back()
    # time.sleep(3)
    # driver.forward()