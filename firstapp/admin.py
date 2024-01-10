from django.contrib import admin
from .models import Slider, Banner_Area, Category, MainCategory, SubCategory, AdditionalInformation, Product, ProductImage,Section, Color, Brand, CouponCode
# Register your models here.

class ProductImages(admin.TabularInline):
    model = ProductImage
    
class AdditionalInformations(admin.TabularInline):
    model = AdditionalInformation

class Product_Admin(admin.ModelAdmin):
    inlines = (ProductImages, AdditionalInformations)
    list_display = ('product_name', 'price','categories','section', 'tax', 'packing_cost', 'delivery_cost')
    list_editable = ('categories', 'section','tax', 'packing_cost', 'delivery_cost')


admin.site.register(Slider)
admin.site.register(Banner_Area)
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Section)
admin.site.register(Product, Product_Admin)
admin.site.register(ProductImage)
admin.site.register(AdditionalInformation)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(CouponCode)