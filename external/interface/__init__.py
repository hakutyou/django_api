from django.conf import settings

from . import baidu, tencent

baidu_vision_service = baidu.BaiduService(client_id=settings.VISION_CLIENT_ID,
                                          client_secret=settings.VISION_SECRET)

baidu_ocr_service = baidu.BaiduService(client_id=settings.OCR_CLIENT_ID,
                                       client_secret=settings.OCR_SECRET)

tencent_sms_service = tencent.TencentService(appid=settings.SMS_APPID,
                                             appkey=settings.SMS_APPKEY,
                                             template_id=settings.SMS_TEMPLATE_ID)
