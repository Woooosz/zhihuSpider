import json
import base64
import requests
from lxml import etree
import logging
import time
import redis
from zhihuSpider import settings
from zhihuSpider.tools import qrcode_terminal

def getCookies():
    red = redis.Redis(host = settings.REDIS_HOST, port = settings.REDIS_PORT)
    if not red.exists('zhihu:cookie'):
        logging.warning('Cookie expired, getting cookie via simulate login')
        session = requests.Session()
        r = session.get('https://zhihu.com/signin',headers = settings.DEFAULT_REQUEST_HEADERS)
        info = r.content.decode('utf8')
        #拿xsrf
        xsrf = etree.HTML(info).xpath('//input [@name="_xsrf"]/@value')[0]
        #设置headers
        headers = settings.DEFAULT_REQUEST_HEADERS
        headers['Referer'] = "https://www.zhihu.com/signin"
        #拿udid的cookie
        r = session.post('https://www.zhihu.com/udid', headers = headers, data = {'_xsrf':xsrf})
        #拿二维码的token
        r = session.post('https://account.zhihu.com/api/login/qrcode', headers = headers, data = {'client_id':'060fc1d4872f49ec89d74814806b1c8e'})
        s = json.loads(r.content.decode('utf8'))
        #生成二维码
        qrcode_terminal.draw('https://www.zhihu.com/account/scan/login/' + s['token'], 1)
        print('Plz scan your Qrcode & confirm validation in 10s...')
        time.sleep(10)
        #拿到Server确认cookie
        r = session.get('https://account.zhihu.com/api/login/qrcode/'+ s['token'] +'/scan_info?client_id=060fc1d4872f49ec89d74814806b1c8e',headers = headers)

        logging.warning('Get cookie success, storing into redis...')
        cookie = session.cookies.get_dict()

        red.set('zhihu:cookie',cookie)
        red.expire('zhihu:cookie',2590000)
        logging.warning('Cookie stored')
        return cookie
    else:
        return json.loads(red.get('zhihu:cookie').decode('utf8').replace("\"", "").replace("\'","\""))