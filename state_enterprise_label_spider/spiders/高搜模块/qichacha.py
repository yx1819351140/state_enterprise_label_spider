# -*- coding:UTF-8 -*-
# @Time    : 24.9.5 13:52
# @Author  : yangxin
# @Email   : yang1819351140@163.com
# @IDE     : PyCharm
# @File    : qichacha.py
# @Project : state_enterprise_label_spider
# @Software: PyCharm
import os
import pandas as pd
from state_enterprise_label_spider.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, KAFKA_BOOTSTRAP_SERVERS
import pymysql
import time
from kafka import KafkaProducer
import json


# 连接数据库
def connect_db():
    connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB, charset="utf8", port=MYSQL_PORT)
    return connection


# 处理并插入数据的函数
def process_and_insert_data(file_path, connection, kafka_producer):
    # 读取 Excel 文件，跳过第一行的声明
    df = pd.read_excel(file_path, skiprows=1)

    # 将DataFrame中的列重命名为数据库字段
    df.columns = [
        'company_name', 'company_status', 'legal_entity_name', 'reg_capital_amt',
        'es_dt', 'usc_no', 'register_addr', 'province', 'city',
        'region', 'phones', 'more_phones', 'email', 'register_type',
        'tax_code', 'regis_code', 'org_code', 'insurance_amount', 'insurance_year',
        'operation_date', 'nic_name', 'nic_1', 'nic_2', 'nic_3', 'qcc_name', 'qcc_nic_1',
        'qcc_nic_2', 'qcc_nic_3', 'company_scale', 'history_name', 'english_name', 'data_source',
        'address', 'company_intro', 'business_scope'
    ]

    # 将DataFrame的空值替换为 None
    df = df.where(pd.notnull(df), None)

    # 插入数据到数据库
    with connection.cursor() as cursor:
        for index, row in df.iterrows():
            sql = """
            INSERT INTO qcc_list_technology_enterprise (
                company_name, company_status, legal_entity_name, reg_capital_amt, 
                es_dt, usc_no, register_addr, province, city, 
                region, phones, more_phones, email, register_type, 
                tax_code, regis_code, org_code, insurance_amount, insurance_year, 
                operation_date, nic_name, nic_1, nic_2, nic_3, qcc_name, qcc_nic_1, 
                qcc_nic_2, qcc_nic_3, company_scale, history_name, english_name, data_source, 
                address, company_intro, business_scope
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(sql, (
                    row['company_name'], row['company_status'], row['legal_entity_name'], row['reg_capital_amt'],
                    row['es_dt'], row['usc_no'], row['register_addr'], row['province'], row['city'],
                    row['region'], row['phones'], row['more_phones'], row['email'], row['register_type'],
                    row['tax_code'], row['regis_code'], row['org_code'], row['insurance_amount'], row['insurance_year'],
                    row['operation_date'], row['nic_name'], row['nic_1'], row['nic_2'], row['nic_3'], row['qcc_name'], row['qcc_nic_1'],
                    row['qcc_nic_2'], row['qcc_nic_3'], row['company_scale'], row['history_name'], row['english_name'], row['data_source'],
                    row['address'], row['company_intro'], row['business_scope']
                ))
            except:
                continue

            data = {
                'company_name': row['company_name'],
                'company_status': row['company_status'],
                'legal_entity_name': row['legal_entity_name'],
                'reg_capital_amt': row['reg_capital_amt'],
                'es_dt': row['es_dt'],
                'usc_no': row['usc_no'],
                'register_addr': row['register_addr'],
                'province': row['province'],
                'city': row['city'],
                'region': row['region'],
                'phones': row['phones'],
                'more_phones': row['more_phones'],
                'email': row['email'],
                'register_type': row['register_type'],
                'tax_code': row['tax_code'],
                'regis_code': row['regis_code'],
                'org_code': row['org_code'],
                'insurance_amount': row['insurance_amount'],
                'insurance_year': row['insurance_year'],
                'operation_date': row['operation_date'],
                'nic_name': row['nic_name'],
                'nic_1': row['nic_1'],
                'nic_2': row['nic_2'],
                'nic_3': row['nic_3'],
                'qcc_name': row['qcc_name'],
                'qcc_nic_1': row['qcc_nic_1'],
                'qcc_nic_2': row['qcc_nic_2'],
                'qcc_nic_3': row['qcc_nic_3'],
                'company_scale': row['company_scale'],
                'history_name': row['history_name'],
                'english_name': row['english_name'],
                'data_source': row['data_source'],
                'address': row['address'],
                'company_intro': row['company_intro'],
                'business_scope': row['business_scope'],
                'create_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            kafka_producer.send('collect_qcc_list_technology_enterprise', value=data)

        connection.commit()
        kafka_producer.flush()


# 批量处理文件夹中的 Excel 文件
def process_files(folder_path):
    connection = connect_db()
    kafka_producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # 将消息序列化为 JSON 格式
    )

    try:
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.xlsx'):
                file_path = os.path.join(folder_path, file_name)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]Processing {file_path}...")
                process_and_insert_data(file_path, connection, kafka_producer)
    finally:
        connection.close()


# 主程序入口
if __name__ == "__main__":
    file_path = './data/'
    process_files(file_path)
