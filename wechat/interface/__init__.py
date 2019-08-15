from decouple import config

from . import wechat

wechat_official = wechat.WechatOfficial(appid=config('WECHAT_APPID'), appsecret=config('WECHAT_APPSECRET'),
                                        token=config('WECHAT_OFFICIAL_TOKEN'), aes_key=config('WECHAT_AES_KEY'))
