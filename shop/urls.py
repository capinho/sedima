from django.urls import path,re_path

from . import views
from django.contrib import admin

admin.site.site_header = 'Administration SEDIMA NIOKOBOKK'

urlpatterns = [
    path('', views.product_list,
        name='product_list'),
    path('category/<slug:category_slug>/', views.product_list,name='product_list_by_category'),
    path('<slug:category_slugg>/<slug:product_slugg>/', views.product_detail, name='product_detail'),
    path('search',views.search,name='search'),
]
