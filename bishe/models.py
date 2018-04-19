# Create your models here.
from __future__ import unicode_literals

from datetime import datetime, date

from django.db import models
# 用户
from bisheproject.settings import MEDIA_ROOT


# class Session(models.Model):
#     session_id = models.CharField(max_length=50,default=0);
#     number = models.CharField(max_length=50,default="1111");
class user(models.Model):
    #时间作为id号
    user_id = models.CharField(u'用户id',max_length=50,unique=True,primary_key=True,editable=False)
    user_name = models.TextField(u'用户名',max_length=50,default="",editable=False)
    user_openid = models.CharField(u'用户openid',max_length=50,default="",editable=False)
    user_password = models.TextField(u'用户密码',max_length=50,default="",editable=False)
    user_phone = models.CharField(u'联系方式',max_length=50,default="")
    user_time = models.DateTimeField(u'注册时间', default=datetime.now(),editable=False)
    user_img = models.ImageField(u'头像',upload_to='userImage',default='userImage/default.png')
    user_Daddress = models.TextField(u'默认收货地址',blank=True)
    user_Dphone = models.IntegerField(u'收货电话',default=0)
    user_address = models.IntegerField(u'默认地址和电话',default=0)
    user_favourite = models.ManyToManyField('store',related_name="STORE2USER")
    def __str__(self):
        return self.user_name
#商店
def get_path(instance,filename):
    path = instance.store_registerId
    return 'storeImage/'+path+'/'+filename
class store(models.Model):
    #注册号
    store_id = models.CharField(u'商店id',max_length=50,unique=True,primary_key=True,editable=False)
    store_name = models.TextField(u'商店名',max_length=50,default="")
    store_openid = models.CharField(max_length=50,default="",blank=True)
    store_password = models.TextField(u'商店密码', max_length=50, default="", editable=False)
    store_registerId = models.CharField(u'社会信用号', max_length=50, default=0)
    store_registerName = models.CharField(u'注册名字', max_length=50, default="")
    store_address = models.TextField(u'商店地址',default="")
    store_date = models.TextField(u'商店成立时间', default="",editable=False)
    store_message = models.TextField(u'商店经营类型',default="")
    store_score = models.FloatField(u'商店分数',default=2.0)
    store_phone = models.CharField(u'商店联系方式',max_length=20,default="")
    store_time = models.DateTimeField(u'商店注册时间', default=datetime.now(),editable=False)
    store_cover = models.ImageField(u'头像', upload_to=get_path,default='storeImage/default.png')
    store_card_Ddiscount = models.FloatField(u'初始折扣', default=1)
    latitude = models.FloatField(u'经度', default=39.908775864608)
    longitude = models.FloatField(u'纬度', default=116.39759036591)
    cityid = models.FloatField(u'cityCode',default=110100)
    order_number = models.IntegerField(u'订单数量',default=0)
    store_card_Dlever = models.CharField(u'初始等级',max_length=50,default="")
    store_card_number = models.CharField(u'会员数量',max_length=50,default=0)
    store_card_prefix = models.CharField(u'会员卡前缀',max_length=50,default="")
    store_card_level = models.TextField(u'会员等级划分',default=0)
    store_card_discount = models.TextField(u'会员折扣划分', default=0)
    store_card_up_style = models.TextField(u'等级上升的标准',default=0)#人工或者通过积分
    store_card_message = models.TextField(u'会员卡说明',default="")
    store_card_date = models.TextField(u'有限期',default=0)#0表示无限期，用天数表示
    store_cardSetting = models.IntegerField(u'是否进行会员卡设置',default=0)
    store_img1 = models.ImageField(u'图片1', upload_to=get_path,default='storeImage/default.png')
    store_img2 = models.ImageField(u'图片2', upload_to=get_path,blank=True)
    store_img3 = models.ImageField(u'图片3', upload_to=get_path,blank=True)
    def __str__(self):
        return self.store_name
