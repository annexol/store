from django.contrib import admin
from .models import Product, Category, Basket, User, Ordered

# Register your models here.


admin.site.register(Category)
admin.site.register(Basket)
admin.site.register(User)
admin.site.register(Ordered)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    fields = ('image', 'name', 'description', 'price', 'stripe_product_price_id', 'category', 'is_published')
    # readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('name',)