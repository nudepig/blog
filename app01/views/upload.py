from django.shortcuts import render,redirect,HttpResponse
import time
import os
import logging
logger = logging.getLogger(__name__)
import json

def FileUploads(request):
    file = request.FILES.get('file')  # 获取文件对象，包括文件名文件大小和文件内容
    curttime = time.strftime("%Y%m%d")
    # 规定上传目录
    upload_url = os.path.join("upload")
    print(upload_url)
    # 判断文件夹是否存在
    folder = os.path.exists(upload_url)
    if not folder:
        os.makedirs(upload_url)
        print("创建文件夹")
    if file:
        file_size = int(file.size)
        print(file_size)
        file_name = file.name
        # 判断文件是是否重名，懒得写随机函数，重名了，文件名加时间
        if os.path.exists(os.path.join(upload_url ,file_name)):
            name, etx = os.path.splitext(file_name)
            addtime = time.strftime("%Y%m%d%H%M%S")
            finally_name = name + "_" + addtime + etx
            # print(name, etx, finally_name)
        else:
            finally_name = file.name
        # 文件分块上传
        upload_file_to = open(os.path.join(upload_url, finally_name), 'wb+')
        for chunk in file.chunks():
            upload_file_to.write(chunk)
        upload_file_to.close()
        # 返回文件的URl
        file_upload_url = "my_home/upload/" + 'attachment/' + curttime + '/' +finally_name
        # 构建返回值
        response_data = {}
        response_data['FileName'] = file_name
        response_data['FileUrl'] = file_upload_url
        response_json_data = json.dumps(response_data)  # 转化为Json格式
        print(response_json_data)
        return HttpResponse(response_json_data)
    return render(request, "upload2.html", locals())