from django.contrib import admin
from login.models import UserInfo
from login.models import ClassificationHistory
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('openid','nickname','phonenumber','address','credits')

class ClassAdmin(admin.ModelAdmin):
    list_display = ('userid_id','image_md5','image_path','image_date','image_kind','image_type')

admin.site.register(UserInfo,UserAdmin)
admin.site.register(ClassificationHistory,ClassAdmin)

