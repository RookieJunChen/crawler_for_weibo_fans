# 导入需要的数据包
from selenium import webdriver
import time
# 将获取的cookie保存在json文件中
import json


# 首先创建函数(*^_^*)
def get_cookies():
    # 保存cookies的文件
    file = 'cookies.json'

    # 打开需要获取cookies的网站
    wb = webdriver.Chrome()
    wb.implicitly_wait(3)
    wb.get('https://weibo.cn')

    # 网站打开后，在时间内手动执行登录操作
    time.sleep(120)

    # 登录成功后，获取cookies并保存为json格式
    cookies = wb.get_cookies()
    print(cookies)
    print(type(cookies))
    fp = open(file, 'w')
    json.dump(cookies, fp)
    fp.close()

    # 关闭浏览器
    wb.close()


# 执行代码获得cookie
if __name__ == "__main__":
    get_cookies()
