import sys
import traceback
from typing import Callable

from flask import Flask

from .helper.mini.MiniHelper import MiniHelper, AuthResponse
from .helper.sms.SmsHelper import SmsHelper
from .helper.token.TokenHelper import TokenHelper
from .utils.token.Token import Token, TokenStatus, AccessClaims, RefreshClaims


class AuthManager(object):

    def __init__(self):
        self.app = None
        self.app_id = None
        self.app_secret = None
        self.token_secret = None
        self.access_timeout = None
        self.refresh_timeout = None
        self._load_code_callback = None
        self._verify_auth_callback = None

    def init_app(self, app: Flask):
        self.app = app
        self.app_id = app.config.get('APP_ID')
        self.app_secret = app.config.get('APP_SECRET')
        self.token_secret = app.config.get('TOKEN_SECRET')
        self.access_timeout = app.config.get('ACCESS_TOKEN_TIMEOUT')
        self.refresh_timeout = app.config.get('REFRESH_TOKEN_TIMEOUT')
        self.access_key_id = app.config.get('SMS_ACCESS_KEY_ID')
        self.access_key_secret = app.config.get('SMS_ACCESS_KEY_SECRET')
        self.region_id = app.config.get('SMS_REGION_ID')
        self.sign_name = app.config.get('SMS_SIGN_NAME')
        self.template_code = app.config.get('SMS_TEMPLATE_CODE')
        self.template_param = app.config.get('SMS_TEMPLATE_PARAM')

    # def load_code(self, callback) -> str:
    #     self._load_code_callback = callback
    #     return self.load_code_callback
    #
    # @property
    # def load_code_callback(self) -> str:
    #     return self._load_code_callback
    #
    # def verify_auth(self, callback) -> bool:
    #     self._verify_auth_callback = callback
    #     return self.verify_auth_callback
    #
    # @property
    # def verify_auth_callback(self) -> bool:
    #     return self._verify_auth_callback

    def auth_code(self, code: str) -> AuthResponse:
        auth_response = None
        try:
            # code = self._load_code_callback()
            auth_response = MiniHelper.auth(self.app_id, self.app_secret, code, 5)

            if auth_response.errcode is not None:
                raise Exception('obtain auth_response error. errcode: {}'.format(auth_response.errcode))
        except Exception as exception:
            self.app.logger.error('(%s.%s) exception: %s', self.__class__.__name__, sys._getframe().f_code.co_name,
                                  str(exception))
            self.app.logger.error(traceback.format_exc())
        return auth_response

    def decrypt_phone(self, session_key: str, encrypted_data: str, iv: str) -> str:
        phone = None
        try:
            decrypted_dict = MiniHelper.decrypt(self.app_id, session_key, encrypted_data, iv)

            phone = decrypted_dict.get('purePhoneNumber', None)
        except Exception as exception:
            self.app.logger.error('(%s.%s) exception: %s', self.__class__.__name__, sys._getframe().f_code.co_name,
                                  str(exception))
            self.app.logger.error(traceback.format_exc())
        return phone

    def generate_token(self, union_id: str) -> Token:
        token = None
        try:
            token = TokenHelper.generate(union_id, self.token_secret, self.access_timeout, self.refresh_timeout)
        except Exception as exception:
            self.app.logger.error('(%s.%s) exception: %s', self.__class__.__name__, sys._getframe().f_code.co_name,
                                  str(exception))
            self.app.logger.error(traceback.format_exc())
        return token

    def verify_access_token(self, access_token: str) -> TokenStatus:
        token_status = TokenStatus.INVALID
        try:
            access_claims = TokenHelper.parse_access_token(access_token, self.token_secret)
            token_status = TokenHelper.get_access_status(access_claims, self.access_timeout, self.refresh_timeout)
        except Exception as exception:
            self.app.logger.error('(%s.%s) exception: %s', self.__class__.__name__, sys._getframe().f_code.co_name,
                                  str(exception))
            self.app.logger.error(traceback.format_exc())
        return token_status

    def verify_refresh_token(self, refresh_token: str) -> TokenStatus:
        token_status = TokenStatus.INVALID
        try:
            refresh_claims = TokenHelper.parse_refresh_token(refresh_token, self.token_secret)
            token_status = TokenHelper.get_refresh_status(refresh_claims)
        except Exception as exception:
            self.app.logger.error('(%s.%s) exception: %s', self.__class__.__name__, sys._getframe().f_code.co_name,
                                  str(exception))
            self.app.logger.error(traceback.format_exc())
        return token_status

    def refresh_token(self, refresh_token: str) -> Token:
        token = None
        try:
            refresh_claims = TokenHelper.parse_refresh_token(refresh_token, self.token_secret)
            refresh_data = refresh_claims.refresh_data
            access_token = refresh_data.access_token
            access_claims = TokenHelper.parse_access_token(access_token, self.token_secret)
            access_data = access_claims.access_data
            union_id = access_data.union_id
            token = self.generate_token(union_id)
        except Exception as exception:
            self.app.logger.error('(%s.%s) exception: %s', self.__class__.__name__, sys._getframe().f_code.co_name,
                                  str(exception))
            self.app.logger.error(traceback.format_exc())
        return token

    def parse_access_token(self, access_token: str) -> AccessClaims:
        access_claims = None
        try:
            access_claims = TokenHelper.parse_access_token(access_token, self.token_secret)
        except Exception as exception:
            self.app.logger.error('(%s.%s) exception: %s', self.__class__.__name__, sys._getframe().f_code.co_name,
                                  str(exception))
            self.app.logger.error(traceback.format_exc())
        return access_claims

    def parse_refresh_token(self, refresh_token: str) -> RefreshClaims:
        refresh_claims = None
        try:
            refresh_claims = TokenHelper.parse_refresh_token(refresh_token, self.token_secret)
        except Exception as exception:
            self.app.logger.error('(%s.%s) exception: %s', self.__class__.__name__, sys._getframe().f_code.co_name,
                                  str(exception))
            self.app.logger.error(traceback.format_exc())
        return refresh_claims

    def send_sms(self, phone: str, code: str) -> bool:
        template_param = self.template_param.replace('{}', code)

        result = SmsHelper.send(access_key_id=self.access_key_id, access_key_secret=self.access_key_secret,
                                region_id=self.region_id, phone=phone, sign_name=self.sign_name,
                                template_code=self.template_code, template_param=template_param)
        return result

    ##################################################

    def auth(self, code: str, verify_auth_response: Callable[[AuthResponse], bool]) -> Token:
        token = None
        try:
            auth_response = MiniHelper.auth(self.app_id, self.app_secret, code, 5)
            verify_result = verify_auth_response(auth_response)
            if not verify_result:
                raise Exception('verify auth_response error')
            token = TokenHelper.generate(auth_response.unionid, self.token_secret, self.access_timeout,
                                         self.refresh_timeout)
        except Exception as exception:
            self.app.logger.error('(%s.%s) exception: %s', self.__class__.__name__, sys._getframe().f_code.co_name,
                                  str(exception))
            self.app.logger.error(traceback.format_exc())
        return token
