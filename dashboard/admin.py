from django.contrib import admin
from .models import Product, Order

#Change Admin title header
admin.site.site_header = 'e-Inventory Dashboard'


#To display the product model in table style
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity')
    list_filter = ('category',)


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)