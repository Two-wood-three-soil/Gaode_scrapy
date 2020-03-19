# -*- coding: utf-8 -*-
import json
import time

import requests
import scrapy
from scrapy.exceptions import CloseSpider

from ..settings import types
from ..mysql_action import SessionMysql


class GaodeSpiderSpider(scrapy.Spider):
    name = 'gaode_spider'
    allowed_domains = ['restapi.amap.com']
    start_urls = 'http://restapi.amap.com/'
    ins_tablename = "land_resource_info"
    update = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    select_sql = "select gaode_id from {0} where gaode_id = ".format(
        ins_tablename)

    offset = 0  # 每頁返回幾條
    count = 100
    _count = 0

    def start_requests(self):
        provinces = [
            '山西省',
            '吉林省',
            '江苏省',
            '浙江省',
            '安徽省',
            '河南省',
            '湖北省',
            '湖南省',
            '广东省',
            '海南省',
            '四川省',
            '贵州省',
            '云南省',
            '陕西省',
            '甘肃省',
            '青海省',
            '黑龙江省',
            '西藏自治区',
            '内蒙古自治区',
            '广西壮族自治区',
            '宁夏回族自治区',
            '新疆维吾尔自治区',
            '香港',
            '澳门',
            '台湾',
            '北京市',
            '天津市',
            '上海市',
            '重庆市']
        next_url = "v3/place/text?"
        basic_url = self.start_urls + next_url
        # index = 50
        for province in provinces:
            select_sql = "SELECT DISTINCT district_adcode FROM `districts_info` where province_name ='{0}' ".format(
                province)
            citys = SessionMysql().select_districts_info(select_sql)
            for k, v in types.items():
                for city in citys:
                    index = 45
                    for i in range(1, index):
                        # print(self._count)
                        if self._count >= 150000:
                            time.sleep(60*60*60)

                        # print(self.count)
                        if self.count != 0:
                            params = {
                                "key": "7a7102893c6c5522ba21885cce07a46b",
                                "keyword": v,
                                "city": city,
                                "citylimit": "true",
                                "page": i,
                                "types": k,
                                "extensions": "all",
                                "offset": 25
                            }
                            # print(params)
                            url = requests.get(basic_url, params=params).url
                            yield scrapy.Request(url, callback=self.parse, dont_filter=True)
                        # 如果count=0，说明数据为空
                        elif self.count == 0:
                            self._count += 1
                            self.count = 100
                            break
                        else:
                            self._count += 1
                            break

    def parse(self, response):
        self._count += 1
        poi_dic = {}
        response_json = json.loads(response.text)
        # print(response_json)
        if response_json != {}:
            # 获取count数量
            self.count = response_json["count"]
            pois = response_json["pois"]
            if pois != []:
                for poi in pois:
                    poi_dic["gaode_id"] = poi["id"]
                    poi_dic["name"] = poi["name"]  # 名称
                    poi_dic["biz_type"] = poi["biz_type"]  # 行业类型
                    poi_dic["address"] = poi["pname"] + \
                        poi["cityname"] + poi["adname"]
                    poi_dic["lowest_price"] = list(poi["biz_ext"].values())[-1]
                    poi_dic["location"] = poi["location"]  # 经纬度
                    poi_dic["tel"] = poi["tel"]
                    poi_dic["zip_code"] = poi["postcode"]  # 邮编
                    poi_dic["pcode"] = poi["pcode"]  # 省份编码
                    poi_dic["province_name"] = poi["pname"]  # 省份名
                    poi_dic["city_code"] = poi["citycode"]
                    poi_dic["city_name"] = poi["cityname"]
                    poi_dic["adcode"] = poi["adcode"]  # 行政编码
                    poi_dic["adname"] = poi["adname"]
                    poi_dic["website"] = poi["website"]
                    # poi_dic["parking_type"] = poi["parking_type"] #停车场类型
                    poi_dic["entr_location"] = poi["entr_location"]  # 入口经纬度
                    poi_dic["exit_location"] = poi["exit_location"]  # 出口经纬度
                    poi_dic["business_area"] = poi["business_area"]  # shangquan
                    try:
                        _type = poi["type"].split(";")
                        if _type.__len__() >= 3:
                            poi_dic["type_a"] = _type[0]  # 兴趣点大类
                            poi_dic["type_b"] = ",".join(_type[0:-2])
                            poi_dic["type_c"] = _type[-1]
                        else:
                            # print(poi_dic)
                            poi_dic["type_a"] = _type
                    except Exception as e:
                        poi_dic["type_a"] = poi["type"]
                        # print(e)
                    poi_dic["update_time"] = self.update
                    select_sql = self.select_sql + "\'" + \
                        poi["id"] + "\'"  # 去重的sql语句
                    sessionmysql = SessionMysql(
                        data=poi_dic, tablename=self.ins_tablename)
                    if sessionmysql.is_redundant(select_sql) == []:
                        sessionmysql.execute_sql(action="insert")
                    else:
                        with open("redundant.txt", "a+") as f:
                            f.write(str(poi["id"]) + poi["name"] + "\n")
                        # print("数据重复")
            else:
                return

    # def get_apge(self, url, city):
    #     params = {
    #         "key": "f1b0700972ef778a6fd9c32751eb23a5",
    #         "keyword": "酒店",
    #         "city": city,
    #         "citylimit": "true",
    #         "page": 1,
    #         "types": "100000",
    #         "extensions": "all"
    #     }
    #     count = requests.get(url=url, params=params).json()["count"]
	#
    #     return
