from django.conf import settings

from . import tencent_face, baidu_face, tencent_ocr, baidu_vision, tencent_scf

# 人脸识别
tencent_face_service = tencent_face.TencentFaceService(appid=settings.TENCENT_AI_APPID,
                                                       app_key=settings.TENCENT_AI_APPKEY)
baidu_face_service = baidu_face.BaiduFaceService(client_id=settings.FACE_CLIENT_ID,
                                                 client_secret=settings.FACE_SECRET)

# OCR 识别
# 关闭百度的 OCR 识别（有限次免费）
# baidu_ocr_service = baidu_ocr.BaiduOCRService(client_id=settings.OCR_CLIENT_ID,
#                                               client_secret=settings.OCR_SECRET)
tencent_ocr_service = tencent_ocr.TencentOCRService(appid=settings.TENCENT_AI_APPID,
                                                    app_key=settings.TENCENT_AI_APPKEY)

baidu_vision_service = baidu_vision.BaiduVisionService(client_id=settings.VISION_CLIENT_ID,
                                                       client_secret=settings.VISION_SECRET)

# 腾讯 SCF
scf_service = tencent_scf.TencentSCFService(secret_id=settings.TENCENT_SCF_SECRET_ID,
                                            secret_key=settings.TENCENT_SCF_SECRET_KEY)
