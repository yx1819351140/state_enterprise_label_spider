import scrapy
import time
from loguru import logger
import json
from scrapy import FormRequest
from state_enterprise_label_spider.items import CfdiItem


class CfdiSpider(scrapy.Spider):
    name = 'cfdi'
    allowed_domains = ['cfdi.org.cn']
    start_urls = ['http://cfdi.org.cn/']

    def __init__(self):
        self.url = 'https://beian.cfdi.org.cn/CTMDS/pub/PUB010100.do?method=handle06'
        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            # 'cookie': 'JSESSIONID=97893C81A5F202313FD0B298D96079C8; MM_1xL8nvQydGCE0=',
            'origin': 'https://beian.cfdi.org.cn',
            'priority': 'u=1, i',
            'referer': 'https://beian.cfdi.org.cn/CTMDS/apps/pub/drugPublic1.jsp',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

    def start_requests(self):
        yield FormRequest(url=self.url, headers=self.headers, dont_filter=True,
                               formdata={'pageSize': '2000',
                                        'curPage': '1',
                                        'sortName': '',
                                        'sortOrder': '',}
                               )

    def parse(self, response):
        try:
            yield from (
                CfdiItem({
                    'address': i.get('address'),
                    'areaName': i.get('areaName'),
                    'compName': i.get('compName'),
                    'companyId': i.get('companyId'),
                    'linkMan': i.get('linkMan'),
                    'linkTel': i.get('linkTel'),
                    'recordNo': i.get('recordNo'),
                    'status': i.get('recordStatus'),
                })
                for i in json.loads(response.text)['data']
            )
        except Exception as e:
            logger.error(f'【高搜模块】药物临床试验机构备案管理信息平台：列表页解析失败！失败原因：\n{e}')
