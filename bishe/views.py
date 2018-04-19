from __future__ import unicode_literals

# import BeautifulSoup4
import base64
import random
import re
from _cffi_backend import buffer
from datetime import timezone, datetime
from math import radians, atan, tan, acos, sin, cos

from PIL import Image, ImageDraw, ImageFont
from barcode import Code39
from bs4 import BeautifulSoup
from django.core.serializers import json
from django.shortcuts import render, render_to_response, redirect
import urllib
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from io import BytesIO, StringIO

from bishe import models
from django.template import Context
import bcrypt

import barcode
from barcode.writer import ImageWriter
#生成条形码
def createbarcodebase64(request,str):
    imagewriter = ImageWriter()
    # 保存到图片中
    # add_checksum : Boolean   Add the checksum to code or not (default: True)
    ean = Code39(str, writer=imagewriter, add_checksum=False)
    # 不需要写后缀，ImageWriter初始化方法中默认self.format = 'PNG'
    ean.save('image2')
    img=open('image2.png', "rb").read()
    return HttpResponse(img,'image2.png')
#进制转换
def baseN(num, b):
    return ((num == 0) and "0") or (baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])
#生成验证码
def verify_code(request):
    print(request.Meta);
    print(request.COOKIES)
    # 1，定义变量，用于画面的背景色、宽、高
    # random.randrange(20, 100)意思是在20到100之间随机找一个数
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    # 2，创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 3，创建画笔对象
    draw = ImageDraw.Draw(im)
    # 4，调用画笔的point()函数绘制噪点，防止攻击
    for i in range(0, 100):
        # 噪点绘制的范围
        xy = (random.randrange(0, width), random.randrange(0, height))
        # 噪点的随机颜色
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        # 绘制出噪点
        draw.point(xy, fill=fill)
    # 5，定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 6，随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 7，构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.load_default().font
    # 8，构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 9，绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 9，用完画笔，释放画笔
    del draw
    # 10，存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    print(rand_str);
    # 11，内存文件操作
    buf = BytesIO()
    # 12，将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 13，将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
#url="http://gsxt.gdgs.gov.cn//GSpublicity/GSpublicityList.html?jumpid=rO0ABXQASntzZXJ2aWNlOmVudEluZm8sZW50Tm86N2IyZmJlNGUtMDE0ZC0xMDAwLWUwMTktMGVl%0D%0ANzBhMTEwMTE1LHJlZ09yZzo0NDA5MDF9%0D%0A"
def get_session(request):
    js_code = request.POST.get('js_code', None)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    url = "https://api.weixin.qq.com/sns/jscode2session?appid=wx84d665115047ddfe&secret=d3ce24a9b1a60346cf8a0cd2a1687e43&js_code="+js_code +"&grant_type=authorization_code";
    print(url);
    html = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(html)
    print(html)
    return HttpResponse(html)

#网页爬虫模块
def get_message(request):
        if request.method == "POST":
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            url = request.POST.get('url', None)
            html = urllib.request.Request(url=url,headers=headers)
            html = urllib.request.urlopen(html).read()
            soup= BeautifulSoup(html,"html.parser")
            content = soup.findAll('span',class_="content")
            #message = ""
            i = 0
            type = ""
            for item in content:
                if(i == 0):
                    message = message + item.text + ","#注册号/统一社会信用代码，唯一的
                if(i == 1):
                    message = message + item.text + ","#企业名称
                if(i == 2):
                    type = item.text#企业类型
                if(i == 5):
                    message = message + item.text + ","#注册时间
                if(type == "个体户"):
                    if(i == 9):
                        message = message + item.text + ","#地址
                    if (i == 10):
                        message = message + item.text #经营范围
                else:
                    if(i == 11):
                        message = message + item.text + ","  # 地址
                    if(i == 12):
                        message = message + item.text # 地址
                i = i+1
        return JsonResponse({'message':message} )
def index(respsonse):
    return HttpResponse(u"welcom")
