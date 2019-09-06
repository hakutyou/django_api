from django.conf import settings

from . import tencent_cos, tencent_sms, face, ocr, vision

face_service = face.FaceService()
ocr_service = ocr.OCRService()
vision_service = vision.VisionService()
tencent_sms_service = tencent_sms.TencentSMSService(appid=settings.SMS_APPID,
                                                    app_key=settings.SMS_APPKEY,
                                                    template_id=settings.SMS_TEMPLATE_ID)

tencent_cos_service = tencent_cos.TencentCoSService(region=settings.COS_REGION, secret_id=settings.COS_ID,
                                                    secret_key=settings.COS_KEY, default_bucket=settings.COS_BUCKET)
