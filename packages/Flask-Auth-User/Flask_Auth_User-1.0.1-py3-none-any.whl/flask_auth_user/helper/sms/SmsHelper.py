import json
import random
import string

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


class SmsHelper(object):

    @staticmethod
    def build_code(len: int = 4) -> str:
        return "".join(random.sample(string.digits, len))

    @staticmethod
    def send(access_key_id: str, access_key_secret: str, region_id: str, phone: str, sign_name: str, template_code: str,
             template_param: str) -> bool:
        result = False

        client = AcsClient(access_key_id, access_key_secret,  region_id)

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')
        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', sign_name)
        request.add_query_param('TemplateCode', template_code)
        request.add_query_param('TemplateParam', template_param)

        body_bytes = client.do_action_with_exception(request)
        body = str(body_bytes, encoding='utf-8')
        body_dict = json.loads(body)
        if (body_dict is not None) and (body_dict.get('Message', None) == 'OK'):
            result = True
        return result
