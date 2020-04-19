from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from app01 import models

class LuffyAuth(BaseAuthentication):

    def authenticate(self, request):
        token = request.query_params.get('token')  #query_params方发是获取url中的params里面字典
        obj = models.UserToken.objects.filter(token=token).first()
        if not obj:
            raise AuthenticationFailed({'code':1001,'error':'认证失败'})
        return (obj.user.username,obj)