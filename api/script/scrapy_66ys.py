# coding=utf-8
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import sys
import re
import random
import time
import logging
import hashlib
#mongo

mongoconn = MongoClient()
movie_collection = mongoconn.movie.movie

# create logger
logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)
 
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
 
# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
 
# add formatter to ch
ch.setFormatter(formatter)
 
# add ch to logger
logger.addHandler(ch)

logger.info('开始....')
start_time = time.time()

url = 'http://www.66ys.tv/'
r_index = requests.get(url)
index_text = r_index.content.decode('gb2312')
index_soup = BeautifulSoup(index_text,'html5lib')
menu_tags = index_soup.select('.menutv li a')

tag_homepages = [] #主页数组
del menu_tags[0]
for key,menu in enumerate(menu_tags):
    tag_homepages.append((menu['href'],menu.string))


nums = 0
for tag_homepage in tag_homepages:
    
    page = tag_homepage[0]
    r_page = requests.get(page)
    page_text = r_page.content
    page_soup = BeautifulSoup(page_text,'html5lib')
    #分类总条数
    total_page_tag = page_soup.select_one('a[title="Total record"] b')
    category_page_tag = page_soup.select('.pagebox a').pop()
    #分类总页数
    total_page =  re.search('index_(\d+)',category_page_tag['href']).group(1)
    for i in range(1,int(total_page)+1):
        if i == 1:
            url = page+'index.html'
        else:
            url = page+'index_%s.html' %(i)
        logger.info('读取:'+str(url))
        try:
            r_movie_page = requests.get(url,timeout=1)
        except:
            logger.info('读取:'+str(url)+'超时')
            continue
        movie_page_soup = BeautifulSoup(r_movie_page.content,'html5lib')
        movie_tags = movie_page_soup.select('.listInfo a')
        for movie_tag in movie_tags:
            #爬进 电影主页 抓取 下载地址
            movie = {} #文档字典
            movie['scrapy_site'] = url
            movie['tag'] = [tag_homepage[1]]
            
            movie_title =  movie_tag.string
            movie['title'] = movie_title
            md5obj = hashlib.md5()
            md5obj.update(movie_title.encode('utf-8').strip())
            movie_hash = md5obj.hexdigest()
            if movie_collection.find_one({'hash':movie_hash}):
                logger.info('跳过一个重复记录')
                continue
            movie['hash'] = movie_hash
            movie_home_url = movie_tag['href']
            movie['scrapy_url'] = movie_home_url
            try:
                r_movie_home_page = requests.get(movie_home_url,timeout=1)
            except:
                logger.info('抓取%s超时'%movie_home_url.encode('utf-8'))
                continue
            movie_home_soup = BeautifulSoup(r_movie_home_page.content,'html5lib')
            movie_download_table_tag = movie_home_soup.select_one('table')
            movie_download_url = []
            try:
                movie_download_table_tag.select('tr a')
            except:
                logger.info('%s遇到错误'%movie_home_url.encode('utf-8'))
                continue
            for a in  movie_download_table_tag.select('tr a'):
                if re.search('pan.baidu.com',a['href']):
                    a_parent = a.find_parent('tr')
                    movie_download_url.append(a_parent.text.encode('utf-8').strip())
                else:
                    movie_download_url.append(a['href'])
            movie['download_url'] = movie_download_url
            
            logger.info('插入一个新记录')
            movie_collection.insert_one(movie)
            nums = nums+1
                
end_time = time.time()

logger.info('耗时%s,抓取%s条记录' %(end_time-start_time,nums))

    
