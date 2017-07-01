# coding=utf-8
import hashlib
import logging
from os import path
import random
import re
import sys
import threading
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
sys.path.append(path.abspath('../'))
from common import logger


args = sys.argv
try:
    env = args[1]
except:
    env = 'default'

config = {
    'default': {'mdb_host': '127.0.0.1', 'mdb_port': 27017, 'mdb_name': 'movie'},
    'vison': {'mdb_host': '192.168.33.10', 'mdb_port': 27017, 'mdb_name': 'movie'},
}
# mongo

mongoconn = MongoClient(config[env]['mdb_host'], config[env]['mdb_port'])
movie_collection = mongoconn.movie.movie

# create logger
logger = logging.getLogger("root.file")


logger.info('开始....')
start_time = time.time()

url = 'http://www.66ys.tv/'
r_index = requests.get(url)
index_text = r_index.content.decode('gb2312')
index_soup = BeautifulSoup(index_text, 'html5lib')
menu_tags = index_soup.select('.menutv li a')

nums = 0
thread_nums = 0
global total_speed_time = 0

def start_scrapy(threadName, homepage, home_url):
    logger.info('开始线程:%s' % threadName)
    thread_start_time = time.time()
    tag_homepage = (home_url, homepage)
    page = tag_homepage[0]
    r_page = requests.get(page)
    page_text = r_page.content
    page_soup = BeautifulSoup(page_text, 'html5lib')
    # 分类总条数
    total_page_tag = page_soup.select_one('a[title="Total record"] b')
    category_page_tag = page_soup.select('.pagebox a').pop()
    # 分类总页数
    total_page = re.search('index_(\d+)', category_page_tag['href']).group(1)
    for i in range(1, int(total_page) + 1):
        if i == 1:
            url = page + 'index.html'
        else:
            url = page + 'index_%s.html' % (i)
        logger.debug('线程%s读取:%s' % (threadName, str(url)))
        try:
            r_movie_page = requests.get(url, timeout=1)
        except:
            logger.error('线程%s读取:%s超时' % (threadName, str(url)))
            continue
        movie_page_soup = BeautifulSoup(r_movie_page.content, 'html5lib')
        movie_tags = movie_page_soup.select('.listInfo a')
        for movie_tag in movie_tags:
            # 爬进 电影主页 抓取 下载地址
            movie = {}  # 文档字典
            movie['scrapy_site'] = url
            movie['tag'] = [tag_homepage[1]]

            movie_title = movie_tag.string
            movie['title'] = movie_title
            md5obj = hashlib.md5()
            md5obj.update(movie_title.encode('utf-8').strip())
            movie_hash = md5obj.hexdigest()
            if movie_collection.find_one({'hash': movie_hash}):
                logger.debug('线程%s跳过一个重复记录' % threadName)
                continue
            movie['hash'] = movie_hash
            movie_home_url = movie_tag['href']
            movie['scrapy_url'] = movie_home_url
            try:
                r_movie_home_page = requests.get(movie_home_url, timeout=1)
            except:
                logger.error('抓取%s超时' % movie_home_url.encode('utf-8'))
                continue
            movie_home_soup = BeautifulSoup(
                r_movie_home_page.content, 'html5lib')
            movie_download_table_tag = movie_home_soup.select_one('table')
            movie_download_url = []
            try:
                movie_download_table_tag.select('tr a')
            except:
                logger.error('%s遇到错误' % movie_home_url.encode('utf-8'))
                continue
            for a in movie_download_table_tag.select('tr a'):
                if re.search('pan.baidu.com', a['href']):
                    a_parent = a.find_parent('tr')
                    movie_download_url.append(
                        a_parent.text.encode('utf-8').strip())
                else:
                    movie_download_url.append(a['href'])
            movie['download_url'] = movie_download_url
            movie['create_time'] = datetime.now()

            logger.debug('线程%s插入一个新记录' % threadName)
            movie_collection.insert_one(movie)
            global nums
            nums = nums + 1
    logger.info('线程%s执行完毕' % threadName)
    thread_end_time = time.time()
    speed_time = thread_end_time - thread_start_time
    logger.info('线程%s执行时间' % speed_time)
    global thread_nums
    thread_nums -= 1
    total_speed_time +-speed_time
    


tag_homepages = []  # 主页数组
del menu_tags[0]
thread_list = []
for key, menu in enumerate(menu_tags):
    tag_homepages.append((menu['href'], menu.string))
    try:
        t = threading.Thread(target=start_scrapy, args=(
            key, menu.string, menu['href']))
        t.start()
        thread_list.append(t)
        thread_nums += 1
    except:
        print '执行线程%s失败' % menu.string.decode('utf-8')

    
# end_time = time.time()
# logger.info('耗时%s,抓取%s条记录' % (end_time - start_time, nums))

