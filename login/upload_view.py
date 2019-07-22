from django.shortcuts import render
from django.shortcuts import HttpResponse
from login import models
import os,filetype,hashlib
from django.conf import settings
from django.http import FileResponse
from PIL import Image

from .models import UserInfo,ClassificationHistory
import urllib.request,json
from django.views.decorators.csrf import csrf_exempt
from .search import classificationImage,compress_image


@csrf_exempt
def postImage(request):
    result={}
    openid=request.POST.get('openid')
    photoTime=request.POST.get('photoTime')
    #检查是否为PSOT请求
    if request.method=='POST':
        myImage=request.FILES.get("imageFile",None)
        #检查是否有文件
        if myImage:
            md5 = pCalculateMd5(myImage)
            md5_1=md5+'.jpg'
            dir = os.path.join(os.path.join(settings.BASE_DIR,'static'),'profiles')
            imagePath=os.path.join(dir,md5_1)
            destination=open(imagePath,'wb+')
            for chunk in myImage.chunks():
                destination.write(chunk)
            destination.close()

            kind,thetype=classificationImage(imagePath)#获得图片识别结果
            comporessed_image = compress_image(imagePath)#压缩图片
            image=open(comporessed_image,'rb')

            #将状态信息和识别结果打包返回
            result['kind']=kind
            result['type']=thetype
            result['status'] = 'ok'
            id=UserInfo.objects.get(openid=openid)
            #将数据存入数据库
            ClassificationHistory.objects.create(
            userid=id,
            image_path=comporessed_image,
            image_date=photoTime,
            image_md5=md5,
            image_kind=kind,
            image_type=thetype,
            )
        else:
            result['status'] = 'no image found'

    else:
        result['status']='not a post'
    return  HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")

#读取最后上传图片的id
def load_history(request):
    result=[]
    openid=request.GET.get('openid')
    num=int(request.GET.get('num'))
    history=ClassificationHistory.objects.filter(userid=openid).order_by('-id')[:num]
    for i in history:
        temp={}
        temp['id']=i.id
        temp['imagePath']=i.image_md5+'.jpg'
        temp['kind']=i.image_kind
        temp['type']=i.image_type
        temp['time']=i.image_date
        temp['filePath']=''
        result.append(temp)
    return HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")

#供网页下载图片文件
def download_image(request):
    filename=request.GET.get('imagePath')
    dir=os.path.join(os.path.join(settings.BASE_DIR, 'static'), 'compressed_image')
    imagePath=os.path.join(dir,filename)
    file=open(imagePath,'rb')
    response=FileResponse(file)
    response['Content-Type']='image/jpeg'
    return  response




#计算文件的MD5
def pCalculateMd5(file):
    md5Obj=hashlib.md5()
    for chunk in file.chunks():
        md5Obj.update(chunk)
    # md5Obj.update(file.read())
    return md5Obj.hexdigest()