# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import time

from scrapy.utils.project import get_project_settings


class MongoDBPipeline(object):
    def __init__(self):
        settings = get_project_settings()

        client = pymongo.MongoClient(settings["MONGO_URL"])
        db = client[settings["MONGO_DATABASE"]]
        self.Information = db[settings["MONGO_TABLE"]]

    def process_item(self, item, spider):
        item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.Information.update(
            {'_id': item['_id']},
            dict(item), upsert=True)
        return item
