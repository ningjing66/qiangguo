# -*- encoding: utf-8 -*-
import json
import subprocess

# bing冰淇淋
# from getData import dataTimeOperation
# from getData import dataTimeOperation
# from operation import scan_article, watch_video, exam
# from userOperation import login, check
#


from enum import Enum
from datetime import datetime
from rich import print
from rich.table import Column, Table
from rich.progress import Progress
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from data import dataTimeOperation
import requests
import json
import time
import datetime
import json
import pathlib
import selenium
import random
import difflib
import re

#
# from userOperation import check
# from selenium import webdriver
# from selenium import webdriver
# import json
# import time
# import random
# from rich.progress import Progress
#


def get_video():
    if not is_get_data('videos'):
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
    set_time('videos')
    print('--> 视频数据更新成功')


def logout(browser):
    browser.get('https://www.xuexi.cn/')
    time.sleep(round(random.uniform(1, 2), 2))
    logoutBtn = browser.find_element_by_xpath('//*[@id="root"]/div/header/div[2]/div[2]/span/a')
    logoutBtn.click()

#
# if __name__ == '__main__':
#     browser = webdriver.Chrome()
#     logout(browser)
#

class CheckResType(Enum):
    NULL = 0
    ARTICLE = 1
    VIDEO = 2
    ARTICLE_AND_VIDEO = 3
    DAILY_EXAM = 4
    WEEKLY_EXAM = 5
    SPECIAL_EXAM = 6


def check_task(browser):
    """
    检查任务项并返回给主程序
    :param browser: browser
    :return: CheckResType：任务类型
    """
    # table = PrettyTable(["每日登录", "选读文章", "视频数量", "视频时长", "每日答题", "每周答题", "专项答题", "今日累计积分", "成长总积分"])
    table = Table(show_header=True, header_style="bold black")
    table.add_column("每日登录", justify='center')
    table.add_column("选读文章", justify='center')
    table.add_column("视频数量", justify='center')
    table.add_column("视频时长", justify='center')
    table.add_column("每日答题", justify='center')
    table.add_column("每周答题", justify='center')
    table.add_column("专项答题", justify='center')
    table.add_column("今日累计积分", justify='center')
    table.add_column("成长总积分", justify='center')
    tableRow = []
    settingsPath = 'data/settings.json'
    with open(settingsPath, 'r', encoding='utf-8') as f:
        settings = f.read()
    # print(settings)
    settings = json.loads(settings)

    exam_temp_Path = './data/exam_temp.json'
    with open(exam_temp_Path, 'r', encoding='utf-8') as f:
        exam_temp = f.read()
    exam_temp = json.loads(exam_temp)

    res = CheckResType.NULL
    browser.get('https://www.xuexi.cn/index.html')
    time.sleep(round(random.uniform(1, 3), 2))
    browser.get('https://pc.xuexi.cn/points/my-points.html')
    browser.implicitly_wait(3)
    time.sleep(round(random.uniform(1, 3), 2))

    # 每日登录积分
    login = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]')
    tableRow.append(login.text.strip())

    # 选读文章积分
    article = browser.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div[2]')
    tableRow.append(article.text.strip())
    # 视听学习积分
    video = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[3]/div[2]/div[3]/div[2]/div[1]/div[2]')
    tableRow.append(video.text.strip())
    # 视听学习时长积分
    video_time = browser.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div/div[3]/div[2]/div[4]/div[2]/div[1]/div[2]')
    tableRow.append(video_time.text.strip())
    # 每日答题积分
    daily = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[1]/div[2]')
    tableRow.append(daily.text.strip())
    # 每周答题积分
    weekly = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[1]/div[2]')
    tableRow.append(weekly.text.strip())
    # 专项答题积分
    special = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[7]/div[2]/div[1]/div[2]')
    tableRow.append(special.text.strip())
    # 今日积分
    todayPoints = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[2]/span[3]')
    tableRow.append(todayPoints.text.strip())
    # 总积分
    allPoints = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[2]/span[1]')
    tableRow.append(allPoints.text.strip())

    # 打印表格
    table.add_row(tableRow[0],
                  tableRow[1],
                  tableRow[2],
                  tableRow[3],
                  tableRow[4],
                  tableRow[5],
                  tableRow[6],
                  tableRow[7] + '分',
                  tableRow[8] + '分')
    print(table)

    if settings['浏览文章'] == "true" and article.text != '12分/12分':
        res = CheckResType.ARTICLE
    if settings['观看视频'] == "true" and (video.text != '6分/6分' or video_time.text != '6分/6分'):
        if res == CheckResType.ARTICLE:
            res = CheckResType.ARTICLE_AND_VIDEO
        else:
            res = CheckResType.VIDEO

    # 检查设置文件
    if settings['自动答题'] != 'true':
        return res

    # dayOfWeek = str(time.now().isoweekday())
    dayOfWeek = '2021-1-1'
    if settings['每日答题'] == 'true' and res == CheckResType.NULL and daily.text != '5分/5分':
        if settings['答题时间设置']['是否启用(关闭则每天都答题)'] != 'true' or (settings['答题时间设置']['是否启用(关闭则每天都答题)'] == 'true' and dayOfWeek in settings['答题时间设置']['答题类型(数字代表星期几)']['每日答题']):
            res = CheckResType.DAILY_EXAM
    if exam_temp['WEEKLY_EXAM'] == 'true' and settings['每周答题'] == 'true' and res == CheckResType.NULL and weekly.text != '5分/5分':
        if settings['答题时间设置']['是否启用(关闭则每天都答题)'] != 'true' or (settings['答题时间设置']['是否启用(关闭则每天都答题)'] == 'true' and dayOfWeek in settings['答题时间设置']['答题类型(数字代表星期几)']['每周答题']):
            res = CheckResType.WEEKLY_EXAM
    if exam_temp['SPECIAL_EXAM'] == 'true' and settings['专项答题'] == 'true' and res == CheckResType.NULL and special.text != '10分/10分':
        if settings['答题时间设置']['是否启用(关闭则每天都答题)'] != 'true' or (settings['答题时间设置']['是否启用(关闭则每天都答题)'] == 'true' and dayOfWeek in settings['答题时间设置']['答题类型(数字代表星期几)']['专项答题']):
            res = CheckResType.SPECIAL_EXAM

    return res





