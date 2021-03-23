# -*- encoding: utf-8 -*-
import json
import subprocess

from operation import scan_article, watch_video, exam
from userOperation import login, check
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random

from getData import dataTimeOperation
from getData import dataTimeOperation
import requests
import json
import requests
import json

import time
import datetime
import json
import pathlib


def get_diff(date_str):
    """
    获取两个日期之差
    :param date_str: 日期字符串
    :return: 差值
    """
    now_time = time.localtime(time.time())
    compare_time = time.strptime(date_str, "%Y-%m-%d")
    date1 = datetime.datetime(compare_time[0], compare_time[1], compare_time[2])
    date2 = datetime.datetime(now_time[0], now_time[1], now_time[2])
    diff_days = (date2 - date1).days
    return diff_days


def is_get_data(file_type):
    dataPath = './data/lastTime.json'
    if not pathlib.Path(dataPath).is_file():
        with open(dataPath, 'w', encoding='utf-8') as f:
            dataDict = {
                'articles': '2020-01-01',
                'videos': '2020-01-01'
            }
            f.write(json.dumps(dataDict, ensure_ascii=False, indent=4))
        return True
    else:
        with open(dataPath, 'r', encoding='utf-8') as f:
            lastTime = json.loads(f.read())
            diff_days = get_diff(lastTime[file_type])
    return diff_days > 30


def set_time(file_type):
    dataPath = './data/lastTime.json'
    with open(dataPath, 'r', encoding='utf-8') as f:
        dataDict = json.loads(f.read())
        dataDict[file_type] = time.strftime("%Y-%m-%d", time.localtime())
    with open(dataPath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dataDict, ensure_ascii=False, indent=4))

#
# if __name__ == '__main__':
#     print(get_diff('2020-12-1'))
#     is_get_data('articles')


