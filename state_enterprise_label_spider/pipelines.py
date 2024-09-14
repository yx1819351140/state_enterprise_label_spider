# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
import json
from loguru import logger
from state_enterprise_label_spider.items import BaseInfoItem, ListUnicornItem, HiddenChampionItem
from kafka import KafkaProducer


class StateEnterpriseLabelSpiderPipeline:

    def open_spider(self, spider):
        host = spider.settings.get('MYSQL_HOST')
        port = spider.settings.get('MYSQL_PORT')
        user = spider.settings.get('MYSQL_USER')
        password = spider.settings.get('MYSQL_PASSWORD')
        db = spider.settings.get('MYSQL_DB')
        self.client = pymysql.connect(host=host, user=user, password=password, database=db, charset="utf8",port=port)
        self.cursor_doris = self.client.cursor()

        kafka_servers = spider.settings.get('KAFKA_BOOTSTRAP_SERVERS')
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # 将消息序列化为 JSON 格式
        )

    def process_item(self, item, spider):
        if isinstance(item, BaseInfoItem):
            table = '20221018001_3_data'
            topic = 'collect_guoqi_base_info'
        elif isinstance(item, ListUnicornItem):
            table = 'list_unicorn_enterprise'
            topic = 'collect_list_unicorn_enterprise'
        elif isinstance(item, HiddenChampionItem):
            table = 'hidden_champion_ent'
            topic = 'collect_hidden_champion_ent'
        else:
            table = ''
            topic = ''

        if table:
            self.save_data(item, table)
        if topic:
            self.send_to_kafka(item, topic)
        return item

    def save_data(self, item, table_name):
        try:
            # 获取表的列名
            self.cursor_doris.execute(f'desc `{table_name}`')
            columns = [row[0] for row in self.cursor_doris.fetchall()]
            # 准备插入数据
            data = {}
            for column in columns:
                if column in item:
                    data[column] = item[column]
            if not data:
                logger.error(f'【{table_name}】映射数据表为空：{item}')
            # 构建SQL语句
            columns_str = ", ".join(f"`{col}`" for col in data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            sql = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"
            values = tuple(data.values())
            # 执行SQL插入
            self.cursor_doris.execute(sql, values)
            logger.info(f"【{table_name}】数据插入到 Tidb 成功!")
        except Exception as e:
            logger.error(f'【{table_name}】插入数据失败，失败原因：{e}')

    def send_to_kafka(self, item, topic):
        try:
            # 将 item 序列化为字典，然后发送到 Kafka
            self.kafka_producer.send(topic, value=dict(item))
            self.kafka_producer.flush()
            logger.info(f"【{topic}】数据发送到 Kafka 成功!")
        except Exception as e:
            logger.error(f'【{topic}】发送数据到 Kafka 失败，失败原因：{e}')

    def close_spider(self, spider):
        self.client.commit()
        self.client.close()
