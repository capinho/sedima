from django.urls import path, re_path,include
from . import task
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.site.site_header = 'Administration Commande Poulets et oeufs SEDIMA '

urlpatterns = [
        path('place_order/', views.place_order, name='place_order'),
        path('order_complete/', views.order_complete, name='order_complete'),


]
