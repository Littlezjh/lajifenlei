# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def search_form(request):
    return render_to_response('search_form.html')

def search(request):
    request.encoding='utf-8'
    if 'q' in request.GET:
        message='你搜索的内容为：'+request.GET['q']
    else:
        message = '你提交了空表单'
    return HttpResponse(message)


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
        return  HttpResponse('OK')

def classificationImage(imagePath):
    print(os.path.getsize(imagePath)/1024)
    return '书','可回收垃圾'

def compress_image(infile,mb=150,step=10,quality=80):
    o_size=get_size(infile)
    if o_size<=mb:
        return infile
    outfile=get_outfile(infile)
    print('图片',outfile)
    while o_size>mb:
        im=Image.open(infile)
        im.save(outfile,quality=quality)
        if quality-step<0:
            break
        quality-=step
        o_size=get_size(outfile)
    return outfile

def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024

def get_outfile(infile):
    dir,name=os.path.split(infile)
    foredir=os.path.dirname(dir)
    outfile = os.path.join(os.path.join(foredir,'compressed_image'),name)
    return outfile