#用户注册模块:
def user_register(request):
    # try:
        if request.method == "POST":
            #判断用户名是否被注册
            user_name = request.POST.get('user_name',None)
            print(user_name)
            # result = models.user.objects.filter(user_name=user_name)
            result = models.user.objects.extra(where=['binary user_name=%s'], params=[user_name])
            if(result.count() == 0):
                # 生成用户id
                time = datetime.now().strftime("%y%m%d%H%M%S%f")
                user_id = 'U'+ time
                user_openId = 'OPENID' + time
                # 通过bcrypt加密用户密码
                password = request.POST.get('user_password',None)
                password = password.encode("utf8")
                user_password = bcrypt.hashpw(password,bcrypt.gensalt(10))# 10轮的加密
                user_password=user_password.decode('utf-8')
                user_phone=request.POST.get('user_phone',None)
                user_img = request.FILES.get('user_img',None)
                #插入到数据库中
                if(user_img == None):
                    obj = models.user.objects.create(user_id=user_id, user_openId=user_openId,
                                                     user_name=user_name, user_password=user_password,
                                                     user_phone=user_phone)
                else:
                    obj = models.user.objects.create(user_id=user_id,user_openId=user_openId,user_img=user_img,
                     user_name=user_name,user_password=user_password,user_phone=user_phone)
                models.user.save(obj)
                return JsonResponse({'msg': 'ok'})
            else:
                return JsonResponse({'msg': 'duplicate'})
    # except:
    #     return JsonResponse({'msg': 'system_fail'})
#用户登录模块
def user_login(request):
    return render_to_response('user_login.html')
#判断是否登陆
def check_user_ifLogin(request):
    if request.session.get('user_login'):
        return JsonResponse({'msg': 'login'})
    else:
        return JsonResponse({'msg': 'unLogin'})
def user_login_check(request):
    # try:
        if request.method == "POST":
            # 获取用户输入的验证码
            vcode = request.POST.get('vcode')
            print(vcode)
            print(urllib.parse.quote(request.POST.get('name', None)))
            print(urllib.parse.unquote(request.POST.get('name', None)))
            # 获取session中的验证码
            vcode_session = request.session.get('verifycode')
            print(vcode_session)
            if(vcode != vcode_session):
                return JsonResponse({'msg': 'fail_verify'})
            #获取用户名
            name = request.POST.get('name', None)

            user = models.user.objects.filter(user_name=name)
            if(user.count() == 0):
                return JsonResponse({'msg': 'fail'})
            else:
                password = user[0].user_password
                password = password.encode("utf8")
                password1 = request.POST.get('password',None)
                password1 = password1.encode("utf8")
                password1 = bcrypt.hashpw(password1, password)
                if(password == password1):
                    request.session['user_login']=True
                    request.session['user_name']=name
                    return JsonResponse({'msg': 'ok_user'})
                else:
                    return JsonResponse({'msg': 'fail'})
    # except:
    #     return JsonResponse({'msg': 'system_fail'})
def user_home(request):
    if request.session.get('user_login'):
        name = request.session['user_name']
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        cityid = request.POST.get('cityid')
        store = models.store.objects.filter()
        store_list = []
        for item in store:
            if cityid == store.cityid:
                ra = 6378.140  # 赤道半径
                rb = 6356.755  # 极半径 （km）
                flatten = (ra - rb) / ra  # 地球偏率
                rad_lat_A = radians(latitude)
                rad_lng_A = radians(longitude)
                rad_lat_B = radians(item.latitude)
                rad_lng_B = radians(item.longitude)
                pA = atan(rb / ra * tan(rad_lat_A))
                pB = atan(rb / ra * tan(rad_lat_B))
                xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
                c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
                c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
                dr = flatten / 8 * (c1 - c2)
                distance = ra * (xx + dr)
                data = {"name":item.store_name,"distance":distance,"number":item.order_number,'score':item.store_score,'lat':item.latitude,'lng':item.longitude}
                store_list.append(data)
        return JsonResponse({'name':name,'store_list':store_list})
    else:
        return JsonResponse({'msg': 'unLogin'})
