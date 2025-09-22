from django.urls import re_path, path
from .import views

urlpatterns= [

    re_path('^$', views.landingpage, name='landingpage'),

    re_path('welcome', views.welcome, name='welcome'),

    re_path('signup', views.signup, name='signup'),

    re_path('register', views.register, name='register'),

    re_path('login', views.login, name= 'login'),

    re_path('header', views.header, name='header'),

    re_path('home', views.home, name='home'),

    re_path('viewproducts', views.viewproducts, name='viewproducts'),

    re_path('addproducts', views.addproducts, name= 'addproducts'),

    re_path('^editproducts(\d+)$', views.editproducts,name='editproducts'), 
    
    re_path ('updateproducts/(\d+)$', views.updateproducts,name='updateproducts'),

    re_path('^delproduct(\d+)$', views.delproduct, name='delproduct'),


    re_path('categories', views.categories, name='categories'),

    re_path('^category_products/(\d+)$', views.category_products, name='category_products'),

    re_path('^discounts', views.discounts, name='discounts'),

    re_path('^set_discount/(\d+)$', views.set_discount, name='set_discount'),

    re_path('^edit_price/(\d+)$', views.edit_price, name='edit_price'),

    re_path('orders', views.orders, name='orders'),

    re_path('^markcompleted/(\d+)$', views.mark_completed, name='markcompleted'),

    re_path('viewprofile', views.viewprofile, name='viewprofile'),

    re_path('productsearch', views.product_search, name='product_search'),

    re_path('logoutpage', views.logoutpage, name='logoutpage'),

    re_path('logout', views.logout, name='logout'),

   
   


    
]