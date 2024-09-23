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


class ListUnicornItem(scrapy.Item):
    id = scrapy.Field()
    full_name = scrapy.Field()
    image_url = scrapy.Field()
    country = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    is_listed = scrapy.Field()
    is_technology_organization = scrapy.Field()
    set_up_time = scrapy.Field()
    last_cognizance = scrapy.Field()
    cognizances = scrapy.Field()
    high_tech_zone = scrapy.Field()
    level = scrapy.Field()
    area_path = scrapy.Field()
    field_path = scrapy.Field()
    field = scrapy.Field()
    industry_path = scrapy.Field()
    industry = scrapy.Field()
    cognizance_year = scrapy.Field()
    cognizance_type = scrapy.Field()
    origin_cognizance_type = scrapy.Field()
    register_status = scrapy.Field()
    identified_time = scrapy.Field()
    historys = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    update_time = scrapy.Field()
    create_time = scrapy.Field()


class HiddenChampionItem(scrapy.Item):
    ENTID = scrapy.Field()
    entname = scrapy.Field()
    regcap = scrapy.Field()
    esdate = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    tel = scrapy.Field()
    email = scrapy.Field()
    creidtcode = scrapy.Field()
    tax_code = scrapy.Field()
    regis_code = scrapy.Field()
    org_code = scrapy.Field()
    emp = scrapy.Field()
    entstype = scrapy.Field()
    industry = scrapy.Field()
    dom = scrapy.Field()
    OPSCOPE = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()


class ECqsItem(scrapy.Item):
    creditname = scrapy.Field()
    prodname = scrapy.Field()
    licenceno = scrapy.Field()
    licmatter = scrapy.Field()
    orgaddr = scrapy.Field()
    testlocus = scrapy.Field()
    province = scrapy.Field()
    certdate = scrapy.Field()
    certvaliddate = scrapy.Field()
    model2 = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
