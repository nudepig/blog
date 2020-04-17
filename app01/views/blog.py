from rest_framework.views import APIView
from rest_framework.response import Response
from app01.auth.auth import LuffyAuth

class BlogView(APIView):
    authentication_classes = [LuffyAuth, ]
    def GET(seif,request,*args,**kwargs):

        ret = {"code": 1000, "error": "good"}
        return Response(ret)