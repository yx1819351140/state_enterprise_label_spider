# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseInfoItem(scrapy.Item):
    update_time = scrapy.Field()
    create_time = scrapy.Field()
    from_url = scrapy.Field()
    url = scrapy.Field()
    attrib_level = scrapy.Field()
    attrib = scrapy.Field()
    name = scrapy.Field()
    code = scrapy.Field()