def add_cookie_login(browser):
    """
    自动登录流程，读取cookie文件，添加cookie，并尝试登录
    :param browser: browser
    :return: bool，表示是否登录成功
    """
    print('--> 尝试自动登陆')
    with open('data/cookies.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        if cookie['name'] != 'token':
            continue
        browser.add_cookie({
            'domain': cookie['domain'],
            'name': cookie['name'],
            'value': cookie['value'],
            'path': cookie['path'],
            'secure': cookie['secure'],
            'httpOnly': cookie['httpOnly']
        })
    browser.get('https://pc.xuexi.cn/points/my-points.html')
    browser.implicitly_wait(5)
    time.sleep(1)
    if browser.current_url == 'https://pc.xuexi.cn/points/my-points.html':
        print('--> 自动登录成功')
        jsonCookies = json.dumps(browser.get_cookies())
        with open('data/cookies.json', 'w') as f:
            f.write(jsonCookies)
        return True
    print('--> 自动登录失败，准备扫码登录')
    return False


def normal_login(browser):
    """
    正常扫码登录流程
    :param browser: browser
    :return: bool，表示是否登录成功
    """
    print('--> 请在5分钟内扫码完成登录')
    browser.implicitly_wait(10)
    iframe = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/div/iframe')
    browser.switch_to.frame(iframe)
    login_QR_box = browser.find_element_by_xpath('/html/body/div/div/div[1]')
    browser.execute_script('arguments[0].scrollIntoView();', login_QR_box)

    for i in range(60):
        if browser.current_url == 'https://pc.xuexi.cn/points/my-points.html':
            print('--> 登录成功')
            jsonCookies = json.dumps(browser.get_cookies())
            with open('data/cookies.json', 'w') as f:
                f.write(jsonCookies)
            return True
        time.sleep(5)
    return False


def login(browser):
    """
    全部登录流程，将登录的最终结果返回给主程序
    :param browser: browser
    :return: bool，表示是否登录成功
    """
    browser.get('https://pc.xuexi.cn/points/my-points.html')
    time.sleep(2.5)
    settingsPath = 'data/settings.json'
    with open(settingsPath, 'r', encoding='utf-8') as f:
        settings = f.read()
    settings = json.loads(settings)
    if settings['保持登陆'] == "true":
        try:
            login_res = add_cookie_login(browser)
            if not login_res:
                login_res = normal_login(browser)
        except IOError:
            login_res = normal_login(browser)
    else:
        login_res = normal_login(browser)

    return login_res

#
# if __name__ == '__main__':
#     browser = webdriver.Chrome()
#     login(browser)



def watch_video(browser):
    videoPath = 'data/videos.json'
    with open(videoPath, 'r', encoding='utf-8') as f:
        videos = f.read()
    # print(videos)
    videos = json.loads(videos)
    while True:
        randIndex = random.randint(0, len(videos) - 1)
        if videos[randIndex]['type'] != 'shipin':
            del videos[randIndex]
            continue
        else:
            break

    url = videos[randIndex]['url']
    browser.get('https://www.xuexi.cn/0809b8b6ab8a81a4f55ce9cbefa16eff/ae60b027cb83715fd0eeb7bb2527e88b.html')
    time.sleep(round(random.uniform(1, 3), 2))
    browser.get('https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html#t1jk1cdl7l-5')
    time.sleep(round(random.uniform(1, 3), 2))
    browser.get(url)
    time.sleep(round(random.uniform(3, 6), 2))
    video = browser.find_element_by_xpath('/html/body/div/div/section/div/div/div/div/div[2]/section/div/div/div/div/div/div/div/div[1]/div[2]/div/div[1]/div[1]/div/video')
    start = browser.find_element_by_xpath(
        '/html/body/div/div/section/div/div/div/div/div[2]/section/div/div/div/div/div/div/div/div[1]/div[2]/div/div[1]/div[1]/div/div[1]')
    time.sleep(round(random.uniform(1, 3), 2))
    browser.execute_script('arguments[0].scrollIntoView();', video)
    try:
        start.click()
    except BaseException as e:
        pass

    # 看视频随机65-75秒
    totalTime = random.randint(65, 75)
    print('--> 正在观看：《' + videos[randIndex]['title'] + '》')
    with Progress() as progress:
        task = progress.add_task("--> [red]观看进度：", total=totalTime)
        while not progress.finished:
            sleepTime = round(random.uniform(1, 3), 2)
            progress.update(task, advance=sleepTime)
            time.sleep(sleepTime)

    print()

    del videos[randIndex]
    with open(videoPath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(videos, ensure_ascii=False, indent=4))




def scan_article(browser):
    articlePath = 'data/articles.json'
    with open(articlePath, 'r', encoding='utf-8') as f:
        articles = f.read()
    # print(articles)
    articles = json.loads(articles)
    while True:
        randIndex = random.randint(0, len(articles) - 1)
        if articles[randIndex]['type'] != 'tuwen':
            del articles[randIndex]
            continue
        else:
            break
    url = articles[randIndex]['url']
    browser.get('https://www.xuexi.cn/d184e7597cc0da16f5d9f182907f1200/9a3668c13f6e303932b5e0e100fc248b.html')
    time.sleep(round(random.uniform(1, 3), 2))
    browser.get(url)
    time.sleep(round(random.uniform(1, 5), 2))

    # 看文章随机65-75秒
    totalTime = random.randint(65, 75)
    print('--> 正在浏览：《' + articles[randIndex]['title'] + '》')
    with Progress() as progress:
        task = progress.add_task("--> [cyan]浏览进度：", total=totalTime)
        while not progress.finished:
            browser.execute_script(
                'window.scrollBy(' + str(random.randint(2, 9)) + ',' + str(random.randint(15, 31)) + ')')
            sleepTime = round(random.uniform(1, 5), 2)
            progress.update(task, advance=sleepTime)
            time.sleep(sleepTime)

    print()
    del articles[randIndex]
    with open(articlePath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(articles, ensure_ascii=False, indent=4))



def check_exam(browser, examType):
    """
    检查可做的题目，如果本页没有则翻页查找
    :param browser: browser
    :param examType: 题目类型(周、专)
    :return: null
    """
    time.sleep(round(random.uniform(1, 2), 2))
    while True:
        flag = True  # 用来记录是否答题，答题则置为False
        allExams = browser.find_elements_by_class_name('ant-btn-primary')
        for exam in allExams:
            if exam.text == '开始答题' or exam.text == '继续答题':
                browser.execute_script('arguments[0].scrollIntoView();', exam)
                time.sleep(round(random.uniform(1, 2), 2))
                exam.click()
                time.sleep(round(random.uniform(2, 4), 2))
                run_exam(browser)
                flag = False
                break
        if flag:  # flag为True则执行翻页
            nextPage = browser.find_element_by_class_name('ant-pagination-next')
            browser.execute_script('arguments[0].scrollIntoView();', nextPage)
            time.sleep(round(random.uniform(1, 2), 2))
            if nextPage.get_attribute('aria-disabled') == 'true':  # 检查翻页按钮是否可点击
                exam_type = None
                if examType == CheckResType.WEEKLY_EXAM:
                    exam_type = 'WEEKLY_EXAM'
                    print('--> 每周答题：已无可做题目')
                elif examType == CheckResType.SPECIAL_EXAM:
                    exam_type = 'SPECIAL_EXAM'
                    print('--> 专项答题：已无可做题目')
                # 如果该类型的题目已全部做完，则记录防止再次刷
                exam_temp_Path = './data/exam_temp.json'
                with open(exam_temp_Path, 'r', encoding='utf-8') as f:
                    dataDict = json.loads(f.read())
                    dataDict[exam_type] = 'false'
                with open(exam_temp_Path, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(dataDict, ensure_ascii=False, indent=4))
                return
            nextPage.click()
            time.sleep(round(random.uniform(3, 5), 2))
        else:
            break


def to_exam(browser, examType):
    """
    根据参数题目类型进入对应的题目
    :param browser: browser
    :param examType: 题目类型(日、周、专)
    :return:
    """
    browser.get('https://www.xuexi.cn/')
    time.sleep(round(random.uniform(1, 2), 2))
    browser.get('https://pc.xuexi.cn/points/my-points.html')
    time.sleep(round(random.uniform(1, 2), 2))

    if examType == CheckResType.DAILY_EXAM:
        daily = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[2]/div')
        browser.execute_script('arguments[0].scrollIntoView();', daily)
        time.sleep(round(random.uniform(1, 2), 2))
        daily.click()
        time.sleep(round(random.uniform(2, 4), 2))
        run_exam(browser)
    elif examType == CheckResType.WEEKLY_EXAM:
        weekly = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[2]/div')
        browser.execute_script('arguments[0].scrollIntoView();', weekly)
        time.sleep(round(random.uniform(1, 2), 2))
        weekly.click()
        check_exam(browser, examType)
    elif examType == CheckResType.SPECIAL_EXAM:
        special = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[7]/div[2]/div[2]/div')
        browser.execute_script('arguments[0].scrollIntoView();', special)
        time.sleep(round(random.uniform(1, 2), 2))
        special.click()
        check_exam(browser, examType)


def select_all(options):
    print('-->    最大概率选项：', end='')
    for i in range(len(options)):
        print(' ' + options[i].text[0], end='')
    print()
    for i in range(len(options)):
        time.sleep(round(random.uniform(0.5, 1.5), 2))
        options[i].click()


def run_exam(browser):
    while True:
        content = browser.find_element_by_class_name('ant-breadcrumb')
        browser.execute_script('arguments[0].scrollIntoView();', content)
        time.sleep(round(random.uniform(2, 3), 2))
        # 题目类型
        questionType = browser.find_element_by_class_name('q-header').text
        # print(questionType)
        # 当前题目的坐标
        questionIndex = int(browser.find_element_by_class_name('big').text)
        # 题目总数
        questionCount = int(re.findall('/(.*)', browser.find_element_by_class_name('pager').text)[0])
        # 确定按钮
        okBtn = browser.find_element_by_class_name('ant-btn-primary')
        try:
            browser.find_element_by_class_name('answer')
            if okBtn.text == '下一题':
                okBtn.click()
                time.sleep(round(random.uniform(2, 3), 2))
                continue
        except selenium.common.exceptions.NoSuchElementException:
            pass
        # 提示按钮
        tipBtn = browser.find_element_by_class_name('tips')
        print('--> 当前题目进度：' + str(questionIndex) + '/' + str(questionCount))
        tipBtn.click()
        time.sleep(round(random.uniform(0.5, 1.5), 2))
        try:
            # 获取所有提示内容
            tipsContent = browser.find_element_by_class_name('line-feed').find_elements_by_tag_name('font')
            time.sleep(round(random.uniform(0.5, 1.5), 2))
            tipBtn.click()
            tips = []
            tips.clear()
            for tip in tipsContent:
                tips.append(tip.text)

            if '单选题' in questionType:
                # 选择题，获取所有选项
                options = browser.find_elements_by_class_name('choosable')
                if len(tips) == 0:
                    time.sleep(round(random.uniform(0.5, 1.5), 2))
                    options[0].click()
                else:
                    ansDict = {}  # 存放每个选项与提示的相似度
                    for i in range(len(options)):
                        ansDict[i] = difflib.SequenceMatcher(None, tips[0], options[i].text[3:]).ratio()
                    ansDict = sorted(ansDict.items(), key=lambda x: x[1], reverse=True)
                    # print(ansDict)
                    print('-->    最大概率选项： ' + options[ansDict[0][0]].text[0])
                    options[ansDict[0][0]].click()

                time.sleep(round(random.uniform(0.5, 2), 2))
                okBtn.click()

            elif '多选题' in questionType:
                # 选择题，获取所有选项
                options = browser.find_elements_by_class_name('choosable')
                qWord = browser.find_element_by_class_name('q-body').text
                bracketCount = len(re.findall('（）', qWord))
                if len(options) == bracketCount:
                    select_all(options)
                else:
                    if len(tips) == 0:
                        time.sleep(round(random.uniform(0.5, 1.5), 2))
                        options[0].click()
                        time.sleep(round(random.uniform(0.5, 1.5), 2))
                        options[1].click()
                    else:
                        # 如果选项数量多于提示数量，则匹配出最可能的选项
                        if len(options) > len(tips):
                            ans = []  # 存放匹配出的最终结果
                            for i in range(len(tips)):
                                ansDict = {}  # 存放每个选项与提示的相似度
                                for j in range(len(options)):
                                    ansDict[j] = difflib.SequenceMatcher(None, tips[i], options[j].text[3:]).ratio()
                                # print(ansDict)
                                ansDict = sorted(ansDict.items(), key=lambda x: x[1], reverse=True)
                                ans.append(ansDict[0][0])
                            ans = list(set(ans))
                            # print(ans)
                            print('-->    最大概率选项：', end='')
                            for i in range(len(ans)):
                                print(' ' + options[ans[i]].text[0], end='')
                            print()
                            for i in range(len(ans)):
                                time.sleep(round(random.uniform(0.5, 1.5), 2))
                                options[ans[i]].click()
                        # 如果选项数量和提示数量相同或少于提示数量，则全选
                        else:
                            select_all(options)

                time.sleep(round(random.uniform(0.5, 2), 2))
                okBtn.click()

            elif '填空题' in questionType:
                # 填空题，获取所有输入框
                blanks = browser.find_elements_by_class_name('blank')
                tips_i = 0
                for i in range(len(blanks)):
                    time.sleep(round(random.uniform(0.5, 1.5), 2))
                    if len(tips) > tips_i and tips[tips_i].strip() == '':
                        tips_i += 1
                    try:
                        blank_ans = tips[tips_i]
                    except:
                        blank_ans = '未找到提示'
                    print('-->    第{0}空答案可能是： {1}'.format(i + 1, blank_ans))
                    blanks[i].send_keys(blank_ans)
                    tips_i += 1

                time.sleep(round(random.uniform(0.5, 2), 2))
                okBtn.click()
            # print()

        except WebDriverException as e:
            print(e)
            print('--> 答题异常，正在重试')
            otherPlace = browser.find_element_by_id('app')
            otherPlace.click()
            time.sleep(round(random.uniform(0.5, 2), 2))

        if questionIndex == questionCount:
            try:
                submit = browser.find_element_by_class_name('submit-btn')
                submit.click()
                time.sleep(round(random.uniform(1.6, 3.6), 2))
            except selenium.common.exceptions.NoSuchElementException:
                pass
            print('--> 答题结束')
            break




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
#

def get_video():
    if not is_get_data('videos'):
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
    set_time('videos')
    print('--> 视频数据更新成功')

#
# if __name__ == '__main__':
#     get_video()
#

def get_article():
    if not is_get_data('articles'):
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
    set_time('articles')
    print('--> 文章数据更新成功')

#
# if __name__ == '__main__':
#     get_article()
#



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
    if not is_get_data('videos'):
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
    set_time('videos')
    print('--> 视频数据更新成功')

#
# if __name__ == '__main__':
#     get_video()
#

def get_article():
    if not is_get_data('articles'):
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
    set_time('articles')
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
    while not login(browser):
        print('--> 登录超时，正在尝试重新登录')
        continue


def run():
    """
    刷视频，刷题目主要部分
    通过check_task()函数决定应该执行什么任务，并调用相应任务函数
    :return: null
    """
    while True:
        checkRes = check_task(browser)
        if checkRes == CheckResType.NULL:
            break
        elif checkRes == CheckResType.ARTICLE:
            scan_article(browser)
        elif checkRes == CheckResType.VIDEO:
            watch_video(browser)
        elif checkRes == CheckResType.ARTICLE_AND_VIDEO:
            if article_or_video() == 1:
                scan_article(browser)
            else:
                watch_video(browser)
        else:
            to_exam(browser, checkRes)


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
        get_video()
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