def get_video():
    if not dataTimeOperation.is_get_data('videos'):
        return
    headers = {
        "Accept": "application/json",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "www.xuexi.cn",
        "Referer": "https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/b87d700beee2c44826a9202c75d18c85.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    articles = requests.get(url='https://www.xuexi.cn/lgdata/4d82ahlubmol.json', headers=headers)
    with open('./data/videos.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(json.loads(articles.content), ensure_ascii=False, indent=4))
    dataTimeOperation.set_time('videos')
    print('--> 视频数据更新成功')

#
# if __name__ == '__main__':
#     get_video()
#

def get_article():
    if not dataTimeOperation.is_get_data('articles'):
        return
    headers = {
        "Accept": "application/json",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "www.xuexi.cn",
        "Referer": "https://www.xuexi.cn/4f5aa999a479568bf620109395d8fe56/69fe65d658afc891dd105e1ce9e5879d.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    articles = requests.get(url='https://www.xuexi.cn/lgdata/u1ght1omn2.json', headers=headers)
    with open('./data/articles.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(json.loads(articles.content), ensure_ascii=False, indent=4))
    dataTimeOperation.set_time('articles')
    print('--> 文章数据更新成功')

# # from getData import get_article, get_video
# if __name__ == '__main__':
#     get_article()
#

def article_or_video():
    """
    伪随机(在随机浏览文章或视频的情况下，保证文章或视频不会连续2次以上重复出现)，浏览文章或视频
    :return: 1(文章)或2(视频)
    """
    rand = random.randint(1, 2)
    if len(randArr) >= 2 and randArr[len(randArr) - 1] + randArr[len(randArr) - 2] == 2:
        rand = 2
    elif len(randArr) >= 2 and randArr[len(randArr) - 1] + randArr[len(randArr) - 2] == 4:
        rand = 1
    randArr.append(rand)
    return rand


def user_login():
    """
    登录，循环执行，直到登录成功
    :return:
    """
    while not login.login(browser):
        print('--> 登录超时，正在尝试重新登录')
        continue


def run():
    """
    刷视频，刷题目主要部分
    通过check_task()函数决定应该执行什么任务，并调用相应任务函数
    :return: null
    """
    while True:
        checkRes = check.check_task(browser)
        if checkRes == check.CheckResType.NULL:
            break
        elif checkRes == check.CheckResType.ARTICLE:
            scan_article.scan_article(browser)
        elif checkRes == check.CheckResType.VIDEO:
            watch_video.watch_video(browser)
        elif checkRes == check.CheckResType.ARTICLE_AND_VIDEO:
            if article_or_video() == 1:
                scan_article.scan_article(browser)
            else:
                watch_video.watch_video(browser)
        else:
            exam.to_exam(browser, checkRes)


def finally_run():
    """
    程序最后执行的函数，包括储存cookies，关闭浏览器等
    :return: null
    """
    # 获取cookies并保存
    jsonCookies = json.dumps(browser.get_cookies())
    with open('data/cookies.json', 'w') as f:
        f.write(jsonCookies)

    browser.quit()

    print(r'''
      __/\\\\\\\\\\\\\____/\\\________/\\\__________/\\\\\\\\\\\\__/\\\\\\\\\\\\_____/\\\\\\\\\\\\\\\_        
       _\/\\\/////////\\\_\///\\\____/\\\/_________/\\\//////////__\/\\\////////\\\__\/\\\///////////__       
        _\/\\\_______\/\\\___\///\\\/\\\/__________/\\\_____________\/\\\______\//\\\_\/\\\_____________      
         _\/\\\\\\\\\\\\\\______\///\\\/___________\/\\\____/\\\\\\\_\/\\\_______\/\\\_\/\\\\\\\\\\\_____     
          _\/\\\/////////\\\_______\/\\\____________\/\\\___\/////\\\_\/\\\_______\/\\\_\/\\\///////______    
           _\/\\\_______\/\\\_______\/\\\____________\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\_____________   
            _\/\\\_______\/\\\_______\/\\\____________\/\\\_______\/\\\_\/\\\_______/\\\__\/\\\_____________  
             _\/\\\\\\\\\\\\\/________\/\\\____________\//\\\\\\\\\\\\/__\/\\\\\\\\\\\\/___\/\\\_____________ 
              _\/////////////__________\///______________\////////////____\////////////_____\///______________ 
            ''')
    subprocess.call('pause', shell=True)

#
#
# 解决 'chromedriver' executable needs to be in PATH.'报错
# 试了把chromedriver.exe放到chrome安装文件下，python安装文件下，然后把路径配到path里，均无用。
## 最后是修改函数调用得以解决：#
# from selenium import  webdriver#
# browser = webdriver.Chrome(executable_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver_X64.exe')
# browser.get('http://www.baidu.com')
# import tkinter
# import tkinter.messagebox #这个是消息框，对话框的关键
# tkinter.messagebox.showinfo('提示','人生苦短')


if __name__ == "__main__":
    import tkinter
    import tkinter.messagebox

    print0 = "请在5分钟内扫码完成登录！需要x64位系统大内存 "
    print1 = "请确认已经连上护互联网，可以用 https://pc.xuexi.cn/points/login.html 测试！ \r 然后在5分钟内扫码完成登录！\r "
    print2 = "脚本运行过程中请勿关闭或最小化浏览器，否则可能会失败，系统需要大内存x64位,"

    print(print0, "！！")
    print(print1, "！！")
    print(print2, "！！")

    chrome_options = Options()
    chrome_options.add_argument("--mute-audio")  # 静音
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
    chrome_options.add_argument('--ignore-certificate-errors')     # 忽略证书错误
    chrome_options.add_argument('--ignore-ssl-errors')             # 忽略ssl错误
    browser = webdriver.Chrome(options=chrome_options)
    ###chromeoptions=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ###browser = webdriver.Chrome(executable_path=chromeoptions)
    browser.maximize_window()

    exam_temp_Path = './data/exam_temp.json'
    try:
        with open(exam_temp_Path, 'w', encoding='utf-8') as f:
            dataDict = {
                'DAILY_EXAM': 'true',
                'WEEKLY_EXAM': 'true',
                'SPECIAL_EXAM': 'true'
            }
            f.write(json.dumps(dataDict, ensure_ascii=False, indent=4))

        get_article()
        get_video.get_video()
        user_login()
        randArr = []  # 存放并用于判断随机值，防止出现连续看文章或者看视频的情况
        run()
        print('--> 任务全部完成，程序已结束')
    except BaseException as e:
        print(e)
        print('--> 程序异常，请尝试重启脚本')
    finally:
        import os
        os.remove(exam_temp_Path)
        finally_run()
