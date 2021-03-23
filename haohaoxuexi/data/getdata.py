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
#

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

#
# if __name__ == '__main__':
#     get_article()
#
