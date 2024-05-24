# -*- coding: utf-8 -*-
'''
使用事先保存在本地的cookies，登录网站
'''
import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq

def login_with_selenium(url,cookies_filename,save_filename=None):
    options = Options()
    #options.add_argument("--headless")  # 不打开浏览器界面，以节省时间
    browser = webdriver.Chrome(options=options)

    # 先建立连接, 随后才可以可修改cookie
    browser.get(url)
    browser.maximize_window()
    # 删除这次登录时，浏览器自动储存到本地的cookie
    browser.delete_all_cookies()

    # 读取之前已经储存到本地的cookie
    cookies_file = open(cookies_filename, 'r', encoding='utf-8')
    cookies_list = json.loads(cookies_file.read())
    print(cookies_list)

    for cookie in cookies_list:  # 把cookie添加到本次连接
        browser.add_cookie({
            'domain': cookie['domain'],  # 此处xxx.com前，需要带点
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expires': None
        })

    # 登录后查阅网站内容
    browser.implicitly_wait(10)
    browser.get(url)

    page_source = browser.page_source

    browser.quit()

    if save_filename:
        with open(save_filename, 'w', encoding='utf-8') as f:
            f.write(page_source)
    return page_source



def get_player_info(doc):
    # 找到包含玩家信息的父元素
    player_container = doc('#main-wrap > main > table > tbody')
    item_list = player_container.items('tr')

    player_info_list = []

    for item in item_list:
        ranking = item('td:nth-child(1)').text()

        title_name = item('td:nth-child(2)').text().split('\xa0')
        if len(title_name) == 2:
            title = title_name[0]
            name = title_name[1]
        else:
            title = ''
            name = title_name[0]
        
        score = item('td:nth-child(3)').text()
        score_diff = item('td:nth-child(4)').text()
        if item.find('bad') != []:
            score_diff = '-' + score_diff

        player_info = {
            'ranking': ranking,
            'title': title,
            'name': name,
            'score': score,
            'score_diff': score_diff
        }
        player_info_list.append(player_info)
    return player_info_list

def write_to_csv(player_info_list,csv_filename):
    # 写入csv文件
    out_filename = csv_filename
    out_file = open(out_filename, 'w', encoding='utf-8')
    out_file.write('ranking,title,name,score,score_diff\n')
    for player_info in player_info_list:
        out_file.write(player_info['ranking'] + ',' + player_info['title'] + ',' + player_info['name'] + ',' + player_info['score'] + ',' + player_info['score_diff'] + '\n')


save_filename='./output/page_source_bullet.html'
csv_filename='./output/player_info.csv'

page_source = login_with_selenium(url='https://lichess.org/player/top/200/bullet',
                                cookies_filename='./output/cookies_lichess.json',
                                save_filename=save_filename)

doc = pq(page_source)

player_info_list = get_player_info(doc)
write_to_csv(player_info_list,csv_filename)