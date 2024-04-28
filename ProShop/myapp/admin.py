from django.contrib import admin
from .models import Product, ProductM, OrderDetail

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name', 'price', 'description')
    list_editable = ('price', 'description')
    actions = ('make_zero',)

    def make_zero(self, request, queryset):
        queryset.update(price=0)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductM)
admin.site.register(OrderDetail)
