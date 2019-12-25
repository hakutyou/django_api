from external.service import tencent_ocr_service


class OCRService:
    def __init__(self):
        self.ocr_service_list = {
            'tencent': tencent_ocr_service,
            # 'baidu': baidu_ocr_service,
        }

    def ocr_general(self, url, lang):
        data = {}
        for i in self.ocr_service_list:
            data[i] = self.ocr_service_list[i].ocr_general(url, lang)
        return data
