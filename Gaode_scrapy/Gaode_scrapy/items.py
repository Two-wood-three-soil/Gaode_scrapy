# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GaodeScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    gaode_id = scrapy.Field()
    name = scrapy.Field()  #名称
    biz_type = scrapy.Field() #行业类型
    address = scrapy.Field()
    lowest_price = scrapy.Field()  # 最低价格
    location = scrapy.Field() #经纬度
    tel = scrapy.Field() # 手机号码
    zip_code = scrapy.Field() # 邮编
    pcode = scrapy.Field() # #省份编码
    province_name = scrapy.Field() # 省份名
    city_code = scrapy.Field()  # 城市编码
    city_name = scrapy.Field() # 城市名
    adcode = scrapy.Field() # 行政编码
    adname = scrapy.Field() #
    website = scrapy.Field() # 官网
    entr_location = scrapy.Field() #入口经纬度
    exit_location = scrapy.Field() #出口经纬度
    business_area = scrapy.Field() #shangquan
    type_a = scrapy.Field()  #兴趣点大类
    type_b = scrapy.Field()  #兴趣点中类
    type_c = scrapy.Field()  #兴趣点小类
    update_time = scrapy.Field() #更新时间