# -*- codeing = utf -*-
# @Time : 2022/3/8 14:54
# @Author : 陈迪曙
# @File : authJWT.py
# @software : PyCharm
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, get_authorization_header, \
    jwt_decode_handler


class AuthToken(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        jwt_value = str(get_authorization_header(request), encoding='utf-8')
        if not jwt_value:
            raise AuthenticationFailed("Authorization  字段是必须的")
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('签名过期')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('非法用户')
        user = self.authenticate_credentials(payload)
        return user, jwt_value
