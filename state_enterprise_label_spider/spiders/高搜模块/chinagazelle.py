import scrapy
import time
import json
from loguru import logger
from scrapy import Request
from state_enterprise_label_spider.items import ListUnicornItem


class ChinaGazelleSpider(scrapy.Spider):
    name = 'chinagazelle'
    # allowed_domains = ['chinagazelle.cn']
    # start_urls = ['http://chinagazelle.cn']

    def __init__(self):
        self.url = 'https://wh.chinagazelle.cn/city/org/list/{}/1000'
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }

        self.cookies = {
            'city_visited': 'wh',
            '_rm_20160825': 'JqVakRD5r0HrO4bYlNg1gQu/z6RuzjBGQFKE2XiXYuHh+kP4qUzz7wBynd9q3DCJX09Gmpj8BnQAsb78HmG3CIrGIznbLMaaxgx0OeUw5LYdkWEsvK1evKD2XpOU5PB/UD8ZsX5BiuoOYt4pOV2hR2AgeF7Hdng/XlpK7HWKK9XS/N0F1FDmEDqzlE3rKXUjT3a4HRLu9tgR6/V1fGGzZsISl65mHiSFEnDeJqMHsP/qH4LQer8gPBhvXJ8ZU6GJe6Zju3hW+ZwnQ707IPuBjFcaUFRQtRaBpjMcnYGvIzCBryIbDdtg8ZwosCUMKCPu79mREcisPZQv/576Yi6hJz6GX112vwFEzOvCZJz7bX484qWfDKD1fjdEg3F9tqPC1HZCjbgM9xe86IqvaGts9J/tBONEDRhY3LbDWZkmlUB2SzHsG5KD94OpH6Erxe/AHu6rvxunbJOd1ttxHikUT6o9LYo9gr2OWbBw4aXGntJY3ZfQ7NbSq8mwmBVHXWPf1kqNEYK7nd3OKO0x60DR3QP31H7cHmssr3Xf6rwsPIq73RAS2y568Cdl1o49sCRxwMJUfWCp2zF9fbCRMsac30MvpMFO+xDws2tiBE925aY=',
            '_portal_sid': '87727493-afa7-4a56-b6db-475fc795ab9d'
        }

    def start_requests(self):
        page = 1
        yield Request(self.url.format(page), headers=self.headers, cookies=self.cookies, meta={'page': page}, callback=self.parse)

    def parse(self, response):
        try:
            data_list = json.loads(response.text).get('list', [])
            if data_list:
                for data in data_list:
                    id = data.get('id', '')
                    full_name = data.get('fullname', '')
                    image_url = data.get('imageUrl', '')
                    country = data.get('country', '')
                    province = data.get('province', '')
                    city = data.get('city', '')
                    county = data.get('county', '')
                    is_listed = data.get('isListed', '')
                    is_technology_organization = data.get('isTechnologyOrganization', '')
                    set_up_time = data.get('setUpTime', '')
                    last_cognizance = data.get('lastCognizance', '')
                    cognizances = data.get('cognizances', '')
                    high_tech_zone = data.get('highTechZone', '')
                    level = data.get('level', '')
                    area_path = data.get('areaPath', '')
                    field_path = data.get('fieldPath', '')
                    field = data.get('field', '')
                    industry_path = data.get('industryPath', '')
                    industry = data.get('industry', '')
                    cognizance_year = data.get('cognizanceYear', '')
                    cognizance_type = data.get('cognizanceType', '')
                    origin_cognizance_type = data.get('originCognizanceType', '')
                    register_status = data.get('registerStatus', '')
                    identified_time = data.get('identifiedTime', '')
                    historys = data.get('historys', '')
                    longitude = data.get('longitude', '')
                    latitude = data.get('latitude', '')

                    if full_name:
                        item = ListUnicornItem()
                        item['id'] = id
                        item['full_name'] = full_name
                        item['image_url'] = image_url
                        item['country'] = country
                        item['province'] = province
                        item['city'] = city
                        item['county'] = county
                        item['is_listed'] = is_listed
                        item['is_technology_organization'] = is_technology_organization
                        item['set_up_time'] = set_up_time
                        item['last_cognizance'] = last_cognizance
                        item['cognizances'] = cognizances
                        item['high_tech_zone'] = high_tech_zone
                        item['level'] = level
                        item['area_path'] = area_path
                        item['field_path'] = field_path
                        item['field'] = field
                        item['industry_path'] = industry_path
                        item['industry'] = industry
                        item['cognizance_year'] = cognizance_year
                        item['cognizance_type'] = cognizance_type
                        item['origin_cognizance_type'] = origin_cognizance_type
                        item['register_status'] = register_status
                        item['identified_time'] = identified_time
                        item['historys'] = historys
                        item['longitude'] = longitude
                        item['latitude'] = latitude
                        item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
                        item['update_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
                        # print(dict(item))
                        yield item

                page = response.meta['page'] + 1
                yield Request(self.url.format(page), headers=self.headers, cookies=self.cookies, meta={'page': page}, callback=self.parse)
        except Exception as e:
            logger.error(f'【高搜模块】瞪羚云平台：数据解析失败！失败原因：\n{e}')
