# coding=utf-8
import threading
import time
import random
import sys
import logging

try:
    args = sys.argv
    thread_nums = args[2]
except:
    thread_nums = 4
# create logger with 'spam_application'
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def test(name, nums):
    logger.info('进入线程%s' % name)
    logger.info('睡眠中。。。')
    while nums > 0:
        time.sleep(1)
        logger.info('线程%s倒计时%s' % (name, nums))
        nums -= 1
    logger.info('结束线程%s' % name)


while thread_nums > 0:
    sleep_nums = random.randint(1, 8)
    t = threading.Thread(target=test, args=(thread_nums, sleep_nums))
    t.start()
    thread_nums -= 1
