#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
import json
from scrapy.contrib.spiders import CrawlSpider, Rule

from ..items import *
from scrapy.contrib.linkextractors import LinkExtractor
import area


class Che168Spider(CrawlSpider):
    name = "che168_area"
    allowed_domains = ['www.che168.com', 'cacheapi.che168.com']
    # start_urls = ['http://www.che168.com/chongqing/list/#pvareaid=100945']
    start_urls = ['http://www.che168.com/{}/list/'.format(v) for (k, v) in area.areaData.items()]

    def __init__(self, *args, **kwargs):
        super(Che168Spider, self).__init__(*args, **kwargs)
        print kwargs

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@id="listpagination"]')),
        Rule(LinkExtractor(allow='.*', restrict_xpaths='//ul[@id="viewlist_ul"]'),
             callback='parse_detail', follow=False,
             ),
    )

    def parse_detail(self, response):
        infoid = response.xpath('//input[@id="car_infoid"]/@value').extract_first()
        if infoid:
            location = response.xpath('//meta[@name="location"]/@content').extract_first()
            [province_str, city_str, _] = location.split(';')
            item = CarItem()
            item['url'] = response.url
            item['province'] = province_str[9:]
            item['city'] = city_str[5:]
            item['price'] = response.xpath('//input[@id="car_price"]/@value').extract_first()
            item['name'] = response.xpath('//input[@id="car_carname"]/@value').extract_first()
            item['mileage'] = response.xpath('//input[@id="car_mileage"]/@value').extract_first()
            item['first_reg_time'] = response.xpath('//input[@id="car_firstregtime"]/@value').extract_first()
            item['_id'] = response.xpath('//input[@id="car_infoid"]/@value').extract_first()

            params = {}
            params['uip'] = response.xpath('//input[@id="uip"]/@value').extract_first()
            params['infoid'] = infoid
            params['sessionid'] = response.xpath('//input[@id="sessionId"]/@value').extract_first()
            params['cid'] = response.xpath('//input[@id="car_cid"]/@value').extract_first()
            params['firstregtime'] = response.xpath('//input[@id="car_firstregtime"]/@value').extract_first()
            params['specid'] = response.xpath('//input[@id="car_specid"]/@value').extract_first()
            params['mileage'] = float(response.xpath('//input[@id="car_mileage"]/@value').extract_first()) * 10000
            url = "http://cacheapi.che168.com/assess/usedcar.ashx?uip={uip}" \
                  "&sessionid={sessionid}&version=2.07v&pid=500000&cid={cid}&" \
                  "mileage={mileage}&firstregtime={firstregtime}&specid={specid}&infoid={infoid}".format(**params)
            request = scrapy.Request(url, self.parse_json)
            request.meta['item'] = item
            request.meta[''] = item
            yield request

    def parse_json(self, response):
        item = response.meta['item']
        try:
            data = json.loads(response.body)
            item['reference_price'] = data['result']['referenceprice']
            item['new_price'] = data['result']['newcarprice']
            yield item
        except Exception:
            yield item
