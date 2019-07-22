from django.db import models
from django.conf import settings

# Create your models here.

# 用户信息表
#主要有用户ID，用户名，用户电话，用户地址，用户积分信息

class UserInfo(models.Model):
   openid = models.CharField(max_length=20,unique=True)
   nickname=models.CharField(max_length=20,default='匿名')
   phonenumber=models.CharField(max_length=20,null=True)
   address=models.CharField(max_length=50,null=True)
   credits=models.IntegerField(default=0)
   def __str__(self):
                return self.nickname

#图片信息表，主要有用户ID，图片路径，图片时间，图片种类，垃圾识别种类
class ClassificationHistory(models.Model):

    userid=models.ForeignKey('UserInfo',to_field='openid',on_delete=models.CASCADE)
    image_md5= models.CharField(max_length=128)
    image_path=models.CharField(max_length=100)
    image_date=models.CharField(max_length=50)
    image_kind=models.CharField(max_length=20)
    image_type=models.CharField(max_length=20)

    #获取对象的md5
    @classmethod
    def getImageByMd5(cls,md5):
        try:
            return ClassificationHistory.objects.filter(image_md5=md5).first()
        except Exception as e:
            return None

    def getImageUrl(self):
        filename=self.file_md5+".jpg"
        url=settings.WEB_HOST_NAME+settings.WEB_IMAGE_SERVER_PATH+filename
        return url

    def getImagePath(self):
        filename=self.file_md5+".jpg"
        path=settings.IMAGE_SAVING_PATH +filename

    # def __str__(self):
    #     s = "filename:" + str(self.filename) + " - " + "filetype:" + str(self.file_type) \
    #     + " - " +  "filesize:" + str(self.file_size) + " - " + "filemd5:" + str(self.file_md5)
    #     return s
