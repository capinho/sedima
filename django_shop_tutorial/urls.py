"""django_shop_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include,re_path,reverse_lazy

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth
from orders.views import *

from django.views.static import serve 


admin.site.site_header = 'Administration Commande Poulets et oeufs SEDIMA '

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('orders/', include('orders.urls')),

    re_path(r'^accounts/', include(('accounts.urls', 'accounst'), namespace='accounts')),
    re_path('', include(('shop.urls', 'shop'), namespace='shop')),

    #re_path(r'^', include('templated_email.urls', namespace='templated_email')),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
