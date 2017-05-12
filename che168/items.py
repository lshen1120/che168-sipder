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
    price = scrapy.Field()                      # 报价
    new_price = scrapy.Field()                  # 新车价
    province = scrapy.Field()                   # 省
    city = scrapy.Field()                       # 城市
    mileage = scrapy.Field()                    # 里程数
    first_reg_time = scrapy.Field()             # 首次上牌
    reference_price = scrapy.Field()            # 参考价(区间) 15.4-18
    reference_price_low = scrapy.Field()        # 最低参考价 15
    reference_price_high = scrapy.Field()       # 最高参考价 18
    update_time = scrapy.Field()                # 更新时间
    annual_inspection_expire = scrapy.Field()   # 年检到期 已过期的值表示为1970-01-01
    insurance_expire = scrapy.Field()           # 保险到期 已过期的值表示为1970-01-01
    quality_expire = scrapy.Field()             # 质保到期 已过期的值表示为1970-01-01
    transfer_count = scrapy.Field()             # 过户次数
    emission_standard = scrapy.Field()          # 排放标准
    usage = scrapy.Field()                      # 用途
    engine = scrapy.Field()                     # 发动机
    transmission = scrapy.Field()               # 变速器
    drive_mode = scrapy.Field()                 # 驱动方式
    color = scrapy.Field()                      # 颜色
    fuel_type = scrapy.Field()                  # 燃油标号
    vehicle_level = scrapy.Field()              # 车辆级别
    other_config = scrapy.Field()               # 其他配置