def store_show(request):
    if request.method == "POST":
        store_name = request.POST.get('store_name', None)
        store = models.store.objects.extra(where=['binary store_name=%s'], params=[store_name])
        if (store.count() == 0):
            return JsonResponse({'msg': 'fail'})
        Goods = store[0].STORE2GOODS.all()
        goods_list = []
        for i in Goods:
            if i.goods_Allowsale == 0:
                data = {'name':i.goods_name,'price':i.goods_price,'left':i.goods_left,'id':i.goods_id,'score':i.goods_score,'discount':i.goods_discount,
                        'number':i.goods_number,'Allowcard':i.goods_Allowcard,'cardScore':i.goods_cardScore,'message':i.goods_message}
                goods_list.append(data)
        return JsonResponse( {'goods_list':goods_list})
def user_user(request):
    if request.session.get('user_login'):
        name = request.session['user_name']
        user = models.user.objects.filter(user_name=name)
        user_message = {'name':user[0].user_name,'phone':user[0].user_phone}
        card_list = []
        Cards = user[0].USER2CARD.all()
        for item in Cards:
            data = {"number":item.card_number,'store':item.card_store.store_name,'level':item.card_level,'discount':item.card_discount,'score':item.card_score}
            card_list.append(data)
        return JsonResponse({'user_message':user_message,'card_list': card_list})

def user_order(request):
    if request.session.get('user_login'):
        name = request.session['user_name']
        user = models.user.objects.filter(user_name=name)
        order_list = []
        Order = user[0].USER2ORDER.all()
        for item in Order:
            goods = item.order_goods.all();
            goods_name = "";
            for i in goods:
                goods_name = goods_name + ',' + i.goods_name;
            goods_name = goods_name.split(',').pop(0);
            order_discount = item.order_discount.split(',').pop(0);
            order_number = item.order_number.split(',').pop(0);
            order_allowCard = item.order_allowCard.split(',').pop(0);
            order_priceList = item.order_priceList.split(',').pop(0);
            data = {
                'name':item.order_store.store_name,
                'id':item.oorder_id,
                'data':item.order_time,
                'price':item.order_price,
                'state':item.state,
                'pay':item.order_pay,
                'goods': goods_name,
                'discount': order_discount,
                'priceList':order_priceList,
                'number': order_number,
                'allowCard': order_allowCard,
                'cardDiscount':item.order_cardDiscount,
            };
            order_list.append(data)
        return JsonResponse({ 'name':name,'order_list': order_list})

def store_order(request):
    if request.session.get('store_login'):
        name = request.session['store_name']
        store = models.store.objects.filter(store_name=name)
        order_list = []
        Order = store[0].STORE2ORDER.all()
        for item in Order:
            goods = item.order_goods.all();
            goods_name = "";
            for i in goods:
                goods_name = goods_name + ',' + i.goods_name;
            goods_name = goods_name.split(',').pop(0);
            order_discount = item.order_discount.split(',').pop(0);
            order_number = item.order_number.split(',').pop(0);
            order_allowCard = item.order_allowCard.split(',').pop(0);
            order_priceList = item.order_priceList.split(',').pop(0);
            data = {
                'name': item.order_user.store_user,
                'id': item.order_id,
                'data': item.order_time,
                'price': item.order_price,
                'state': item.state,
                'pay': item.order_pay,
                'goods': goods_name,
                'discount': order_discount,
                'priceList': order_priceList,
                'number': order_number,
                'allowCard': order_allowCard,
                'cardDiscount': item.order_cardDiscount,
            };
            order_list.append(data)
        return JsonResponse({'name': name, 'order_list': order_list})
