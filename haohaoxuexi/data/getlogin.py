
import time
import random
import json
from enum import Enum
from selenium import webdriver
from rich import print
from rich.table import Column, Table
from datetime import datetime

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

    dayOfWeek = str(datetime.now().isoweekday())
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
