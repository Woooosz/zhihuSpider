import json
import base64
import requests
import re
import logging
import time
import redis
import settings
from tools import qrcode_terminal

def getCookies():
    red = redis.Redis(host = settings.REDIS_HOST, port = settings.REDIS_PORT)
    if not red.exists('zhihu:cookie'):
        session = requests.Session()
        r = session.get('https://zhihu.com/signin',headers = settings.DEFAULT_REQUEST_HEADERS)
        session.cookies.set('acw_tc',None)
        #设置headers
        headers = settings.DEFAULT_REQUEST_HEADERS
        headers['Referer'] = "https://www.zhihu.com/signin"

        r = session.get('https://static.zhihu.com/heifetz/main.app.71184930c9b1fc530258.js')
        authorization = re.match(r"(?<=h=\")[0-9a-z]{32}$",r.content.decode('utf8'))

        # 更新header
        headers['authorization'] = "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
        r = session.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=cn', headers = headers)

        r = session.post('https://account.zhihu.com/api/login/qrcode', headers = headers)
        s = json.loads(r.content.decode('utf8'))
        token = s['token']
        qrcode_terminal.draw('https://www.zhihu.com/account/scan/login/%s' % token, 1)
        time.sleep(10)

        s = session.get('https://account.zhihu.com/api/login/qrcode/%s/scan_info' % token ,headers = headers)

        logging.warning('Get cookie success, storing into redis...')
        cookie = session.cookies.get_dict()

        red.set('zhihu:cookie',cookie)
        red.expire('zhihu:cookie',2590000)
        logging.warning('Cookie stored')
        return cookie
    else:
    return json.loads(red.get('zhihu:cookie').decode('utf8').replace("\"", "").replace("\'","\""))