#商品分析
def store_goods(request):
    if request.session.get('store_login'):
        name = request.session['store_name']
        store = models.store.objects.filter(store_name=name)
        goods_number = []
        goods_left = []
        goods_name = []
        goods_id = []
        Order = store[0].STORE2ORDER.all()
        time = datetime.datetime.now()
        sum = 0;
        for item in Order:
            if time.month == item.order_time.number:
                order_number = item.order_number
                order_number = order_number.split(',').pop(0)
                goods = item.order_goods.all();
                TheIndex = 0;
                for i in goods:
                    currIndex = goods_id.index(i.goods_id)
                    Index = 0;
                    if currIndex == -1:
                        for ii in goods_number:
                            if ii < order_number[Index]:
                                break;
                            Index = Index + 1;
                        goods_id.insert(Index,i.goods_id);
                        goods_name.insert(Index,i.goods_name)
                        goods_number.insert(Index,order_number[Index])
                        goods_left.insert(Index,i.goods_left)
                    else:
                        goods_number[currIndex] = goods_number[currIndex]+order_number[TheIndex]
                    sum = sum + order_number[TheIndex];
                    TheIndex = TheIndex + 1;
        return JsonResponse({'goods_id': goods_id, 'goods_name': goods_name,
                               'goods_left':goods_left,'goods_number':goods_number,'sum':sum})

def store_count(request):
    if request.session.get('store_login'):
        name = request.session['store_name']
        store = models.store.objects.filter(store_name=name)
        time = datetime.datetime.now()
        expend = [0];
        income = [0];
        gain = [0];
        Order = store[0].STORE2ORDER.all()
        for item in Order:
            if time.year == item.order_time.year:
                month = time.month;
                income[month] = income[month]  + item.order_price
        Stock = store[0].GOODS2STOCK.all()
        for item in Stock:
            if time.year == item.stock_time.year:
                month = time.month;
                expend[month] = expend[month]  + item.stock_price*item.stock_number
        index = 0;
        for item in expend:
            gain[index] = income[index] - item;
        return JsonResponse({'expend':expend,'income':income,'gain':gain});
#商品列表
def goodsList_show(request):
    if request.session.get('store_login'):
        store_name = request.session['store_name']
        store = models.store.objects.extra(where=['binary store_name=%s'], params=[store_name])
        if (store.count() == 0):
            return JsonResponse({'msg': 'fail'})
        Goods = store[0].STORE2GOODS.all()
        goods_list = []
        for i in Goods:
            data = {'name': i.goods_name, 'price': i.goods_price, 'left': i.goods_left, 'id': i.goods_id,
                    'score': i.goods_score, 'discount': i.goods_discount,'warn':i.goods_warn,'plan':i.goods_plan,
                    'number': i.goods_number, 'Allowcard': i.goods_Allowcard, 'cardScore': i.goods_cardScore,
                    'message': i.goods_message}
            goods_list.append(data)
        return JsonResponse({'goods_list': goods_list})
#商品细节
def goodsDetail_show(request):
    if request.method == "POST":
        goods_id = request.POST.get('goods_id', None)
        goods = models.goods.objects.extra(where=['binary goods_id=%s'], params=[goods_id])
        if (goods.count() == 0):
            return JsonResponse({'msg': 'fail'})
        data = {'name': goods[0].goods_name, 'price': goods[0].goods_price, 'left': goods[0].goods_left, 'id': goods[0].goods_id,
                'score': goods[0].goods_score, 'discount': goods[0].goods_discount,
                'number': goods[0].goods_number, 'Allowcard': goods[0].goods_Allowcard, 'cardScore': goods[0].goods_cardScore,
                'message': goods[0].goods_message}
        return JsonResponse({'goods_detail': data})
