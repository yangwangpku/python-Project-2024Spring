# -*- coding: utf-8 -*-
'''
配合手工操作登录网站，获取cookies，保存到本地，以备后续使用
'''
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #用于设置浏览器启动的一些参数
import time

options = Options()
#options.add_argument("--headless")  # 不打开浏览器界面，以节省时间
browser = webdriver.Chrome(options=options)
browser.get('https://lichess.org/login')
browser.maximize_window()

input("请登录，然后按回车……")  # 等待用手机扫码登录, 登录后回车即可

cookies_dict = browser.get_cookies()
cookies_json = json.dumps(cookies_dict)
#print(cookies_json)

# 登录完成后,将cookies保存到本地文件
out_filename = './output/cookies_lichess.json'
out_file = open(out_filename, 'w', encoding='utf-8')
out_file.write(cookies_json)
out_file.close()
print('Cookies文件已写入：' + out_filename)

time.sleep(1)
browser.quit()
