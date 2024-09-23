import scrapy
import time
from loguru import logger
import json
from state_enterprise_label_spider.items import ECqsItem


def timestamp(time_stamp):
    try:
        time_stamp = int(time_stamp * (10 ** (10 - len(str(time_stamp)))))
        time_array = time.localtime(time_stamp)
        str_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        return str_date
    except ValueError:
        print(time_stamp)
        return time_stamp


class GuoqiSpider(scrapy.Spider):
    name = 'e-cqs'
    # allowed_domains = ['e-cqs.cn']
    # start_urls = ['http://psp.e-cqs.cn/']

    def __init__(self):
        self.url = 'http://psp.e-cqs.cn/aeaPP/jsonClient.action?encoding=true&jsonValue=%7B%22serviceClassName%22%3A%22com.itown.pp.query.publicQuery.CertificateOfHistoryService%22%2C%22methodName%22%3A%22getTCertInfoEntityList%22%2C%22serviceObject%22%3Anull%2C%22type%22%3Anull%2C%22params%22%3A%5B%22%22%5D%7D'

    def start_requests(self):
        yield from (
            scrapy.FormRequest(url=self.url, dont_filter=True,
                               formdata={'name': 'easyui',
                                         'subject': 'datagrid',
                                         'page': f'{page}',
                                         'rows': '10'}
                               )
            for page in range(1, 1585)
        )

    def parse(self, response):
        try:
            yield from (
                ECqsItem({
                    'creditname': i.get('creditName'),  # 公司名称
                    'prodname': i.get('prodName'),  # 主导产品
                    'licenceno': i.get('licenceNo'),  # 证书编号
                    'licmatter': i.get('licMatter'),  # 说明
                    'orgaddr': i.get('orgAddr'),  # 生产地址
                    'testlocus': i.get('testLocus'),  # 住所
                    'province': i.get('province'),  # 省份
                    'certdate': timestamp(int(i.get('certDate').get('value'))),  # 发证日期
                    'certvaliddate': timestamp(int(i.get('certValidDate').get('value'))),  # 有效期至
                    'model2': i.get('model2'),  # 明细
                })
                for i in json.loads(response.text)['returnValue']['value']
            )
        except Exception as e:
            logger.error(f'【高搜模块】中国电子质量监督：列表页解析失败！失败原因：\n{e}')

