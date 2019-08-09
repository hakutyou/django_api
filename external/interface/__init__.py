from django.conf import settings

from . import baidu, tencent_sms, tencent_cos

baidu_vision_service = baidu.BaiduService(client_id=settings.VISION_CLIENT_ID,
                                          client_secret=settings.VISION_SECRET)

baidu_ocr_service = baidu.BaiduService(client_id=settings.OCR_CLIENT_ID,
                                       client_secret=settings.OCR_SECRET)

tencent_sms_service = tencent_sms.TencentSMSService(appid=settings.SMS_APPID,
                                                    appkey=settings.SMS_APPKEY,
                                                    template_id=settings.SMS_TEMPLATE_ID)

tencent_cos_service = tencent_cos.TencentCoSService(region=settings.COS_REGION, secret_id=settings.COS_ID,
                                                    secret_key=settings.COS_KEY, default_bucket=settings.COS_BUCKET)
