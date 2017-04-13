# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    new_price = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    mileage = scrapy.Field()
    first_reg_time = scrapy.Field()
    reference_price = scrapy.Field()
    update_time = scrapy.Field()
