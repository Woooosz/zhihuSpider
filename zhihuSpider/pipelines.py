# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from zhihuSpider import settings
from zhihuSpider.items import ZhihuspiderItem
import logging

class ZhihuspiderPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == ZhihuspiderItem:
            try:
                self.cursor.execute(
                    "INSERT INTO person_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (item['name'], item['gender'], item['url_token'], item['answer_count'],
                        item['voteup_count'],item['thanked_count'],item['participated_live_count'],
                        item['favorited_count'], item['follower_count'], item['following_count'], item['locations'],
                        item['description'], item['educations'], item['following_question_count'], item['following_topic_count'], item['business']
                        )
                    )
                self.connect.commit()
            except Exception:
                logging.warning("Database Write Exception")
        else:
            pass