def goodsStock_check(request):
    if request.method == "POST":
        goods_code = request.POST.get('goods_code', None)
        if request.session.get('store_login'):
            store_name = request.session['store_name']
            store = models.store.objects.extra(where=['binary store_name=%s'], params=[store_name])
            if (store.count() == 0):
                return JsonResponse({'msg': 'fail'})
            Goods = store[0].STORE2GOODS.all()
            goods_id = ""
            goods_name = ""
            for i in Goods:
                if(i.goods_code == goods_code):
                    goods_id = i.goods_id
                    goods_name = i.goods_name
            return JsonResponse({'goods_id': goods_id,'goods_name':goods_name})
# 商店注册模块
def store_register(request):
    # try:
        if request.method == "POST":
            store_name = request.POST.get('store_name', None)
            result = models.store.objects.extra(where=['binary store_name=%s'], params=[store_name])
            if (result.count() == 0):
                #id
                time = datetime.now().strftime("%y%m%d")
                store_registerId = request.POST.get('store_registerId', None)
                store_id = "ST" + time + store_registerId
                #密码
                password = request.POST.get('store_password',None)
                password = password.encode("utf8")
                store_password = bcrypt.hashpw(password,bcrypt.gensalt(10))# 10轮的加密
                store_password=store_password.decode('utf-8')
                #商店信息
                store_registerName = request.POST.get('store_registerName',None)
                store_address = request.POST.get('store_address',None)
                store_date = request.POST.get('store_date',None)
                store_message = request.POST.get('store_message',None)
                latitude = request.POST.get('latitude', None)
                longitude = request.POST.get('longitude', None)
                cityid = request.POST.get('cityid', None)
                store_phone = request.POST.get('store_phone',None)
                store_cover = request.FILES.get('store_cover',None)
                l = len(request.FILES.getlist('store_img',None))
                print(l)
                [store_img1, store_img2, store_img3] = ["","",""]
                if l == 1:
                   store_img1= request.FILES.getlist('store_img',None)
                if l == 2:
                    [store_img1, store_img2] = request.FILES.getlist('store_img', None)
                if l == 3:
                    [store_img1, store_img2, store_img3] = request.FILES.getlist('store_img', None)
                # 插入数据库中
                if store_cover == None:
                    obj = models.store.objects.create(store_id=store_id, store_password=store_password,
                                                      store_name=store_name,store_img1=store_img1,store_img2=store_img2,
                                                      store_img3=store_img3,store_registerId=store_registerId,
                                                      store_registerName=store_registerName,
                                                      latitude=latitude,longitude=longitude,cityid=cityid,
                                                      store_address=store_address, store_date=store_date,
                                                      store_message=store_message, store_phone=store_phone)
                else:
                    obj = models.store.objects.create(store_id=store_id,store_password=store_password,store_name=store_name,
                       store_registerId = store_registerId,store_registerName=store_registerName,store_cover=store_cover,
                       store_address=store_address,store_date=store_date,store_message=store_message,store_phone=store_phone,
                                                      latitude=latitude, longitude=longitude, cityid=cityid,
                       store_img1=store_img1,store_img2=store_img2,store_img3=store_img3)
                models.store.save(obj)
                # message = "注册成功，请进行会员卡设置"
                # return render_to_response('card_setting.html', {'message': message,'store_id':store_id})
                request.session['store_register'] = True
                request.session['store_register_name'] = store_name
                return JsonResponse({'msg': 'ok'})
            else:
                return JsonResponse({'msg': 'duplicate'})
    # except:
    #     return JsonResponse({'msg': 'system_fail'})
def check_store_ifLogin(request):
    if request.session.get('store_login'):
        return JsonResponse({'msg': 'login'})
    else:
        return JsonResponse({'msg': 'unLogin'})
#商店登录模块
def store_login(request):
    return render_to_response('store_login.html')
