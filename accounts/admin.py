from django.contrib import admin
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.admin import UserAdmin
import csv,xlwt

from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.hashers import make_password
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget


from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm

from shop.models import Category
# Register your models here.


class UserResource(resources.ModelResource):
    def before_import_row(self,row, **kwargs):
        value = row['password']
        row['password'] = make_password(value)
    class Meta:
        model = Account





class AccountAdmin(UserAdmin, ImportExportModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Account
    resource_class = UserResource

    list_display = ('email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)


    fieldsets = (
        (None, {'fields': ('email', 'password','first_name','last_name', 'last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_admin','is_superadmin','status')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    filter_horizontal = ()
    list_filter = ()




# class CustomUserAdmin(UserAdmin,ImportExportModelAdmin):
#        # list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_site')
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
#    # resource_class = UserResource
#     model = Account
#     # def get_site(self, instance):
#     #     return instance.profile.site
#     # get_site.short_description = 'Localisation'

#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)



admin.site.register(Account, AccountAdmin)
