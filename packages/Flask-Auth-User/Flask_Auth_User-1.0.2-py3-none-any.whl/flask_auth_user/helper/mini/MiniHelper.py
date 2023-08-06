import base64
import json
from typing import Dict

import requests
from Crypto.Cipher import AES


class AuthResponse(object):

    def __init__(self, openid: str = None, session_key: str = None, unionid: str = None, errcode: int = None,
                 errmsg: str = None):
        self.openid = openid
        self.session_key = session_key
        self.unionid = unionid
        self.errcode = errcode
        self.errmsg = errmsg

    def from_dict(self, data: Dict):
        if data is None:
            return
        self.openid = data.get('openid', None)
        self.session_key = data.get('session_key', None)
        self.unionid = data.get('unionid', None)
        self.errcode = data.get('errcode', None)
        self.errmsg = data.get('errmsg', None)

    def to_dict(self) -> Dict:
        data = {
            'openid': self.openid,
            'session_key': self.session_key,
            'unionid': self.unionid,
            'errcode': self.errcode,
            'errmsg': self.errmsg,
        }
        return data

    def to_string(self) -> str:
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False)


class MiniHelper(object):

    @staticmethod
    def auth(app_id: str, app_secret: str, code: str, auth_timeout: int) -> AuthResponse:
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        params = {
            'appid': app_id,
            'secret': app_secret,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
        response = requests.get(url, params, timeout=auth_timeout)

        if response.status_code != 200:
            raise Exception('request auth failed')
        response_content = str(response.content, encoding='utf-8')
        response_data = json.loads(response_content)

        errcode = response_data.get('errcode', None)
        if (errcode is not None) and (errcode != 0):
            raise Exception('the auth request failed. errcode: {}'.format(errcode))

        auth_response = AuthResponse()
        auth_response.from_dict(response_data)
        return auth_response

    @staticmethod
    def decrypt(app_id: str, session_key: str, encrypted_data: str, iv: str) -> Dict:
        session_key = base64.b64decode(session_key)
        encrypted_data = base64.b64decode(encrypted_data)
        iv = base64.b64decode(iv)

        cipher = AES.new(session_key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encrypted_data)
        decrypted_data = decrypted_data[:-ord(decrypted_data[len(decrypted_data) - 1:])]
        decrypted_dict = json.loads(decrypted_data)

        _app_id = None
        watermark = decrypted_dict.get('watermark', None)
        if watermark is not None:
            _app_id = watermark.get('appid', None)
        if _app_id is None:
            raise Exception('obtain app_id failure')

        if _app_id != app_id:
            raise Exception('the app_id is invalid')

        return decrypted_dict
