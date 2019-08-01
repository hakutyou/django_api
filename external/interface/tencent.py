from qcloudsms_py import SmsSingleSender


class TencentService:
    base_url = 'https://aip.baidubce.com'

    def __init__(self, appid, appkey, template_id):
        self.ssender = SmsSingleSender(appid, appkey)
        self.template_id = template_id

    def send_sms(self, phone_number, code, timeout='3'):
        params = [code, timeout]
        try:
            result = self.ssender.send_with_param(
                86, phone_number,
                self.template_id, params, '', '', '')
        except Exception as e:
            print(e)
            return
        print(result)
