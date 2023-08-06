import json
from enum import Enum
from typing import Dict

import jwt


class StandardClaims(object):

    def __init__(self, audience: str = None, expires_at: int = None, id: str = None, issued_at: int = None,
                 issuer: str = None, not_before: int = None, subject: str = None):
        self.audience = audience
        self.expires_at = expires_at
        self.id = id
        self.issued_at = issued_at
        self.issuer = issuer
        self.not_before = not_before
        self.subject = subject

    def to_dict(self) -> Dict:
        data = {}
        if self.audience is not None:
            data['aud'] = self.audience
        if self.expires_at is not None:
            data['exp'] = self.expires_at
        if self.id is not None:
            data['jti'] = self.id
        if self.issued_at is not None:
            data['iat'] = self.issued_at
        if self.issuer is not None:
            data['iss'] = self.issuer
        if self.not_before is not None:
            data['nbf'] = self.not_before
        if self.subject is not None:
            data['sub'] = self.subject
        return data

    def to_string(self) -> str:
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False)


class AccessData(object):

    def __init__(self, union_id: str = None, issued_at: int = None, expires_at: int = None):
        self.union_id = union_id
        self.issued_at = issued_at
        self.expires_at = expires_at

    def from_dict(self, data: Dict):
        if data is None:
            return
        self.union_id = data.get('union_id', None)
        self.issued_at = data.get('issued_at', None)
        self.expires_at = data.get('expires_at', None)

    def to_dict(self) -> Dict:
        data = {}
        if self.union_id is not None:
            data['union_id'] = self.union_id
        if self.issued_at is not None:
            data['issued_at'] = self.issued_at
        if self.expires_at is not None:
            data['expires_at'] = self.expires_at
        return data

    def to_string(self) -> str:
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False)


class AccessClaims(StandardClaims):

    def __init__(self, audience: str = None, expires_at: int = None, id: str = None, issued_at: int = None,
                 issuer: str = None, not_before: int = None, subject: str = None, access_data: AccessData = None):
        super(AccessClaims, self).__init__(audience=audience, expires_at=expires_at, id=id, issued_at=issued_at,
                                           issuer=issuer, not_before=not_before, subject=subject)
        self.access_data = access_data

    def from_dict(self, access_dict: Dict):
        if access_dict is None:
            return
        self.audience = access_dict.get('aud', None)
        self.expires_at = access_dict.get('exp', None)
        self.id = access_dict.get('jti', None)
        self.issued_at = access_dict.get('iat', None)
        self.issuer = access_dict.get('iss', None)
        self.not_before = access_dict.get('nbf', None)
        self.subject = access_dict.get('sub', None)
        _access_data = access_dict.get('data', None)
        if self.access_data is None:
            self.access_data = AccessData()
        self.access_data.from_dict(_access_data)

    def to_dict(self) -> Dict:
        data = {}
        if self.audience is not None:
            data['aud'] = self.audience
        if self.expires_at is not None:
            data['exp'] = self.expires_at
        if self.id is not None:
            data['jti'] = self.id
        if self.issued_at is not None:
            data['iat'] = self.issued_at
        if self.issuer is not None:
            data['iss'] = self.issuer
        if self.not_before is not None:
            data['nbf'] = self.not_before
        if self.subject is not None:
            data['sub'] = self.subject
        if self.access_data is not None:
            data['data'] = self.access_data.to_dict()
        return data

    def to_string(self) -> str:
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False)


class RefreshData(object):

    def __init__(self, access_token: str = None, issued_at: int = None, expires_at: int = None):
        self.access_token = access_token
        self.issued_at = issued_at
        self.expires_at = expires_at

    def from_dict(self, data: Dict):
        if data is None:
            return
        self.access_token = data.get('access_token', None)
        self.issued_at = data.get('issued_at', None)
        self.expires_at = data.get('expires_at', None)

    def to_dict(self) -> Dict:
        data = {}
        if self.access_token is not None:
            data['access_token'] = self.access_token
        if self.issued_at is not None:
            data['issued_at'] = self.issued_at
        if self.expires_at is not None:
            data['expires_at'] = self.expires_at
        return data

    def to_string(self) -> str:
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False)


class RefreshClaims(StandardClaims):

    def __init__(self, audience: str = None, expires_at: int = None, id: str = None, issued_at: int = None,
                 issuer: str = None, not_before: int = None, subject: str = None, refresh_data: RefreshData = None):
        super(RefreshClaims, self).__init__(audience=audience, expires_at=expires_at, id=id, issued_at=issued_at,
                                            issuer=issuer, not_before=not_before, subject=subject)
        self.refresh_data = refresh_data

    def from_dict(self, refresh_dict: Dict):
        if refresh_dict is None:
            return
        self.audience = refresh_dict.get('aud', None)
        self.expires_at = refresh_dict.get('exp', None)
        self.id = refresh_dict.get('jti', None)
        self.issued_at = refresh_dict.get('iat', None)
        self.issuer = refresh_dict.get('iss', None)
        self.not_before = refresh_dict.get('nbf', None)
        self.subject = refresh_dict.get('sub', None)
        _refresh_data = refresh_dict.get('data', None)
        if self.refresh_data is None:
            self.refresh_data = RefreshData()
        self.refresh_data.from_dict(_refresh_data)

    def to_dict(self) -> Dict:
        data = {}
        if self.audience is not None:
            data['aud'] = self.audience
        if self.expires_at is not None:
            data['exp'] = self.expires_at
        if self.id is not None:
            data['jti'] = self.id
        if self.issued_at is not None:
            data['iat'] = self.issued_at
        if self.issuer is not None:
            data['iss'] = self.issuer
        if self.not_before is not None:
            data['nbf'] = self.not_before
        if self.subject is not None:
            data['sub'] = self.subject
        if self.refresh_data is not None:
            data['data'] = self.refresh_data.to_dict()
        return data

    def to_string(self) -> str:
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False)


class TokenStatus(Enum):
    INVALID = -1
    EXPIRED = 0
    VALID = 1


class Token(object):

    def __init__(self, access_token: str = None, refresh_token: str = None):
        self.access_token = access_token
        self.refresh_token= refresh_token

    def to_dict(self) -> Dict:
        data = {}
        if self.access_token is not None:
            data['access_token'] = self.access_token
        if self.refresh_token is not None:
            data['refresh_token'] = self.refresh_token
        return data

    def to_string(self) -> str:
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False)


    @staticmethod
    def generate_access_token(access_claims: AccessClaims, secret_key: str) -> str:
        access_dict = access_claims.to_dict()
        access_token = jwt.encode(access_dict, secret_key, algorithm='HS256')
        return access_token

    @staticmethod
    def parse_access_token(access_token: str, secret_key: str) -> AccessClaims:
        access_dict = jwt.decode(access_token, secret_key, algorithms='HS256')
        access_claims = AccessClaims()
        access_claims.from_dict(access_dict)
        return access_claims

    @staticmethod
    def generate_refresh_token(refresh_claims: RefreshClaims, secret_key: str) -> str:
        refresh_dict = refresh_claims.to_dict()
        refresh_token = jwt.encode(refresh_dict, secret_key, algorithm='HS256')
        return refresh_token

    @staticmethod
    def parse_refresh_token(refresh_token: str, secret_key: str) -> RefreshClaims:
        refresh_dict = jwt.decode(refresh_token, secret_key, algorithms='HS256')
        refresh_claims = RefreshClaims()
        refresh_claims.from_dict(refresh_dict)
        return refresh_claims
