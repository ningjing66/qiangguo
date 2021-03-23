
windows


color 1
color 2
color 3


python.exe xxqg.py


color a
color b
color c





# -*- encoding: utf-8 -*-
import json
import subprocess
from getData import getexam, getdata, getlogin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random


# from getData import get_article, get_video
# from operation import scan_article, watch_video, exam
# from userOperation import login, check


def article_or_video():

    # 2、执行命令Pyinstaller -F -w -i chengzi.ico py_word.py，执行过程特别漫长，就没有录制动图。
    # get_article 执行完毕会发现当前目录多了几个文件夹，打开其中名为dist的文件夹。
    # 伪随机(在随机浏览文章或视频的情况下，保证文章或视频不会连续2次以上重复出现)，浏览文章或视频
    # :return: 1(文章)或2(视频)

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
    while not getlogin.login(browser):
        print('--> 登录超时，正在尝试重新登录')
        continue


def run():
    """
    刷视频，刷题目主要部分
    通过check_task()函数决定应该执行什么任务，并调用相应任务函数
    :return: null
    """
    while True:
        checkRes = getlogin.check_task(browser)
        if checkRes == getlogin.CheckResType.NULL:
            break
        elif checkRes == getlogin.CheckResType.ARTICLE:
            getexam.scan_article(browser)
        elif checkRes == getlogin.CheckResType.VIDEO:
            getexam.watch_video(browser)
        elif checkRes == getlogin.CheckResType.ARTICLE_AND_VIDEO:
            if article_or_video() == 1:
                getexam.scan_article(browser)
            else:
                getexam.watch_video(browser)
        else:
            getexam.to_exam(browser, checkRes)


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

    print0 = "请在5分钟内扫码完成登录！需要x64位系统大内存 "
    print1 = "请确认已经连上护互联网，可以用 https://pc.xuexi.cn/points/login.html 测试！ \r 然后在5分钟内扫码完成登录！ "
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

        getdata.get_article()
        getdata.get_video()
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
