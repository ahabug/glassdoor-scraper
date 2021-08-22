import csv
import json
import logging.config
import os
import threading
import time
from queue import Queue

import pandas as pd
import requests
import ugents

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

logger.addHandler(ch)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d :%(filename)s(%(process)d) - %(message)s')
ch.setFormatter(formatter)
logging.getLogger('selenium').setLevel(logging.CRITICAL)


def get_header(url):
    headers = {'User-Agent': ugents.getAgent(),
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
               'cache-control': 'max-age=0', 'dnt': '1', 'referer': 'https://www.glassdoor.com.hk/',
               'sec-ch-ua-mobile': '?0', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
               'sec-fetch-user': '?1', 'sec-fetch-site': 'none', 'upgrade-insecure-requests': '1'}
    return headers


def get_cookie(manual_cookies):
    with open("manual_cookies.txt", 'r', encoding='utf-8') as frcookie:
        cookies_txt = frcookie.read().strip(';')  # 读取文本内容
        # 手动分割添加cookie
        for item in cookies_txt.split(';'):
            name, value = item.strip().split('=', 1)  # 用=号分割，分割1次
            manual_cookies[name] = value  # 为字典cookies添加内容
    # 将字典转为CookieJar：
    cookies_jar = requests.utils.cookiejar_from_dict(manual_cookies, cookiejar=None, overwrite=True)
    return cookies_jar


def save2csv(data_list):
    out_file = 'score_info.csv'
    df = pd.DataFrame(data_list)
    is_writeheader = not os.path.exists(out_file)
    with open(out_file, 'a', encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=df.columns)
        if is_writeheader:
            writer.writeheader()
            logger.info('写入表头')
        for data in data_list:
            writer.writerow(data)
            logger.info(data)


class Spider(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        while True:
            if DB_queue.empty():
                break
            data = DB_queue.get()
            logger.info(data)
            self.get_list(data)
            left = DB_queue.qsize()
            if left % 50 == 0:
                logger.info(f"This are {left} courts left.")

    def get_list(self, data):
        id = data
        res = {}
        res['id'] = id
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'trend' + '&category=' + 'overallRating'
        logger.info(url)
        response = self.get_response(url)
        response = json.loads(response)
        res["overallRatingtrenddates"] = response['dates']
        res["overallRatingtrendratings"] = response['employerRatings']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'distribution' + '&category=' + 'overallRating'
        response = self.get_response(url)
        response = json.loads(response)
        res["overallRatingdistributionlabels"] = response['labels']
        res["overallRatingdistributionvalues"] = response['values']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'trend' + '&category=' + 'cultureAndValues'
        response = self.get_response(url)
        response = json.loads(response)
        res['cultureAndValuestrenddates'] = response['dates']
        res['cultureAndValuestrendratings'] = response['employerRatings']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'distribution' + '&category=' + 'cultureAndValues'
        response = self.get_response(url)
        response = json.loads(response)
        res['cultureAndValuesdistributionlabels'] = response['labels']
        res['cultureAndValuesdistributionvalues'] = response['values']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'trend' + '&category=' + 'diversityAndInclusion'
        response = self.get_response(url)
        response = json.loads(response)
        res['diversityAndInclusiontrenddates'] = response['dates']
        res['diversityAndInclusiontrendratings'] = response['employerRatings']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'distribution' + '&category=' + 'diversityAndInclusion'
        response = self.get_response(url)
        response = json.loads(response)
        res["diversityAndInclusiondistributionlabels"] = response['labels']
        res["diversityAndInclusiondistributionvalues"] = response['values']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'trend' + '&category=' + 'workLife'
        response = self.get_response(url)
        response = json.loads(response)
        res["workLifetrenddates"] = response['dates']
        res["workLifetrendratings"] = response['employerRatings']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'distribution' + '&category=' + 'workLife'
        response = self.get_response(url)
        response = json.loads(response)
        res["workLifedistributionlabels"] = response['labels']
        res["workLifedistributionvalues"] = response['values']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'trend' + '&category=' + 'seniorManagement'
        response = self.get_response(url)
        response = json.loads(response)
        res["seniorManagementtrenddates"] = response['dates']
        res["seniorManagementtrendratings"] = response['employerRatings']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'distribution' + '&category=' + 'seniorManagement'
        response = self.get_response(url)
        response = json.loads(response)
        res["seniorManagementdistributionlabels"] = response['labels']
        res["seniorManagementdistributionvalues"] = response['values']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'trend' + '&category=' + 'compAndBenefits'
        response = self.get_response(url)
        response = json.loads(response)
        res["compAndBenefitstrenddates"] = response['dates']
        res["compAndBenefitstrendratings"] = response['employerRatings']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'distribution' + '&category=' + 'compAndBenefits'
        response = self.get_response(url)
        response = json.loads(response)
        res["compAndBenefitsdistributionlabels"] = response['labels']
        res["compAndBenefitsdistributionvalues"] = response['values']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'trend' + '&category=' + 'careerOpportunities'
        response = self.get_response(url)
        response = json.loads(response)
        res["careerOpportunitiestrenddates"] = response['dates']
        res["careerOpportunitiestrendratings"] = response['employerRatings']
        time.sleep(1)
        url = 'https://www.glassdoor.com.hk/api/employer/' + id + '-rating.htm?dataType=' + 'distribution' + '&category=' + 'careerOpportunities'
        response = self.get_response(url)
        response = json.loads(response)
        res["careerOpportunitiesdistributionlabels"] = response['labels']
        res["careerOpportunitiesdistributionvalues"] = response['values']
        time.sleep(1)
        save2csv([res])

    def get_response(self, url):
        s = requests.session()
        s.keep_alive = False
        response = s.get(url, headers=get_header(url))
        return response.text


def timeit(f):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = f(*args, **kwargs)
        end_time = time.time()
        logger.info("%s函数运行时间为：%.2f" % (f.__name__, end_time - start_time))
        return res

    return wrapper


@timeit
def main():
    CSV_FILE_PATH = './company_list.csv'
    df = pd.read_csv(CSV_FILE_PATH)  # 序号到手
    with open('company_list.txt', 'r', encoding='utf-8') as f:
        id_list = set(f.readlines())
        for id in id_list:
            DB_queue.put(id.replace('\n', ''))  # 没搞过的撂进去
    thread_list = []
    # 同时开几个，取决于代理质量和电脑性能，这个程序总耗时大约几个小时，比较短，所以可以不用太在意效率
    for _ in range(1):
        crawl = Spider("Spider_crawl_{}".format(_))
        crawl.start()
        thread_list.append(crawl)
    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    DB_queue = Queue()
    main()
