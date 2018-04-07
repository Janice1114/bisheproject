"""bisheproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from bishe.views import user_register, user_login, get_message, store_register, store_login, store_home, verify_code, \
   user_login_check, user_home, store_login_check, goods_stock, createbarcodebase64, card_register, card_setting, \
   buy_goods, index

urlpatterns = [
   #path('admin/', admin.site.urls),
   url(r'^',index),
   url(r'^admin/',admin.site.urls),

   url(r'^user_register/',user_register),
   url(r'^user_login/',user_login),
   url(r'user_login_check/',user_login_check),
   url(r'user_home/',user_home),

   url(r'^store_register/',store_register),
   url(r'^store_login/',store_login),
   url(r'^store_login_check/',store_login_check),
   url(r'^store_home/',store_home),

   url(r'^goods_stock/',goods_stock),
   #爬虫
   url(r'^get_message/',get_message),
   # 生产验证码图片url
   url(r'^verify_code/',verify_code),
   #生成条形码
   url(r'^createbarcodebase64/(\w+)',createbarcodebase64),
   #会员卡
   url(r'^card_register',card_register),
   #会员卡设置
   url(r'^card_setting',card_setting),
   #购买
   url(r'^buy_goods', buy_goods)

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)