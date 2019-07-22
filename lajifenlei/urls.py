"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views,search,upload_view
from django.conf.urls.static import static
from django.conf import  settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('search-form',search.search_form),
    path('search',search.search),
    path('upload',upload_view.postImage),
    path('login',views.login),
    path('load_history',upload_view.load_history),
    path('download',upload_view.download_image)
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)