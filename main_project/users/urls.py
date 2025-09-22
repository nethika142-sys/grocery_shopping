from django.urls import path,re_path
from .import views

urlpatterns= [

    re_path('welcome', views.user_welcome, name='user_welcome'),

    re_path('getstarted', views.getstarted, name= 'user_getstarted'),

    re_path('loginpage', views.loginpage, name='loginpage'),

    re_path('loginview', views.loginview, name='user_login'),

    re_path('registerview', views.registerview, name='user_register'),

    re_path('base', views.base, name='base'),

    re_path('userhome', views.userhome, name='userhome'),

    re_path('shopnow', views.shopnow, name='shopnow'),

    re_path('^add_to_wishlist/(\d+)$', views.add_to_wishlist, name='addtowishlist'),

    re_path('wishlist_view', views.wishlist_view, name='wishlistview'),

    re_path('^removefromwishlist/(\d+)$', views.remove_from_wishlist, name='removefromwishlist'),

    re_path('^addtocart/(\d+)$', views.add_to_cart, name='addtocart'),

    re_path('cartview/', views.cart_view, name='cartview'),

    re_path('^removefromcart/(\d+)$', views.remove_from_cart, name='removefromcart'),

    re_path('profile', views.profile, name='profile'),

    re_path('aboutus', views.aboutus, name='aboutus'),

    re_path('categorypage', views.categorypage, name='categorypage'),

    re_path('^categoryproducts/(\d+)$', views.category, name='categoryproducts'),

    re_path('searchproduct/', views.search_product, name='searchproduct'),

    re_path('placeorder/', views.place_order, name='placeorder'),

    re_path('orderview/', views.order_view, name='orderview'),

    re_path('^cancelorder/(\d+)$', views.cancel_order, name='cancelorder'),

    re_path('userlogout', views.userlogout, name='userlogout'),

    
]