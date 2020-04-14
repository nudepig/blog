from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib import auth
import logging
from app01 import forms
from app01.models import *
import requests
from django.db.models import F,Q
logger = logging.getLogger(__name__)
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid

class Account(APIView):
    def post(seif,request,*args,**kwargs):
            # 初始化一个给AJAX返回的数据
            ret = {"code": 1000, "error": ""}
            user = request.data.get("user")
            pwd = request.data.get("pwd")
            print(user)
            print(pwd)
            username_find = UserInfo.objects.filter(Q(username=user) | Q(email=user) | Q(phone=user)).first()
            user_name = auth.authenticate(username=username_find, password=pwd)
            if not user_name:
                ret['code'] = 1001
                ret['error'] = '账户或密码错误'
            else:
                user_tk = UserInfo.objects.get(username=user).id
                uid = str(uuid.uuid4())
                UserToken.objects.update_or_create(user=user_tk, defaults={'token': uid})
                ret['token'] = uid
            return Response(ret)
