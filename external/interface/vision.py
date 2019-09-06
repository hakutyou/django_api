from django.conf import settings

from external.service import baidu_vision


class VisionService:
    def __init__(self):
        baidu_vision_service = baidu_vision.BaiduVisionService(client_id=settings.VISION_CLIENT_ID,
                                                               client_secret=settings.VISION_SECRET)
        self.vision_service_list = {
            'baidu': baidu_vision_service
        }

    def image_detect(self, url):
        ret = {}
        for i in self.vision_service_list:
            ret[i] = self.vision_service_list[i].image_detect(url)
        return ret
