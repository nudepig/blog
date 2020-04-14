from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import auth
import time
import os
import logging
from app01 import forms
from django.views.decorators.csrf import csrf_exempt
from .models import *
import datetime
import requests  # 发post请求给对应接口
from django.db.models import F,Q
logger = logging.getLogger(__name__)
import json

def login(request):
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        valid_code = request.POST.get("valid_code")  # 获取用户填写的验证码
        print(valid_code)
        print("用户输入的验证码".center(120, "="))
        if valid_code and valid_code.upper() == request.session.get("valid_code", "").upper():
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            username_find = UserInfo.objects.filter(Q(username=username) | Q(email=username) | Q(phone=username)).first()
            user_name = auth.authenticate(username=username_find, password=pwd)
            if user_name:
                # 用户名密码正确
                # 给用户做登录
                auth.login(request, user_name)
                ret["msg"] = "/index/"
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)
    return render(request, "login.html")

def get_valid_img(request):
    from PIL import Image, ImageDraw, ImageFont
    import random

    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (220, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("static/bootstrap/fonts/kumo.ttf", 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((20+40*i, 0), tmp, fill=get_random_color(), font=font_obj)

    print("".join(tmp_list))
    print("生成的验证码".center(120, "="))
    # 不能保存到全局变量
    # global VALID_CODE
    # VALID_CODE = "".join(tmp_list)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    from io import BytesIO
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)

# 注册的视图函数
def register(request):
    if request.method == "POST":
        print(request.POST)
        print("=" * 120)
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        print(request.POST)
        # 帮我做校验
        if form_obj.is_valid():
            # 校验通过，去数据库创建一个新的用户
            form_obj.cleaned_data.pop("re_password")
            avatar_img = request.FILES.get("avatar")
            UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret["msg"] = "/login/"
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            print(ret)
            print("=" * 120)
            return JsonResponse(ret)
    # 生成一个form对象
    form_obj = forms.RegForm()
    print(form_obj.fields)
    return render(request, "register.html", {"form_obj": form_obj})

def forget_passwd(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        username = request.POST.get("username")
        anhao = request.POST.get("anhao")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        if len(password) < 6:
                ret["status"] = 1
                ret["msg"] = "设置密码必须6位及以上"
                return JsonResponse(ret)
        if re_password != password:
            ret["status"] = 1
            ret["msg"] = "两次密码输入不一致"
            return JsonResponse(ret)

        username_find = UserInfo.objects.filter(Q(username=username)|Q(email=username)|Q(phone=username)).first()
        if username_find:
            anhao_find = UserInfo.objects.filter(username=username_find).values("anhao").first().get("anhao", None)
            if anhao_find == anhao:
                user = UserInfo.objects.get(username=username_find)
                user.set_password(password)   #set_password django自带哈希算法更改密码
                user.save()
                ret["msg"] = "密码修改成功！"
                return JsonResponse(ret)
            else:
                ret["status"] = 1
                ret["msg"] = "暗号错误！"
                return JsonResponse(ret)
        else:
            ret["status"] = 1
            ret["msg"] = "账户不存在！"
            return JsonResponse(ret)
    return render(request, "forgetpasswd.html")




def contact(request):
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        data = {}
        # 从提交过来的数据中 取到用户名和密码
        text = request.POST.get("text")
        desp = request.POST.get("desp")
        print(text)
        print(desp)
        data["text"] = text
        data["desp"] = desp
        # 方糖网址
        url = "https://sc.ftqq.com/SCU73548T37a3cad051fd1af9b65f55a8fea2e0605e06020adb357.send"
        #headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        fangta = requests.post(url, data=data)
        try:
            import ast  # 字符串转换为字典，不像json只能是双引号才能转换
            result = ast.literal_eval(fangta.content.decode()).get("errmsg", None)
        except:
            result = None
        if result:
            ret["msg"] = result
            return JsonResponse(ret)
        else:
            ret["status"] = 1
            ret["msg"] = "消息发送失败，请重新发送！"
            return JsonResponse(ret)


    return render(request, 'contact.html')

@login_required
def index(request):
    date=datetime.datetime.now().date()
    book_date=request.GET.get("book_date",date)

    time_choices=Book.time_choices
    room_list=Room.objects.all()
    book_list=Book.objects.filter(date=book_date)


    htmls=""
    for room in room_list:
        htmls+="<tr><td>{}({})</td>".format(room.caption,room.num)

        for time_choice in time_choices:
            book=None
            flag=False
            for book in book_list:
                if book.room.pk==room.pk and book.time_id==time_choice[0]:
                    #意味这个单元格已被预定
                    flag=True
                    break

            if flag:
                if request.user.pk==book.user.pk:
                     htmls += "<td class='active item'  room_id={} time_id={}>{}</td>".format(room.pk, time_choice[0],book.user.username)
                else:
                     htmls += "<td class='another_active item'  room_id={} time_id={}>{}</td>".format(room.pk, time_choice[0],
                                                                                        book.user.username)
            else:
                 htmls+="<td room_id={} time_id={} class='item'></td>".format(room.pk,time_choice[0])

        htmls+="</tr>"
    return render(request,"index.html",locals())




def book(request):
    print(request.POST)
    post_data=json.loads(request.POST.get("post_data")) # {"ADD":{"1":["5"],"2":["5","6"]},"DEL":{"3":["9","10"]}}
    choose_date=request.POST.get("choose_date")

    res={"state":True,"msg":None}
    try:
        # 添加预定
        #post_data["ADD"] : {"1":["5"],"2":["5","6"]}

        book_list=[]
        for room_id,time_id_list in  post_data["ADD"].items():

            for time_id in time_id_list:
                book_obj=Book(user=request.user,room_id=room_id,time_id=time_id,date=choose_date)
                book_list.append(book_obj)

        Book.objects.bulk_create(book_list)


        # 删除预定
        from django.db.models import Q
        # post_data["DEL"]: {"2":["2","3"]}


        remove_book = Q()
        for room_id,time_id_list in post_data["DEL"].items():
            temp = Q()
            for time_id in time_id_list:
                temp.children.append(("room_id",room_id))
                temp.children.append(("time_id",time_id))
                temp.children.append(("user_id",request.user.pk))
                temp.children.append(("date",choose_date))
                remove_book.add(temp,"OR")
        if remove_book:
             Book.objects.filter(remove_book).delete()



    except Exception as e:
        res["state"]=False
        res["msg"]=str(e)

    return HttpResponse(json.dumps(res))


@login_required
@csrf_exempt
def FileUploads(request):
        file = request.FILES.get('file')  # 获取文件对象，包括文件名文件大小和文件内容
        curttime = time.strftime("%Y%m%d")
        #规定上传目录
        upload_url = os.path.join("upload")
        print(upload_url)
        #判断文件夹是否存在
        folder = os.path.exists(upload_url)
        if not folder:
            os.makedirs(upload_url)
            print("创建文件夹")
        if file:
            file_size = int(file.size)
            print(file_size)
            file_name = file.name
            #判断文件是是否重名，懒得写随机函数，重名了，文件名加时间
            if os.path.exists(os.path.join(upload_url,file_name)):
                name, etx = os.path.splitext(file_name)
                addtime = time.strftime("%Y%m%d%H%M%S")
                finally_name = name + "_" + addtime + etx
                #print(name, etx, finally_name)
            else:
                finally_name = file.name
            #文件分块上传
            upload_file_to = open(os.path.join(upload_url, finally_name), 'wb+')
            for chunk in file.chunks():
                upload_file_to.write(chunk)
            upload_file_to.close()
            #返回文件的URl
            file_upload_url = "my_home/upload/" + 'attachment/' + curttime + '/' +finally_name
            #构建返回值
            response_data = {}
            response_data['FileName'] = file_name
            response_data['FileUrl'] = file_upload_url
            response_json_data = json.dumps(response_data)#转化为Json格式
            print(response_json_data)
            return HttpResponse(response_json_data)
        return render(request, "upload2.html", locals())