# -*- coding:UTF-8 -*-
# @Time    : 24.9.23 13:50
# @Author  : yangxin
# @Email   : yang1819351140@163.com
# @IDE     : PyCharm
# @File    : qszt_cscs.py
# @Project : state_enterprise_label_spider
# @Software: PyCharm
import scrapy
import time
from loguru import logger
import json
from state_enterprise_label_spider.items import QsztItem


class QsztSpider(scrapy.Spider):
    name = 'qszt'
    # allowed_domains = ['qszt.net']
    # start_urls = ['http://sc.qszt.net/']

    def __init__(self):
        self.url = 'http://sc.qszt.net/classareashow.asp?page={}&bigid=&smallid='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }
    # 2652
    def start_requests(self):
        yield from (
            scrapy.Request(url=self.url.format(page), dont_filter=True,headers=self.headers)
            for page in range(3, 2652)
        )

    def parse(self, response):
        try:
            elem_list = response.xpath('//table[@cellpadding="4"]//table')[:20]
            if elem_list:
                for elem in elem_list:
                    title = elem.xpath('./tr[1]/td[1]/a/b/text()').get().strip()
                    licenece = elem.xpath('./tr[1]/td[1]//text()').getall()[-1].replace('：', '').strip()
                    text = elem.xpath('./tr[2]/td[1]/text()').get().replace('：', '').strip()

                    item = QsztItem()
                    item['title'] = title
                    item['licenece'] = licenece
                    item['text'] = text

                    yield item
        except Exception as e:
            logger.error(f'【高搜模块】中国QS查询网：列表页解析失败！失败原因：\n{e}')
