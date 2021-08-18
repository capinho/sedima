from django.urls import path,re_path

from . import views
app_name='accounts'

urlpatterns = [
    path('login/',views.login,name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('', views.dashboard, name='dashboard'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

    path('change_password/', views.change_password, name='change_password'),
    path('order_detail/<int:pk>', views.order_detail, name='order_detail'),

]
