from django.contrib import admin
from .models import Product,Category,Order,OrderProduct,PromotionEvent,ProductPromotionEvent,StockManagement

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(PromotionEvent)
admin.site.register(ProductPromotionEvent)
admin.site.register(StockManagement)
