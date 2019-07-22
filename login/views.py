from django.shortcuts import render
from django.shortcuts import HttpResponse
from login import models
import os,filetype,hashlib
from django.conf import settings
from .models import UserInfo,ClassificationHistory
import urllib.request,json
from django.views.decorators.csrf import csrf_exempt
from .search import classificationImage,compress_image
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

# Create your views here.

user_list=[]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    print(settings.APPSECRET)
    # if request.method =='POST':
    #     username = request.POST.get('username')
    #     password=request.POST.get('password')
    #     myImage = request.FILES.get("imageFile", None)
    #     print(request.FILES)
    #     if myImage:
    #         dir = os.path.join(os.path.join(BASE_DIR,'static'),'profiles')
    #         destination=open(os.path.join(dir,myImage.name),'wb+')
    #         for chunk in myImage.chunks():
    #             destination.write(chunk)
    #         destination.close()
    #     models.UserInfo.objects.create(user=username,pwd=password)
    # user_list=models.UserInfo.objects.all()
    # # return render(request,'index.html',{'data':user_list})
    return render(request,'index.html',{'data':user_list})



def upload(request):
    if request.method=='POST':
        myImage=request.FILES.get("imageFile",None)
        if myImage:
            dir = os.path.join(os.path.join(BASE_DIR,'static'),'profiles')
            destination=open(os.path.join(dir,myImage.name),'wb+')
            for chunk in myImage.chunks():
                destination.write(chunk)
            destination.close()
            return HttpResponse('OK')
        else:
            return HttpResponse('Not OK!')
    else:
        return HttpResponse('OK')

def login(request):
    code=request.GET.get('code')
    name=request.GET.get('name')
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (settings.WEIXIN_APP_ID,settings.WEIXIN_APP_SECRET,code)
    response=urllib.request.urlopen(url)
    result=json.loads(response.read().decode('utf-8'))
    print(result)
    openid=result.get('openid')
    if openid:
        users=UserInfo.objects.filter(openid = openid)
        if not users:
            user=UserInfo(openid = openid,nickname=name)
            user.save()
    else:
        openid='none'
    return HttpResponse(openid)

def returnBase(message="", code=1, status=400):
    data = {
        "err_code": code,
        "message":message
    }
    return JsonResponse(data, status=status)

def returnNotFound(message, code=1):
    return  returnBase(message, code)

def returnOk(data=None):
    if not data:
        data = {}
    return JsonResponse(data=data, status=200)

def returnBadRequest(message, code=1):
    return returnBase(message, code)

def returnForbidden(message, code=1):
    return returnBase(message, code, status=403)

def returnRedirect(location):
    return HttpResponseRedirect(location)

# 检查参数
def checkPara(dataMap, keyList):
    if not isinstance(dataMap, dict) or not isinstance(keyList, list):
        return False

    result = [True]
    for k in keyList:
        if k not in dataMap:
            if result[0] == True:
                result[0] = "Need para: " + k
            value = None
        else:
            value = dataMap[k]
        result.append(value)

    return tuple(result)

