from django.conf import settings

from . import baidu, baidu_face, tencent_sms, tencent_cos, tencent_ai

baidu_face_service = baidu_face.BaiduFaceService(client_id=settings.FACE_CLIENT_ID,
                                                 client_secret=settings.FACE_SECRET)

baidu_vision_service = baidu.BaiduService(client_id=settings.VISION_CLIENT_ID,
                                          client_secret=settings.VISION_SECRET)

baidu_ocr_service = baidu.BaiduService(client_id=settings.OCR_CLIENT_ID,
                                       client_secret=settings.OCR_SECRET)

tencent_ai_service = tencent_ai.TencentAIService(appid=settings.TENCENT_AI_APPID,
                                                 app_key=settings.TENCENT_AI_APPKEY)

tencent_sms_service = tencent_sms.TencentSMSService(appid=settings.SMS_APPID,
                                                    app_key=settings.SMS_APPKEY,
                                                    template_id=settings.SMS_TEMPLATE_ID)

tencent_cos_service = tencent_cos.TencentCoSService(region=settings.COS_REGION, secret_id=settings.COS_ID,
                                                    secret_key=settings.COS_KEY, default_bucket=settings.COS_BUCKET)
