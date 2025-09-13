from django.contrib import admin
from .models import Category, Products, Register
from users.models import UserRegister



# Register your models here.

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'shop_name')
    search_fields = ('name', 'shop_name', 'place')
    list_filter = ('category', 'discount_percent')


@admin.register(UserRegister)
class UserRegisterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone')  
    search_fields = ('name', 'email', 'phone')      
    list_filter = ('email',)                          