def store_login_check(request):
    try:
        if request.method == "POST":
            # 获取用户输入的验证码
            vcode = request.POST.get('vcode')
            # 获取session中的验证码
            vcode_session = request.session.get('verifycode')
            print(vcode + vcode_session)
            if(vcode != vcode_session):
                return JsonResponse({'msg': 'fail_verify'})
            #获取商店名
            name = request.POST.get('name', None)
            user = models.store.objects.filter(store_name=name)
            if(user.count() == 0):
                return JsonResponse({'msg': 'fail'})
            else:
                password = user[0].store_password
                password = password.encode("utf8")
                password1 = request.POST.get('password',None)
                password1 = password1.encode("utf8")
                password1 = bcrypt.hashpw(password1, password)
                if(password == password1):
                    request.session['store_login']=True
                    request.session['store_name']=name
                    return JsonResponse({'msg': 'ok'})
                else:
                    return JsonResponse({'msg': 'fail'})
    except:
        return JsonResponse({'msg': 'system_fail'})
def store_home(request):
    # try:
        if request.session.get('store_login'):
            name = request.session['store_name']
            store = models.store.objects.filter(store_name=name)
            goods_list = []
            Goods = store[0].STORE2GOODS.all()
            for item in Goods:
                warn=""
                if item.goods_left<item.goods_warn:
                    warn="库存不足"
                else:
                    warn="库存充足"

                img = [item.goods_img1, item.goods_img2, item.goods_img3
                       , item.goods_img4, item.goods_img5]
                data = {
                    'goods_name':item.goods_name,
                    'goods_price':item.goods_price,
                    'goods_left':item.goods_left,
                    'goods_plan':item.goods_plan,
                    'good_left':item.goods_left,
                    'goods_id':item.goods_id,
                    'warn':warn,
                    'goods_img':img,
                }
                goods_list.append(data)
            mstore = {
                'name':name,'cover':store[0].store_cover.url,
            }
            return JsonResponse({'mstore':mstore,'goods_list':goods_list})
        else:
            return JsonResponse({'msg': 'unLogin'})
    # except:
    #     return JsonResponse({'msg': 'system_fail'})
