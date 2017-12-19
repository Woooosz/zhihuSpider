# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field() #Male:1
    url_token = scrapy.Field()
    answer_count = scrapy.Field()
    voteup_count = scrapy.Field()
    thanked_count = scrapy.Field()
    participated_live_count = scrapy.Field()
    favorited_count = scrapy.Field()
    follower_count = scrapy.Field()
    following_count = scrapy.Field()
    locations = scrapy.Field()
    description = scrapy.Field()
    educations = scrapy.Field()
    following_question_count = scrapy.Field()
    following_topic_count = scrapy.Field()
    business = scrapy.Field()