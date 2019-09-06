from django.conf import settings

from external.service import tencent_ocr, baidu_ocr


class OCRService:
    def __init__(self):
        baidu_ocr_service = baidu_ocr.BaiduOCRService(client_id=settings.OCR_CLIENT_ID,
                                                      client_secret=settings.OCR_SECRET)

        tencent_ocr_service = tencent_ocr.TencentOCRService(appid=settings.TENCENT_AI_APPID,
                                                            app_key=settings.TENCENT_AI_APPKEY)
        self.ocr_service_list = {
            'tencent': tencent_ocr_service,
            'baidu': baidu_ocr_service,
        }

    def ocr_general(self, url, lang):
        data = {}
        for i in self.ocr_service_list:
            data[i] = self.ocr_service_list[i].ocr_general(url, lang)
        return data
