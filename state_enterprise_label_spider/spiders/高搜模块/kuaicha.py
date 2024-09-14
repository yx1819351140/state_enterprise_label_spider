import scrapy
import time
from loguru import logger
from scrapy import Request
import json
from state_enterprise_label_spider.items import HiddenChampionItem


class KuaichaSpider(scrapy.Spider):
    name = 'kuaicha'
    # allowed_domains = ['guoqi.org']
    # start_urls = ['http://guoqi.org/']

    def __init__(self):
        self.url = 'https://yuqing.kuaicha365.com/enterprise_info_app/V1/search/company_search_app'
        self.headers = {
            'hs-dpass': 'Uxuacr0RTvht2z8yavCLzSU90gI9kB2DdYjZJgNBLxrXC4yQFZw5hglcGuUQ/jJoCQX+0lNqQhbNQsceK2KXzA==',
            'device-info': '[yq_project/7.5.0] [os-ver/10] [device-brand/HUAWEI] [device-name/EML-AL00] [screen-pix/1080 x 2159] [screen-scale/3x] [screen-dpi/480] [screen-mode/light] [location/latitude=39.910833,longitude=116.456619]',
            'net-info': '[type/WiFi] [vpn-on/false] [operator/UNKNOWN]',
            'risk': '[jail-broken/false]',
            'hs-sign': 'f6c02bef26439c4b52114d983ecbbde6|1.72617062686E9',
            'hs-device': '50D13A040D46452E989255B3D094220D',
            'version': '7.5.0',
            'source': 'APP',
            'platform': 'android',
            'User-Agent': 'okhttp/3.14.9; Android/10; HUAWEI/EML-AL00; yuqingapp/7.5.0',
            'hs-version': 'Android-7.5.0',
            'Content-Type': 'application/json; charset=utf-8',
            'Host': 'yuqing.kuaicha365.com',
            'Connection': 'Keep-Alive',
        }

        self.cookies = {
            'PHPSESSID': 'nv106r3c54f0vjbvf6aa3jf8m2lq7h7o',
            'ta_random_userid': 'a9wkh2fuh7',
            'u_ukey': 'A10702B8689642C6BE607730E11E6E4A',
            'u_uver': '1.0.0',
            'u_dpass': 'oAKbDVrRYu7ksOBDAVYlqPxRjdwqwrIUaV5FhvvZOKwH5hjafYC0AD8aC1hyrGCaHi80LrSsTFH9a%%2B6rtRvqGg%%3D%%3D',
            'u_did': 'A1271E27D64B446B9CF985DA8FD945ED',
            'u_ttype': 'WEB',
            'userid': '561657835',
            'u_name': 'mx_561657835',
            'escapename': 'mx_561657835',
            'user_status': '0',
            'jsessionid-yqapp': '3532D409DF74483EECB63388E7467198',
            'v': 'AxMmIxw8ceWKCD2xXwYxQTAYoJw9yKeKYVzrvsUwbzJpRDxGTZg32nEsewjW',
            'user': 'MDpteF81NjE2NTc4MzU6Ok5vbmU6NTAwOjU3MTY1NzgzNTo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoxNjo6OjU2MTY1NzgzNToxNzI2MTE5OTE2Ojo6MTYxMDM1OTgwMDoyNjc4NDAwOjA6MTQyMTFhZDI0NDhmZjMzMDZlMzQwN2FjMmZhNDFjYzU3OmRlZmF1bHRfNDow',
            'ticket': 'ba07490fbb6674a49f144e67cf73cd00',
            'utk': '4Ib1c43c2ee1a7cdc1c0e886692c6d6a1',
            'SESSION': '1094d34f-58ca-4e9c-b053-013df1af168c',
            'JSESSIOND': '22281AAE1EFC76D742E45E5B9EC33692',
        }
        self.code_region = {
            '110000': '北京市',
            '340000': '安徽省',
            '460000': '海南省',
            '500000': '重庆市',
            '650000': '新疆维吾尔自治区',
            '220000': '吉林省',
            '440000': '广东省',
            '150000': '内蒙古自治区',
            '520000': '贵州省',
            '610000': '陕西省',
            '640000': '宁夏回族自治区',
            '320000': '江苏省',
            '360000': '江西省',
            '370000': '山东省',
            '530000': '云南省',
            '540000': '西藏自治区',
            '820000': '澳门特别行政区',
            '130000': '河北省',
            '210000': '辽宁省',
            '310000': '上海市',
            '630000': '青海省',
            '710000': '台湾省',
            '330000': '浙江省',
            '420000': '湖北省',
            '430000': '湖南省',
            '450000': '广西壮族自治区',
            '140000': '山西省',
            '350000': '福建省',
            '510000': '四川省',
            '620000': '甘肃省',
            '120000': '天津市',
            '230000': '黑龙江省',
            '410000': '河南省',
            '810000': '香港特别行政区'
        }
        self.data = {
            "area": "",
            "city": "",
            "area_code": "",
            "big_industry": "",
            "city_code": "",
            # "province_code": "110000",
            # "province": "北京市",
            "search_conditions": [{"field": "science_and_technology_new", "options": [{"unit": "", "value": "A0010004000600060001"}]}],
            # "page": 1,
            "small_industry": "",
            "show_risk": 1,
            "page_size": 10
        }

    def start_requests(self):
        for code, region in self.code_region.items():
            page = 1
            self.data['province_code'] = code
            self.data['province'] = region
            self.data['page'] = page
            yield Request(self.url, method='POST', headers=self.headers, cookies=self.cookies,
                              body=json.dumps(self.data), meta={'page': page, 'code': code, 'region': region},
                              callback=self.parse)

    def parse(self, response):
        try:
            data_list = json.loads(response.text).get('data', {}).get('list', [])
            page = response.meta['page']
            if data_list and page <= 10:
                for data in data_list:
                    try:
                        ENTID = data.get('ent_id', '')
                        entname = data.get('name', '')
                        regcap = data.get('capital', '')
                        esdate = data.get('establish_time', '')
                        province = data.get('province', '')
                        city = data.get('city', '')
                        district = data.get('', '')
                        tel_list = data.get('phone_num', []) if data.get('phone_num', []) else []
                        tel = ','.join(tel_list)
                        email_list = data.get('email', []) if data.get('email', []) else []
                        email = ','.join(email_list)
                        creidtcode = data.get('unified_social_credit_code', '')
                        tax_code = data.get('representative_id', '')
                        regis_code = data.get('register_num', '')
                        org_code = data.get('org_id', '')
                        emp = data.get('emp', '')
                        entstype = data.get('state', '')
                        industry = data.get('small_industry', '')
                        dom = data.get('address', '')
                        OPSCOPE = data.get('scope', '')
                        create_time = time.strftime('%Y-%m-%d %H:%M:%S')
                        update_time = time.strftime('%Y-%m-%d %H:%M:%S')

                        if entname:
                            item = HiddenChampionItem()
                            item['ENTID'] = ENTID
                            item['entname'] = entname
                            item['regcap'] = regcap
                            item['esdate'] = esdate
                            item['province'] = province
                            item['city'] = city
                            item['district'] = district
                            item['tel'] = tel
                            item['email'] = email
                            item['creidtcode'] = creidtcode
                            item['tax_code'] = tax_code
                            item['regis_code'] = regis_code
                            item['org_code'] = org_code
                            item['emp'] = emp
                            item['entstype'] = entstype
                            item['industry'] = industry
                            item['dom'] = dom
                            item['OPSCOPE'] = OPSCOPE
                            item['create_time'] = create_time
                            item['update_time'] = update_time
                            # print(dict(item))
                            yield item
                    except Exception as e:
                        logger.error(f'【高搜模块】快查：数据详情解析失败！失败原因：\n{e}')
                        continue

                page += 1
                code = response.meta['code']
                region = response.meta['region']
                self.data['province_code'] = code
                self.data['province'] = region
                self.data['page'] = page
                yield Request(self.url, method='POST', headers=self.headers, cookies=self.cookies,
                              body=json.dumps(self.data), meta={'page': page, 'code': code, 'region': region},
                              callback=self.parse)
        except Exception as e:
            logger.error(f'【高搜模块】快查：列表页解析失败！失败原因：\n{e}')
