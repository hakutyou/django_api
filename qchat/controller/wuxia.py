import hashlib
import re
import urllib.request
from urllib.parse import quote, unquote

import requests

from qchat import qchat

wuxia_id = '1450003565'

url_zone_search = 'http://game.gtimg.cn/comm-htdocs/js/game_area/utf8verson' \
                  '/wuxia_server_select_utf8.js'

baseurl_role_search = 'http://api.unipay.qq.com/v1/r/1450003565/get_role_list?pf' \
                      '=pay_center-__mds_webpay_iframe.hy-website'


def zone_mapper():
    content = urllib.request.urlopen(url_zone_search)
    content = content.read().decode('utf-8')[55:-2]
    content = content.replace('t:', '"t":').replace('v:', '"v":').replace(
        'display:', '"display":').replace('status:', '"status":').replace(
        'opt_data_array:', '"opt_data_array":')
    return eval(content)


def zone_to_id(zone):
    gzone = zone_mapper()
    for lzone in gzone:
        for i in lzone['opt_data_array']:
            if i['t'] == zone:
                return i['v']
    return '6101'  # 欢乐英雄


def get_wuxia_role(qq_number, zone, self_id):
    cookies = requests.get('https://coolq.emilia.fun/get_cookies', headers=qchat.headers).json()
    cookies = cookies['data']['cookies']
    n = re.match('.*skey=(?P<skey>.+?);.*', cookies)
    skey = n.group('skey')

    openid = self_id
    openkey = quote(skey)
    session_id = 'uin'
    session_type = 'skey'
    sck = hashlib.md5((wuxia_id + skey).encode('utf-8')).hexdigest().upper()
    provide_uin = qq_number
    zoneid = zone_to_id(zone)

    url = baseurl_role_search
    for i in ['openid', 'openkey', 'session_id', 'session_type',
              'sck', 'provide_uin', 'zoneid']:
        url += f'&{i}={locals()[i]}'
    content = requests.get(url).json()
    if content['ret'] != 0:
        try:
            return content['msg']
        except:
            return '读取失败'
    response = '----角色信息----\n'
    for i in content['role_list']:
        response += unquote(i['role_name']) + '\n'
    return response
