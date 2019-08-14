from decouple import config

from . import wechat

wechat_official = wechat.WechatOfficial(token=config('WECHAT_OFFICIAL_TOKEN'))
