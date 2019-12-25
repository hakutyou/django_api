from external.service import baidu_vision_service


class VisionService:
    def __init__(self):
        self.vision_service_list = {
            'baidu': baidu_vision_service
        }

    def image_detect(self, url):
        ret = {}
        for i in self.vision_service_list:
            ret[i] = self.vision_service_list[i].image_detect(url)
        return ret