#商品
class goods(models.Model):
    #GOOD_store_goods_number
    goods_id = models.CharField(u'商品id',max_length=50,unique=True,primary_key=True,editable=False)
    # 每个商店对应多个商品
    goods_store=models.ForeignKey('store',on_delete=models.CASCADE,related_name="STORE2GOODS")
    goods_name = models.CharField(u'商品名称',max_length=50)
    goods_code = models.IntegerField(u'商品条形码',default=0)
    goods_message = models.TextField(u'商品信息',default="")
    goods_price = models.FloatField(u'商品价格',default=0.0)
    goods_score = models.FloatField(u'商品分数',default=2.0)
    goods_left = models.FloatField(u'剩余数量', default=0)
    goods_warn = models.FloatField(u'库存预警数量',default=0)
    goods_plan = models.FloatField(u'计划进货数量',default=0)
    goods_Allowsale = models.IntegerField(u'是否能销售',default=0)
    goods_Allowcard = models.IntegerField(u'是否能会员卡打折',default=0)
    goods_cardScore = models.FloatField(u'积分',default=0)
    goods_discount = models.FloatField(u'折扣价格',default=1.0)
    goods_number = models.FloatField(u'已购数量',default=0)
    store_registerId = models.CharField(u'社会信用号', max_length=50, default=0)
    goods_img1 = models.ImageField(u'图片1', upload_to=get_path,blank=True)
    goods_img2 = models.ImageField(u'图片2', upload_to=get_path,blank=True)
    goods_img3 = models.ImageField(u'图片3', upload_to=get_path,blank=True)
    goods_img4 = models.ImageField(u'图片4', upload_to=get_path,blank=True)
    goods_img5 = models.ImageField(u'图片5', upload_to=get_path,blank=True)
    def __str__(self):
        return self.goods_name

# 会员卡
class card(models.Model):
    #CARD_store_user_number
    card_id = models.CharField(u'会员id',max_length=50,unique=True,primary_key=True,editable=False)
    card_number = models.CharField(u'会员卡号',max_length=50,default=0,editable=False)
    #每个用户对应多张卡
    card_user = models.ForeignKey('user',on_delete=models.CASCADE,related_name="USER2CARD")
    #每个商店对应多张卡
    card_store=models.ForeignKey('store',on_delete=models.CASCADE,related_name="STORE2CARD")
    card_level = models.CharField(u'会员等级',max_length=50,default="")
    card_discount = models.FloatField(u'会员折扣',default=1)
    card_score = models.FloatField(u'会员卡积分',default=0 )

    def __str__(self):
        return self.card_id

# 交易表
class order(models.Model):
    order_id = models.CharField(u'订单号',max_length=50,unique=True,primary_key=True,editable=False)
    # 每个商店有多张订单
    order_store = models.ForeignKey('store',on_delete=models.CASCADE,related_name="STORE2ORDER")
    #每个用户有多张订单
    order_user = models.ForeignKey('user', on_delete=models.CASCADE, related_name="USER2ORDER",default="")
    order_goods = models.ManyToManyField('goods',related_name="GOODS2ORDER")
    order_discount = models.TextField(u'折扣',default="")
    order_number = models.TextField(u'数量',default="")
    order_allowCard = models.TextField(u'会员卡', default="")
    order_cardDiscount = models.FloatField(u'会员卡折扣', default=1)
    order_priceList = models.TextField(u'',default="")
    order_price = models.FloatField(u'成交价格',default=0.0)
    order_state = models.CharField(u'状态',max_length=50,default="提交")#0表示提交，表示成功，2表示关闭
    order_pay = models.CharField(u'支付方式',max_length=50,default="未支付")#0未支付，1现金，2移动支付
    order_time = models.DateTimeField(u'成交时间',default=datetime.now())
    def __str__(self):
        return self.order_id

class comment(models.Model):
    comment_id = models.CharField(u'编号',max_length=5,unique=True,primary_key=True,editable=False)
    comment_order = models.ForeignKey('goods',on_delete=models.CASCADE,related_name="GOODS2COMENT")
    comment_time = models.DateTimeField(u'评论时间')
    comment_score = models.FloatField(u'评分',default=0.0)
    comment_message = models.FloatField(u'评论内容',default=0.0)

class stock(models.Model):
    stock_id = models.CharField(u'入库单号',max_length=50,unique=True,primary_key=True,editable=False)
    stock_goods = models.ForeignKey('goods',on_delete=models.CASCADE,related_name="GOODS2STOCK")
    stock_price = models.FloatField(u'入库商品价格',default=0)
    stock_number = models.IntegerField(u'入库数量',default=0)
    stock_time = models.DateTimeField(u'入库日期',default=datetime.now())

