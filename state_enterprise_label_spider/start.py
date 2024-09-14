# -*- coding:UTF-8 -*-
# @Time    : 24.9.2 09:18
# @Author  : yangxin
# @Email   : yang1819351140@163.com
# @IDE     : PyCharm
# @File    : start.py.py
# @Project : state_enterprise_label_spider
# @Software: PyCharm
from scrapy.cmdline import execute


def run_spider():
    execute('scrapy crawl kuaicha'.split())


if __name__ == '__main__':
    run_spider()