#商品入库模块
def goods_stock(request):
    try:
        if request.method == "POST":
            style = request.POST.get('style', None)
            if(style == "new"):
                #增加商品
                if request.session.get('store_login'):
                    store_name = request.session['store_name']
                    goods_name = request.POST.get('goods_name', None)
                    goods_message = request.POST.get('goods_message', None)
                    goods_price = request.POST.get('goods_price', None)
                    goods_warn = request.POST.get('goosd_warn', None)
                    goods_left = request.POST.get('goods_left', None)
                    goods_Allowsale = request.POST.get('goods_Allowsale', None)
                    goods_Allowcard = request.POST.get('goods_Allowcard', None)
                    goods_cardScore = request.POST.get('goods_cardScore', None)
                    goods_discount = request.POST.get('goods_discount', None)
                    goods_code = request.POST.get('goods_code', None)
                    if int(goods_warn)>int(goods_left):
                        goods_plan =int(goods_warn) - int(goods_left)
                    else:
                        goods_plan = 0
                    goods_store = models.store.objects.extra(where=['binary store_name=%s'], params=[store_name])
                    if(goods_store.count() == 0):
                        return JsonResponse({'msg': 'noStore'})
                    #id
                    goods_id ='G' + datetime.now().strftime("%y%m%d%H%M%S%f") + goods_store[0].store_registerId
                    #图片
                    l = len(request.FILES.getlist('goods_img', None))
                    [goods_img1, goods_img2, goods_img3,goods_img4,goods_img5] = ["", "", "","",""]
                    if l == 1:
                        goods_img1 = request.FILES.get('goods_img', None)
                    if l == 2:
                        [goods_img1, goods_img2] = request.FILES.getlist('goods_img', None)
                    if l == 3:
                        [goods_img1, goods_img2, goods_img3] = request.FILES.getlist('goods_img', None)
                    if l == 4:
                        [goods_img1, goods_img2, goods_img3,goods_img4] = request.FILES.getlist('goods_img', None)
                    if l == 5:
                        [goods_img1, goods_img2, goods_img3,goods_img4,goods_img5] = request.FILES.getlist('goods_img', None)
                    store_registerId = goods_store[0].store_registerId
                    #插入数据
                    obj_goods = models.goods.objects.create(goods_id=goods_id,
                                                      goods_store=goods_store[0],
                                                      goods_name=goods_name,
                                                      goods_message=goods_message,
                                                      goods_price=goods_price,
                                                      goods_left=goods_left,
                                                      goods_warn=goods_warn,goods_code=goods_code,
                                                      goods_plan=goods_plan,goods_Allowsale=goods_Allowsale,
                                                      store_registerId=store_registerId,goods_discount=goods_discount,
                                                      goods_Allowcard=goods_Allowcard,goods_cardScore=goods_cardScore,
                                                      goods_img1=goods_img1,
                                                      goods_img2=goods_img2,
                                                      goods_img3=goods_img3,
                                                      goods_img4=goods_img4,
                                                      goods_img5=goods_img5)
                    models.goods.save(obj_goods)
                    #商品入库
                    goods = models.goods.objects.extra(where=['binary goods_id=%s'], params=[goods_id])
                    if(goods.count() == 0):
                        return JsonResponse({'msg': 'noGoods'})
                    stock_id = "S" + datetime.now().strftime("%y%m%d%H%M%S%f") + store_registerId
                    stock_price = request.POST.get('stock_price', None)
                    obj_stock = models.stock.objects.create(stock_id=stock_id,stock_goods=goods[0],
                                                            stock_price=stock_price,stock_number=goods_left)
                    models.stock.save(obj_stock)
                    return JsonResponse({'msg': 'ok'})
            #入库
            else:
                goods_id =request.POST.get('goods_id', None)
                print(goods_id)
                stock_number = request.POST.get('stock_number', None)
                stock_price = request.POST.get('stock_price', None)
                goods = models.goods.objects.extra(where=['binary goods_id=%s'], params=[goods_id])
                print(goods)
                if (goods.count() == 0):
                    return JsonResponse({'msg': 'fail'})
                else:
                    store_id = goods[0].store_registerId
                    goods_warn = goods[0].goods_warn
                    goods_left = goods[0].goods_left
                    sum = int(goods_left)+int(stock_number)
                    if(int(goods_warn)>sum):
                        goods_plan = int(goods_warn)-sum
                    else:
                        goods_plan = 0
                    #订单号
                    stock_id = "S"+ datetime.now().strftime("%y%m%d%H%M%S%f")+store_id
                    obj = models.stock.objects.create(stock_id=stock_id,stock_goods=goods[0],
                                                      stock_price=stock_price,stock_number=stock_number)
                    obj.save()
                    models.goods.objects.filter(goods_id=goods_id).update(goods_left=str(sum),goods_plan=goods_plan)
                    return JsonResponse({'msg': 'ok'})
    except:
        return JsonResponse({'msg': 'system_fail'})

#会员卡设置
def card_setting(request):
    try:
        if request.method == "POST":
            store_card_prefix = request.POST.get('store_card_prefix', None)
            store_card_Ddiscount = request.POST.get('store_card_Ddiscount', None)
            store_card_Dlever = request.POST.get('store_card_Dlever', None)
            store_card_discount = request.POST.get('store_card_discount', None)
            store_card_level = request.POST.get('store_card_level', None)
            store_card_up_style = request.POST.get('store_card_up_style', None)
            store_card_date = request.POST.get('store_card_date', None)
            store_card_message = request.POST.get('store_card_message', None)
            if request.session.get('store_register'):
                name = request.session['store_register_name']
                models.store.objects.filter(store_name=name).update(
                    store_card_prefix=store_card_prefix, store_card_Ddiscount=float(store_card_Ddiscount),
                    store_card_Dlever=store_card_Dlever,store_card_discount=store_card_discount,
                    store_card_level=store_card_level,store_card_up_style=store_card_up_style,
                    store_card_date=store_card_date,store_card_message=store_card_message,store_cardSetting=1
                )
                return JsonResponse({'msg': 'ok'})
            elif request.session.get('store_login'):
                name = request.session['store_name']
                print(float(store_card_Ddiscount))
                models.store.objects.filter(store_name=name).update(
                    store_card_prefix=store_card_prefix,store_card_Ddiscount=float(store_card_Ddiscount),
                    store_card_Dlever=store_card_Dlever,store_card_discount=store_card_discount,
                    store_card_level=store_card_level,store_card_up_style=store_card_up_style,
                    store_card_date=store_card_date,store_card_message=store_card_message,store_cardSetting=1
                )
                return JsonResponse({'msg': 'ok'})
            else:
                return JsonResponse({'msg': 'fail'})
    except:
        return JsonResponse({'msg': 'system_fail'})
