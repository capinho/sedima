from django.contrib import admin
from django import forms
from django.contrib.auth.models import User,Group,Permission

from .models import Category, Product,Size,ProductAttribute


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductVariantsInline(admin.TabularInline):
    model = ProductAttribute
    min_num = 2
    extra = 0
    show_change_link = True
    def has_change_permission(self, request, obj):
        return True
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_tag','name', 'price',
                    'available',]
    list_filter = ['available',]
    list_editable = ['available','price']
    prepopulated_fields = {'slug': ('name',)}
    search_fields=['name']
    inlines = [ProductVariantsInline,]

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['id','image_tag1','product','price', 'size','is_active']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['title']

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Size,SizeAdmin)
