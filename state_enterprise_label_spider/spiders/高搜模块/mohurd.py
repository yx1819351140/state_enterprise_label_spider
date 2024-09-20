# -*- coding:UTF-8 -*-
# @Time    : 24.9.20 10:26
# @Author  : yangxin
# @Email   : yang1819351140@163.com
# @IDE     : PyCharm
# @File    : mohurd.py
# @Project : state_enterprise_label_spider
# @Software: PyCharm
from state_enterprise_label_spider.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, KAFKA_BOOTSTRAP_SERVERS
import pymysql
import time
from kafka import KafkaProducer
import json


# 连接数据库
def connect_db():
    connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB, charset="utf8", port=MYSQL_PORT)
    return connection


def process_and_insert_data(data_list, connection, kafka_producer):
    with connection.cursor() as cursor:
        for data in data_list:
            sql = """
            INSERT INTO enqa_real_estate_development (enqa_name, entname, entname_old, type, pub_unit, enqa_url) VALUES (%s, %s, %s, %s, %s, %s)
            """
            company_name = data.split('.')[-1].strip()
            enqa_name = '房地产开发一级资质'
            type = '核准晋升房地产开发一级资质企业名单'
            pub_unit = '住房和城乡建设部'
            enqa_url = 'https://www.mohurd.gov.cn/ess/?ty=a&query=%E6%88%BF%E5%9C%B0%E4%BA%A7%E5%BC%80%E5%8F%91%E4%B8%80%E7%BA%A7%E8%B5%84%E8%B4%A8&ukl=&uka=&ukf=%E6%88%BF%E5%9C%B0%E4%BA%A7%E5%BC%80%E5%8F%91%E4%B8%80%E7%BA%A7%E8%B5%84%E8%B4%A8&ukt=&sl=&ts=&te=&upg=1'
            try:
                cursor.execute(sql, (enqa_name, company_name, company_name, type, pub_unit, enqa_url))
            except Exception as e:
                print(e)
                continue
            data = {
                'enqa_name': enqa_name,
                'entname': company_name,
                'entname_old': company_name,
                'type': type,
                'pub_unit': pub_unit,
                'enqa_url': enqa_url
            }
            kafka_producer.send('collect_enqa_real_estate_development', value=data)

        connection.commit()
        kafka_producer.flush()


def process_files():
    connection = connect_db()
    kafka_producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # 将消息序列化为 JSON 格式
    )

    try:
        with open('./data/建筑资质.txt', 'r', encoding='utf-8') as f:
            data_list = f.readlines()
            process_and_insert_data(data_list, connection, kafka_producer)
    finally:
        connection.close()


# 主程序入口
if __name__ == "__main__":
    process_files()
