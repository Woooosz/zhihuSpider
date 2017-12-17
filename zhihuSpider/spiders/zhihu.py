# -*- coding: utf-8 -*-
import scrapy
from zhihuSpider.items import ZhihuspiderItem
from zhihuSpider.tools import qrcode_terminal
import time
import json


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    xsrf = ''
    cur_url_token = ''
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
        "Referer": "https://www.zhihu.com/"
        }
    scrawl_ID = {'hesenbao', 'ZitongZeng'}
    finish_ID = set()


    url_person_info_url = 'https://www.zhihu.com/api/v4/members/%s?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,is_org_createpin_white_user,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    url_person_follower_url = 'https://www.zhihu.com/api/v4/members/%s/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=%s&limit=20'


    def start_requests(self):
        yield scrapy.Request("https://zhihu.com/signin", headers = self.headers,
            meta={"cookiejar":1},
            callback = self.get_udid)

    def get_udid(self, response):
        self.xsrf = response.xpath('//input [@name="_xsrf"]/@value').extract()[0]
        headers = self.headers
        headers['Referer'] = "https://www.zhihu.com/signin"
        yield scrapy.FormRequest(
            url = 'https://www.zhihu.com/udid',
            headers = self.headers,
            formdata = {'_xsrf':self.xsrf},
            meta={'cookiejar':response.meta['cookiejar']},
            callback = self.pre_ecode
        )

    def pre_ecode(self, response):
        headers = self.headers
        headers['Referer'] = "https://www.zhihu.com/signin"
        yield scrapy.FormRequest(
            url = 'https://account.zhihu.com/api/login/qrcode',
            headers = self.headers,
            formdata = {'client_id':'060fc1d4872f49ec89d74814806b1c8e'},
            meta={'cookiejar':response.meta['cookiejar']},
            callback = self.get_ecode
        )

    def get_ecode(self, response):
        s = json.loads(response.body)
        qrcode_terminal.draw('https://www.zhihu.com/account/scan/login/' + s['token'], 1)
        print('Plz scan your Qrcode in 10s……')
        time.sleep(10)

        yield scrapy.Request(
            url = 'https://account.zhihu.com/api/login/qrcode/'+ s['token'] +'/scan_info?client_id=060fc1d4872f49ec89d74814806b1c8e',
            meta={'cookiejar':response.meta['cookiejar']},
            headers = self.headers,
            callback = self.start_scrawl
            )


    def start_scrawl(self, response):
        while len(self.scrawl_ID):
            url_token = self.scrawl_ID.pop()
            self.finish_ID.add(url_token)
            self.cur_url_token = url_token
            yield scrapy.Request(
                url =self.url_person_info_url % url_token,
                meta={'cookiejar':response.meta['cookiejar']},
                headers = self.headers,
                callback = self.parse_person_info
            )

            yield scrapy.Request(
                url = self.url_person_follower_url % (url_token,'0'),
                meta={'cookiejar':response.meta['cookiejar'],'offset':'0'},
                headers = self.headers,
                callback = self.parse_followers
            )

    def parse_person_info(self, response):
        s = json.loads(response.body.decode('utf8'))
        item = ZhihuspiderItem()
        item['name'] = str(s['name'])
        item['gender'] = int(s['gender'])
        item['url_token'] = str(s['url_token'])
        item['answer_count'] = int(s['answer_count'])
        item['voteup_count'] = int(s['voteup_count'])
        item['thanked_count'] = int(s['thanked_count'])
        item['participated_live_count'] = int(s['participated_live_count'])
        item['favorited_count'] = int(s['favorited_count'])
        item['follower_count'] = int(s['follower_count'])
        item['following_count'] = int(s['following_count'])
        try:
            item['locations'] = str(s['locations'][0]['name'])
        except Exception:
            item['locations'] = ''
        yield item

    def parse_followers(self, response):
        s = json.loads(response.body.decode('utf8'))
        for i in s['data']:
            if i['url_token'] not in self.scrawl_ID:
                self.scrawl_ID.add(i['url_token'])
        if(s['paging']['is_end'] != True):
            next = str(int(response.meta['offset']) + 20)
            yield scrapy.Request(
                url = self.url_person_follower_url % (self.cur_url_token,next),
                meta={'cookiejar':response.meta['cookiejar'],'offset':next},
                headers = self.headers,
                callback = self.parse_followers
            )

    def parse(self, response):
        pass