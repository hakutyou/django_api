import string

from django.core.cache import cache
from qcloudsms_py import SmsSingleSender

from utils.utils import message_digest, random_string


class TencentSMSService:
    def __init__(self, appid, app_key, template_id):
        self.sms_sender = SmsSingleSender(appid, app_key)
        self.template_id = template_id

    def send_sms(self, name, phone_number, timeout: int = 3):
        code = random_string(string.digits, length=5)
        params = [code, str(timeout)]
        try:
            self.sms_sender.send_with_param(
                86, phone_number,
                self.template_id, params, '', '', '')
        except Exception as e:
            # print(e)
            return False
        cache.set(f'sms:{phone_number}:{message_digest(name)}', code, timeout * 60 + 10)
        return True

    @staticmethod
    def check_sms(name, phone_number, code):
        cache_key = f'sms:{phone_number}:{message_digest(name)}'
        real_code = cache.get(cache_key)
        if code == real_code:
            cache.delete(cache_key)
            return True
        return False
