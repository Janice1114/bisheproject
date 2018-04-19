from django.contrib import admin

# Register your models here.
from bishe import models

class userAdmin(admin.ModelAdmin):
    list_display = ('user_img','user_id','user_name','user_phone','user_time')

class storeAdmin(admin.ModelAdmin):
    list_display = ('store_cover','store_id','store_name','store_registerId','store_registerName'
                    ,'store_address','store_date','store_card_prefix','store_card_number'
                    ,'store_message','store_score','store_phone','store_time'
                    ,'store_card_prefix','store_card_Ddiscount','store_card_Dlever'
                    ,'store_img1','store_img2','store_img3')


class cardAdmin(admin.ModelAdmin):
    list_display = ('card_id','card_number','card_user','card_store','card_discount','card_score','card_level')
    def card_user(self,obj):
        return u'%s'%obj.card_user

class goodsAdmin(admin.ModelAdmin):
    list_display = ('goods_id','goods_name','goods_store','goods_message','goods_score','goods_Allowcard','goods_discount','goods_cardScore'
                    ,'goods_number','goods_left','goods_price','goods_warn','goods_plan','goods_Allowsale','goods_img1')

class orderAdmin(admin.ModelAdmin):
    list_display = ('order_id','order_store','get_goods','order_price','order_discount','order_time')

    def get_goods(self, obj):
        return "\n".join([p.order_goods for p in obj.order_goods.all()])
class commentAdmin(admin.ModelAdmin):
    list_display = ('comment_id','comment_order','comment_score','comment_message','comment_time')

class stockAdmin(admin.ModelAdmin):
    list_display = ('stock_id','stock_goods','stock_price','stock_number','stock_time')


admin.site.register(models.user,userAdmin)
admin.site.register(models.store,storeAdmin)
admin.site.register(models.card,cardAdmin)
admin.site.register(models.goods,goodsAdmin)
admin.site.register(models.order,orderAdmin)
admin.site.register(models.comment,commentAdmin)
admin.site.register(models.stock,stockAdmin)