#会员卡发放
def card_register(request):
    try:
        if request.method == "POST":
            if request.session.get('user_login'):
                user_name = request.session['user_name']
                store_name = request.POST.get('store_name', None)
                store = models.store.objects.extra(where=['binary store_name=%s'], params=[store_name])
                user = models.user.objects.extra(where=['binary user_name=%s'], params=[user_name])
                print(user_name)
                print(user)
                if (store.count() == 0 or user.count() == 0 ):
                    return JsonResponse({'msg': 'fail'})
                card_list = []
                Cards = user[0].USER2CARD.all()
                for item in Cards:
                    if(item.card_store == store[0]):
                        return JsonResponse({'msg': 'duplicate'})
                store_card_number = store[0].store_card_number#数量
                store_card_prefix = store[0].store_card_prefix# 前缀
                card_number = store_card_prefix + datetime.now().strftime("%y%m%d")
                card_number = str(card_number) + str(store_card_number)
                card_id = datetime.now().strftime("%y%m%d")+store[0].store_registerId+store_card_number
                store_card_number = str(int(store_card_number)+1)
                store.update(store_card_number=store_card_number)
                card_discount = store[0].store_card_Ddiscount#初始折扣
                card_level = store[0].store_card_Dlever#初始等级
                obj = models.card.objects.create(card_id=card_id,card_number=card_number,
                                                 card_level = card_level,
                                                  card_discount=card_discount,card_user=user[0],
                                                  card_store=store[0])
                obj.save()
                return JsonResponse({'msg': 'ok'})
            else:
                return JsonResponse({'msg': 'unLogin'})
    except:
        return JsonResponse({'msg': 'system_fail'})

#商品购买
def buy_goods(request):
    try:
        if request.method == "POST":
            if request.session.get('user_login'):
                user_name = request.session['user_name']
                order_number = request.POST.get('order_number', None)
                order_price = request.POST.get('order_price', None)
                order_discount = request.POST.get('order_discount', None)
                order_cardDiscount = request.POST.get('order_cardDiscount', None)
                order_goods = request.POST.get('order_goods', None)
                order_allowCard = request.POST.get('order_allowCard', None)
                store_name = request.POST.get('store_name', None)
                store = models.store.objects.extra(where=['binary store_name=%s'], params=[store_name])
                user = models.user.objects.extra(where=['binary user_name=%s'], params=[user_name])
                if (store.count() == 0 or user.count() == 0):
                    return JsonResponse({'msg': 'fail'})
                obj = models.comment.objects.create(
                    order_user=user[0],order_store=store[0],order_number=order_number,order_allowCard=order_allowCard,
                    order_price = order_price,order_discount=order_discount,order_cardDiscount=order_cardDiscount,
                )
                obj.save()
                goods_list = order_goods.split(',');
                for item in goods_list:
                    if item != "":
                        goods = models.goods.objects.extra(where=['binary goods_id=%s'], params=[item])
                        obj.order_goods.add(goods[0]);
                return JsonResponse({'msg': 'ok'})
            else:
                return JsonResponse({'msg': 'unLogin'})
    except:
        return JsonResponse({'msg': 'system_fail'})
