import scrapy
import time
from loguru import logger
from scrapy import Request
from state_enterprise_label_spider.items import BaseInfoItem


class GuoqiSpider(scrapy.Spider):
    name = 'guoqi'
    # allowed_domains = ['guoqi.org']
    # start_urls = ['http://guoqi.org/']

    def __init__(self):
        self.url = 'http://www.guoqi.org/certification/directory_class.php?id=36&page={}'

    def start_requests(self):
        page = 1
        yield Request(self.url.format(page), meta={'page': page}, callback=self.parse)

    def parse(self, response):
        try:
            temp_url_list = response.xpath('//div[@align="center"]/div[@align="left"]/div/a/@href').getall()
            if len(temp_url_list) > 1:
                for temp_url in temp_url_list:
                    if 'jump' in temp_url:
                        detail_url = 'http://www.guoqi.org/certification/' + temp_url
                        yield Request(detail_url, callback=self.parse_detail)

                page = response.meta['page'] + 1
                yield Request(self.url.format(page), meta={'page': page}, callback=self.parse)
        except Exception as e:
            logger.error(f'【国企标签】国资认证中心网：列表页解析失败！失败原因：\n{e}')

    def parse_detail(self, response):
        try:
            data_list = response.xpath('//div[@class="slideshow2"]//div[@align="center"]/div/div/div[@align="center"]/div/text()').getall()
            name = ''
            code = ''
            for data in data_list:
                if '国家出资企业' in data:
                    name = data.replace('国家出资企业：', '')
                elif '标识码' in data:
                    code = data.replace('标识码：', '')
                    break
            attrib = response.xpath('//div[@class="slideshow2"]//div[@align="center"]/div/div/div[@align="center"]/div/div/span[1]/text()').get()
            attrib_level = response.xpath('//div[@class="slideshow2"]//div[@align="center"]/div/div/div[@align="center"]/div/div/span[2]/text()').get()
            url = response.xpath('//div[@class="slideshow2"]//div[@align="center"]/div/div/div[@align="center"]/div/a/@href').get()

            if name:
                item = BaseInfoItem()
                item['name'] = name
                item['code'] = code
                item['attrib'] = attrib
                item['attrib_level'] = attrib_level
                item['url'] = url
                item['from_url'] = response.url
                item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
                item['update_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
                # print(dict(item))
                yield item
        except Exception as e:
            logger.error(f'【国企标签】国资认证中心网：详情页解析失败！失败原因：\n{e}')
