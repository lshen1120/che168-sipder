#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
import json
from scrapy.contrib.spiders import CrawlSpider, Rule

from ..items import *
from scrapy.contrib.linkextractors import LinkExtractor
import area
import re

detail_pattern = re.compile(r'.*?(?P<year>\d{4})')


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

    def format_expire(self, text):
        str = text.strip()
        if len(str) <= 3:
            return '1970-01'
        else:
            dateStr = str[0:7]
            if len(dateStr) == 6:
                return dateStr[0:4] + '-0' + dateStr[-1]
            else:
                return dateStr

    def get_displacement(self, text):
        index = text.find(u'\uff0f')
        return text[index + 1: -1]

    def parse_detail(self, response):
        infoid = response.xpath('//input[@id="car_infoid"]/@value').extract_first()
        if infoid:
            item = CarItem()
            item['url'] = response.url
            try:
                location = response.xpath('//meta[@name="location"]/@content').extract_first()
                [province_str, city_str, _] = location.split(';')
                item['province'] = province_str[9:]
                item['city'] = city_str[5:]
            except:
                item['city'] = response.xpath('/html/body/div[6]/div[2]/div[3]/ul/li[4]/span//text()').extract_first()
                item['province'] = response.xpath('/html/body/div[5]/a[2]//text()').extract_first()
            item['price'] = response.xpath('//input[@id="car_price"]/@value').extract_first()
            item['name'] = response.xpath('//input[@id="car_carname"]/@value').extract_first()
            match = detail_pattern.match(item['name'])
            if match:
                item['year'] = match.group('year')
            else:
                item['year'] = '-'
            name_detail_list = response.xpath('/html/body/div[5]/a//text()').extract()
            item['brand'] = name_detail_list[-3][2:]
            item['car_model'] = name_detail_list[-2][2:]

            # 行驶里程
            item['mileage'] = response.xpath('//input[@id="car_mileage"]/@value').extract_first()
            # 首次上牌
            item['first_reg_time'] = response.xpath('//input[@id="car_firstregtime"]/@value').extract_first().replace(
                '/', '-')
            item['annual_inspection_expire'] = self.format_expire(
                response.xpath('//*[@id="anchor01"]/ul/li[1]//text()').extract()[1])
            item['insurance_expire'] = self.format_expire(
                response.xpath('//*[@id="anchor01"]/ul/li[2]//text()').extract()[1])
            item['quality_expire'] = self.format_expire(
                response.xpath('//*[@id="anchor01"]/ul/li[3]//text()').extract()[1])
            item['emission_standard'] = response.xpath('//*[@id="anchor01"]/ul/li[4]//text()').extract()[1]
            item['transfer_count'] = response.xpath('//*[@id="anchor01"]/ul/li[5]//text()').extract()[1][0].strip()
            if response.xpath('//*[@id="anchor01"]/ul/li[6]/span//text()').extract_first() == u"证件信息：":
                item['usage'] = response.xpath('//*[@id="anchor01"]/ul/li[7]//text()').extract()[1]
            else:
                item['usage'] = response.xpath('//*[@id="anchor01"]/ul/li[6]//text()').extract()[1]
            item['engine'] = response.xpath('//*[@id="anchor02"]/ul/li[1]//text()').extract()[1].strip()

            try:
                item['displacement'] = self.get_displacement(
                    response.xpath('/html/body/div[6]/div[2]/div[3]/ul/li[3]/span//text()').extract()[0])
            except:
                item['displacement'] = self.get_displacement(
                    response.xpath('/html/body/div[6]/div[2]/div[4]/ul/li[3]/span//text()').extract()[0])

            item['transmission'] = response.xpath('//*[@id="anchor02"]/ul/li[2]//text()').extract()[1]
            item['drive_mode'] = response.xpath('//*[@id="anchor02"]/ul/li[3]//text()').extract()[1]
            item['color'] = response.xpath('//*[@id="anchor02"]/ul/li[4]//text()').extract()[1]
            item['fuel_type'] = response.xpath('//*[@id="anchor02"]/ul/li[5]//text()').extract()[1]
            item['vehicle_level'] = response.xpath('//*[@id="anchor02"]/ul/li[6]//text()').extract()[1]
            item['other_config'] = ",".join(response.xpath('//*[@id="anchor02"]/div[2]/div/ul/li//text()').extract())
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
            reference_price = data['result']['referenceprice'].split('-')

            item['reference_price_low'] = reference_price[0]
            item['reference_price_high'] = reference_price[1]
            item['new_price'] = data['result']['newcarprice']
            yield item
        except Exception:
            yield item
