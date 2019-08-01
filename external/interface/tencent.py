from django.core.cache import cache
from qcloudsms_py import SmsSingleSender

from utils.utils import hash, random_string


class TencentService:
    def __init__(self, appid, appkey, template_id):
        self.ssender = SmsSingleSender(appid, appkey)
        self.template_id = template_id

    def send_sms(self, name, phone_number, timeout: int = 3):
        code = random_string(length=5)
        params = [code, str(timeout)]
        try:
            self.ssender.send_with_param(
                86, phone_number,
                self.template_id, params, '', '', '')
        except Exception as e:
            print(e)
            return False
        cache.set(f'sms:{phone_number}:{hash(name)}', code, timeout * 60 + 10)
        return True

    def check_sms(self, name, phone_number, code):
        real_code = cache.get(f'sms:{phone_number}:{hash(name)}')
        if code == real_code:
            return True
        return False
