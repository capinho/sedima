from orders.models import Order, OrderProduct, Payment
from django.contrib import admin
# from django.contrib.auth.models import User,Group,Permission
# from django.contrib.auth.admin import UserAdmin
import csv,xlwt
# from django import forms
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

# from import_export.admin import ImportExportModelAdmin
# from django.contrib.auth.hashers import make_password
# from import_export import resources, fields
# from import_export.widgets import ManyToManyWidget
from datetime import datetime
from django.http import HttpResponse
# import datetime
# from datetime import date

# from .models import *





# def export_commande(modeladmin, request, queryset):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="commandes.xls"'
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Commande',cell_overwrite_ok=True)

#     # Sheet header, first row
#     row_num = 0
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     columns = ['Numero Commande','Matricule','Nom','Prenom', 'Prix', 'Quantité', 'Produits','Categories']
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     # Sheet body, remaining rows
#     font_style = xlwt.XFStyle()

#     commandes = queryset.values_list('order','order__user__profile__matricule','order__user__first_name','order__user__last_name', 'price', 'quantity', 'product__name','product__category__name','order__user__profile__site')
#     for commande in commandes:
#         row_num += 1
#         for col_num in range(len(commande)):
#             ws.write(row_num, col_num, commande[col_num], font_style)
#     wb.save(response)
#     queryset.update(status='t')
#     return response

#     def get_paid(self, instance):
#         return instance.order.paid
# export_commande.short_description = 'Exporter vers excel'

# def export_commande_adv(modeladmin, request, queryset):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="commandes.xls"'
#     wb = xlwt.Workbook(encoding='utf-8')
#     todayDate = datetime.date.today()
#     current_day = todayDate.day
#     ws = wb.add_sheet('Commande',cell_overwrite_ok=True)

#     # Sheet header, first row
#     row_num = 0
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     columns = ['Matricule','Nom','Prenom','Quantité', 'Produits','Categories']
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     # Sheet body, remaining rows
#     font_style = xlwt.XFStyle()
#     commandes = queryset.values_list('order__user__profile__matricule','order__user__first_name','order__user__last_name','quantity', 'product__name','product__category__name')
#     for commande in commandes:
#         row_num += 1
#         for col_num in range(len(commande)):
#             ws.write(row_num, col_num, commande[col_num], font_style)
#     wb.save(response)
#     return response
# export_commande_adv.short_description = 'Exporter vers excel'

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     raw_id_fields = ['product']
#     extra = 0
#     actions = [export_commande,]


# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['id','product','price','quantity','get_nom','get_matricule','status']
#     list_filter = [('order__created', DateRangeFilter), ('order__updated', DateTimeRangeFilter),]

#     actions = [export_commande,export_commande_adv]
#     search_fields=['price','product__name','order__user__first_name','order__user__last_name','order__user__profile__matricule']
#     #list_display = ['id','price', 'quantity','user_id', 'product_id']
#     #list_filter = ['order__created', 'order__updated']

#     def get_actions(self, request):
#         group = Group.objects.filter(user=request.user,name='adv')
#         actions = super().get_actions(request)
#         if group:
#             if 'export_commande_adv' in actions:
#                 actions['export_commande_adv']
#                 del actions['export_commande']
#                 del actions['delete_selected']
#             return actions
#         else:
#             del actions['export_commande_adv']
#         return actions

#     def get_list_display(self, request):
#         group = Group.objects.filter(user=request.user,name='adv')
#         list_display = super().get_list_display(request)
#         if group:
#             list_display = ['id','product','quantity','get_nom','status']
#         return list_display



#     def has_add_permission(self, request):
#         return True

#     def get_nom(self, instance):
#         return '%s %s' % (instance.order.user.first_name,instance.order.user.last_name)

#     def get_matricule(self, instance):
#         return instance.order.user.profile.matricule

#     get_matricule.short_description = 'Matricule'
#     get_nom.short_description = 'Nom'



# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['Commande','get_nom','get_matricule']
#     list_filter = ['created',]
#     inlines = [OrderItemInline]
#     search_fields = ["user__username","user__profile__matricule","user__first_name","user__last_name"]
#     date_hierarchy = 'created'


#     def has_add_permission(self, request):
#         return False

#     def Commande (self,instance):
#         return instance.id

#     def get_matricule(self, instance):
#         return instance.order.user.profile.matricule

#     def get_nom(self, instance):
#         return '%s %s' % (instance.user.first_name,instance.user.last_name)
#     get_nom.short_description = 'Nom'

#     def get_matricule(self, instance):
#         return instance.user.profile.matricule
#     get_matricule.short_description = 'Matricule'





# admin.site.register(OrderItem, OrderItemAdmin)
# admin.site.register(Order,OrderAdmin)




def export_commande(modeladmin, request, queryset):
    now = datetime.now() # current date and time
    date_time = now.strftime("%m-%Y")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="commandes-%s.xls"' % (date_time)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Commande-%s' % (date_time),cell_overwrite_ok=True)

    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Numero Commande','Nom','Prenom', 'Prix', 'Quantité', 'Produits','Variations']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    commandes = queryset.values_list('order_number','orderproduct__user__first_name','orderproduct__user__last_name', 'orderproduct__product_price', 'orderproduct__quantity', 'orderproduct__product__name','orderproduct__variations__size__title')
    for commande in commandes:
        row_num += 1
        for col_num in range(len(commande)):
            ws.write(row_num, col_num, commande[col_num], font_style)
    wb.save(response)
    queryset.update(status='Traiter')
    return response

export_commande.short_description = 'Exporter vers excel'



class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order','full_name', 'product', 'quantity','product_price','get_variations']
    #list_filter = ['created_at','status','is_ordered']
    search_fields = ["order","user__first_name","user__last_name",'email']
    list_per_page = 20
    actions = [export_commande]



class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'quantity', 'product_price', 'ordered','variations')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name', 'order_total', 'status', 'is_ordered', 'created_at']
    list_filter = [('created_at', DateRangeFilter), ('updated_at', DateTimeRangeFilter),'status','is_ordered']
    search_fields = ['order_number','user__first_name','user__last_name','user__email']
    list_per_page = 20
    inlines = [OrderProductInline]
    actions = [export_commande]

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)

