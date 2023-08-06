import json
import time

from flask_auth_user.utils.token.Token import Token, AccessData, AccessClaims, RefreshData, RefreshClaims, TokenStatus


class TokenHelper(object):

    @staticmethod
    def generate(union_id: str, token_secret: str, access_timeout: int, refresh_timeout: int) -> Token:
        curr_time = int(time.time())

        access_issued_at = curr_time
        access_expires_at = curr_time + access_timeout
        access_data = AccessData(union_id=union_id, issued_at=access_issued_at, expires_at=access_expires_at)
        access_claims = AccessClaims(access_data=access_data)
        access_token = Token.generate_access_token(access_claims, token_secret)

        refresh_issued_at = curr_time
        refresh_expires_at = curr_time + refresh_timeout
        refresh_data = RefreshData(access_token=access_token, issued_at=refresh_issued_at,
                                   expires_at=refresh_expires_at)
        refresh_claims = RefreshClaims(refresh_data=refresh_data)
        refresh_token = Token.generate_refresh_token(refresh_claims, token_secret)

        token = Token(access_token=access_token, refresh_token=refresh_token)
        return token

    @staticmethod
    def parse_access_token(access_token: str, secret_key: str) -> AccessClaims:
        access_claims = Token.parse_access_token(access_token, secret_key)
        return access_claims

    @staticmethod
    def parse_refresh_token(refresh_token: str, secret_key: str) -> RefreshClaims:
        refresh_claims = Token.parse_refresh_token(refresh_token, secret_key)
        return refresh_claims

    @staticmethod
    def get_access_status(access_claims: AccessClaims, access_timeout: int, refresh_timeout: int) -> TokenStatus:
        curr_time = int(time.time())
        interval = refresh_timeout - access_timeout
        access_data = access_claims.access_data
        access_expires_at = access_data.expires_at
        refresh_expires_at = access_expires_at + interval

        token_status = TokenStatus.INVALID
        if access_expires_at >= curr_time:
            token_status = TokenStatus.VALID
        elif refresh_expires_at >= curr_time:
            token_status = TokenStatus.EXPIRED
        else:
            token_status = TokenStatus.INVALID
        return token_status

    @staticmethod
    def get_refresh_status(refresh_claims: RefreshClaims) -> TokenStatus:
        curr_time = int(time.time())
        refresh_data = refresh_claims.refresh_data
        refresh_expires_at = refresh_data.expires_at

        token_status = TokenStatus.INVALID
        if refresh_expires_at >= curr_time:
            token_status = TokenStatus.VALID
        return token_status


def test_generate_token(union_id: str, token_secret: str, access_timeout: int, refresh_timeout: int):
    token = TokenHelper.generate(union_id, token_secret, access_timeout, refresh_timeout)
    token_dict = token.to_dict()
    token_json = json.dumps(token_dict, ensure_ascii=False)
    print(token_json)


def test_parse_access_token(access_token: str, token_secret: str, access_timeout: int, refresh_timeout: int):
    access_claims = TokenHelper.parse_access_token(access_token, token_secret)
    access_data = access_claims.access_data
    union_id = access_data.union_id
    print(union_id)
    token = TokenHelper.generate(union_id, token_secret, access_timeout, refresh_timeout)
    token_dict = token.to_dict()
    token_json = json.dumps(token_dict, ensure_ascii=False)
    print(token_json)


def test_parse_refresh_token(refresh_token: str, token_secret: str, access_timeout: int, refresh_timeout: int):
    refresh_claims = TokenHelper.parse_refresh_token(refresh_token, token_secret)
    refresh_data = refresh_claims.refresh_data
    access_token = refresh_data.access_token
    access_claims = TokenHelper.parse_access_token(access_token, token_secret)
    access_data = access_claims.access_data
    union_id = access_data.union_id
    token = TokenHelper.generate(union_id, token_secret, access_timeout, refresh_timeout)
    token_dict = token.to_dict()
    token_json = json.dumps(token_dict, ensure_ascii=False)
    print(token_json)


def main():
    union_id = 'o9h-Mjj4pzCq_7gFECYL0DPTsYtM'
    token_secret = '243223ffslsfsldfl412fdsfsdf'
    access_timeout = 60 * 60 * 24
    refresh_timeout = 60 * 60 * 24 * 7
    test_generate_token(union_id, token_secret, access_timeout, refresh_timeout)

    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InVuaW9uX2lkIjoibzloLU1qajRwekNxXzdnRkVDWUwwRFBUc1l0TSIsImlzc3VlZF9hdCI6MTYyMzcyNzUyMiwiZXhwaXJlc19hdCI6MTYyMzgxMzkyMn19.NLRd02WbtQqVX11_FvFlNT5GKP5BbmQWFfKFy51XpWM'
    test_parse_access_token(access_token, token_secret, access_timeout, refresh_timeout)

    refresh_token = '''eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7ImFjY2Vzc190b2tlbiI6ImV5SjBlWEFpT2lKS1YxUWlMQ0poYkdjaU9pSklVekkxTmlKOS5leUprWVhSaElqcDdJblZ1YVc5dVgybGtJam9pTVRJek5EVTJOemc1SWl3aWFYTnpkV1ZrWDJGMElqb3hOakl3TmpFNE1ERTFMQ0psZUhCcGNtVnpYMkYwSWpveE5qSXdOakU0TURFMmZYMC5xdldueFl1Ym45eUVJbzhISlF2T3ZzNE9ETFJfRHJ4OFBRWl8wZjR3NThJIiwiaXNzdWVkX2F0IjoxNjIwNjE4MDE1LCJleHBpcmVzX2F0IjoxNjIwNjE4MDE3fX0.N9G88z6I7FVgSAdRzNI0gkr0kDPlGlxAlmC-AIttBfY'''
    test_parse_refresh_token(refresh_token, token_secret, access_timeout, refresh_timeout)


if __name__ == '__main__':
    main()
