import json
import selenium
from selenium.common.exceptions import WebDriverException
import time
import random
import difflib
import re
from userOperation import check
from selenium import webdriver
import json
import time
import random
from rich.progress import Progress
from selenium import webdriver
import json
import time
import random
from rich.progress import Progress


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
                if examType == check.CheckResType.WEEKLY_EXAM:
                    exam_type = 'WEEKLY_EXAM'
                    print('--> 每周答题：已无可做题目')
                elif examType == check.CheckResType.SPECIAL_EXAM:
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

    if examType == check.CheckResType.DAILY_EXAM:
        daily = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[2]/div')
        browser.execute_script('arguments[0].scrollIntoView();', daily)
        time.sleep(round(random.uniform(1, 2), 2))
        daily.click()
        time.sleep(round(random.uniform(2, 4), 2))
        run_exam(browser)
    elif examType == check.CheckResType.WEEKLY_EXAM:
        weekly = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[2]/div')
        browser.execute_script('arguments[0].scrollIntoView();', weekly)
        time.sleep(round(random.uniform(1, 2), 2))
        weekly.click()
        check_exam(browser, examType)
    elif examType == check.CheckResType.SPECIAL_EXAM:
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

