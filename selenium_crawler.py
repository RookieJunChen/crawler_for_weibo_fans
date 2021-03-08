# coding=utf-8

import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from processdata import get_constellation, get_age, get_address, organize_data
import json
import re


# 读取原来保存的cookies
def readcookies():
    file = 'cookies.json'
    fp = open(file, 'r')
    cookies = json.load(fp)
    fp.close()
    print("成功读取cookie文件")
    return cookies


# 将数据写入.json文件中
def write_result(file, data):
    fp = open(file, 'w')
    json.dump(data, fp)
    fp.close()
    print("成功保存数据")


# 获取粉丝信息
def get_fan_info(browser, fan):
    info = {}
    browser.execute_script("arguments[0].click();", fan)
    browser.implicitly_wait(10)
    try:
        # 点击主页
        time.sleep(2)
        choices = browser.find_elements_by_xpath("//li")
        browser.execute_script("arguments[0].click();", choices[0])
        # browser.implicitly_wait(2)
        time.sleep(0.5)

        # 收集昵称
        name = browser.find_element_by_xpath("//span[@class='txt-shadow']")
        info['昵称'] = name.text

        # 收集简介
        ins = browser.find_element_by_xpath("//p[@class='mod-fil-desc m-text-cut']")
        info['简介'] = ins.text

        # 通过图标判断性别
        sex = browser.find_element_by_xpath("//span[@class='mod-fil-n']//i")
        if sex is None:
            pass
        else:
            if sex.get_attribute("class") == "m-icon m-icon-male":
                info['性别'] = '男'
            else:
                info['性别'] = '女'

        # 收集其余信息
        keys = browser.find_elements_by_xpath("//div[@class='box-left']")
        values = browser.find_elements_by_xpath("//div[@class='box-main m-box-col']")
        if len(keys) > 0:
            for i in range(len(keys)):
                if keys[i].text == '信息':
                    info['地域'] = get_address(values[i].text)
                    info['年龄'] = get_age(values[i].text)
                    info['星座'] = get_constellation(values[i].text)
                    continue
                if keys[i].text == '所在地':
                    if '地域' not in info.keys():
                        info['地域'] = values[i].text
                    continue

                info[keys[i].text] = values[i].text

        # 按下返回键
        button = browser.find_element_by_xpath("//div[@class='nav-left']//i")
        action = ActionChains(browser)
        action.move_by_offset(2, 2)
        action.click(button)
        action.perform()
        time.sleep(1)
        return info
    except BaseException:
        # 按下返回键
        button = browser.find_element_by_xpath("//div[@class='nav-left']//i")
        action = ActionChains(browser)
        action.move_by_offset(2, 2)
        action.click(button)
        action.perform()
        time.sleep(1)
        return info


def get_total_info(browser, choice):
    choice_num = 0
    if choice == 'fans':
        choice_num = 1
    else:
        choice_num = 0

    # 点击进入粉丝/关注界面
    texts = browser.find_elements_by_xpath("//div[@class='m-box-center-a']//i")
    print(texts[choice_num].text)
    browser.execute_script("arguments[0].click();", texts[choice_num])
    time.sleep(5)

    # 向下拖动滚轮
    for i in range(150):
        js = "document.documentElement.scrollTop=100000000"
        browser.execute_script(js)
        time.sleep(0.5)

    # 爬取粉丝数据
    fans = browser.find_elements_by_xpath("//div[@class='m-box-col m-box-dir m-box-center']")
    length = len(fans)
    info_list = []
    for i in range(length):
        fans = browser.find_elements_by_xpath("//div[@class='m-box-col m-box-dir m-box-center']")
        info_list.append(get_fan_info(browser, fans[i]))
        print(str(i + 1) + "/" + str(length))

    # 按返回键
    button = browser.find_element_by_xpath("//div[@class='nav-left']//i")
    action = ActionChains(browser)
    action.move_by_offset(2, 2)
    action.click(button)
    action.perform()
    time.sleep(1)
    return info_list


if __name__ == "__main__":
    # 创建Chrome的无头浏览器
    # opt = webdriver.ChromeOptions()
    # opt.set_headless()
    # browser = webdriver.Chrome(options=opt)

    name = "华中师范大学"
    cookies = readcookies()
    # 通过cookies来自动登录微博
    browser = webdriver.Chrome()
    browser.get("https://s.weibo.com/")
    for cookie in cookies:
        browser.add_cookie(cookie_dict=cookie)
    browser.get("https://s.weibo.com/")
    browser.implicitly_wait(10)

    # 切换到找人页面
    button = browser.find_element_by_xpath("//div[@class='nav']//a[@title='找人']")
    browser.execute_script("arguments[0].click();", button)
    browser.implicitly_wait(10)

    # 输入要搜索的人名
    browser.find_element_by_xpath("//div[@class='search-input']//input[@type='text']").send_keys(name)
    browser.implicitly_wait(10)

    # 点击搜索键
    button = browser.find_element_by_xpath("//div[@class='search']//button")
    browser.execute_script("arguments[0].click();", button)
    time.sleep(10)

    # 选择第一个，点进去
    links = browser.find_elements_by_xpath("//div[@class='info']//a[@class='name']")
    print(links[0].text)
    browser.execute_script("arguments[0].click();", links[0])
    browser.close()

    windows = browser.window_handles
    browser.switch_to.window(windows[-1])

    # 找到用户的oid
    oidstr = None
    while oidstr is None:
        pattern = re.compile("\$CONFIG\['oid'\]='(\d)*';")
        oidstr = re.search(pattern, browser.page_source)
        time.sleep(1)
    pattern2 = re.compile("(\d)+")
    oid = re.search(pattern2, oidstr.group(0))
    print(oid.group(0))

    # 根据用户oid进入相关网页
    url = "https://m.weibo.cn/profile/" + oid.group(0)
    browser.get(url)
    for cookie in cookies:
        browser.add_cookie(cookie_dict=cookie)
    browser.get(url)
    browser.implicitly_wait(10)

    # 爬关注数据
    print('爬关注数据:')
    follow_list = get_total_info(browser, choice='follow')
    organize_data(follow_list)

    # 爬粉丝数据
    print('爬粉丝数据:')
    fans_list = get_total_info(browser, choice='fans')
    organize_data(fans_list)

    browser.close()

    # 将数据写入文件中
    write_result("following.json", follow_list)
    write_result("fans.json", fans_list)

# windows = browser.window_handles
# browser.switch_to.window(windows[-1])
#
# browser.implicitly_wait(10)
# # time.sleep(10)
# browser.close()
#
# windows = browser.window_handles
# browser.switch_to.window(windows[0])
#
# browser.execute_script("arguments[0].click();", buttons[1])
