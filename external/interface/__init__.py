from django.conf import settings

from . import baidu_face, baidu_ocr, baidu_vision, tencent_sms, tencent_cos, tencent_face, tencent_ocr

baidu_face_service = baidu_face.BaiduFaceService(client_id=settings.FACE_CLIENT_ID,
                                                 client_secret=settings.FACE_SECRET)

baidu_vision_service = baidu_vision.BaiduVisionService(client_id=settings.VISION_CLIENT_ID,
                                                       client_secret=settings.VISION_SECRET)

baidu_ocr_service = baidu_ocr.BaiduOCRService(client_id=settings.OCR_CLIENT_ID,
                                              client_secret=settings.OCR_SECRET)

tencent_face_service = tencent_face.TencentFaceService(appid=settings.TENCENT_AI_APPID,
                                                       app_key=settings.TENCENT_AI_APPKEY)

tencent_ocr_service = tencent_ocr.TencentOCRService(appid=settings.TENCENT_AI_APPID,
                                                    app_key=settings.TENCENT_AI_APPKEY)

tencent_sms_service = tencent_sms.TencentSMSService(appid=settings.SMS_APPID,
                                                    app_key=settings.SMS_APPKEY,
                                                    template_id=settings.SMS_TEMPLATE_ID)

tencent_cos_service = tencent_cos.TencentCoSService(region=settings.COS_REGION, secret_id=settings.COS_ID,
                                                    secret_key=settings.COS_KEY, default_bucket=settings.COS_BUCKET)
