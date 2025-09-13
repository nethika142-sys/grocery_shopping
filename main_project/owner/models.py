from django.db import models

# Create your models here.


class Register(models.Model):
    name= models.CharField(max_length=50)
    email= models.EmailField(unique=True)
    password= models.CharField(max_length=50)
    phone= models.CharField(max_length= 15)

    def __str__(self):
        return self.email
    


class Category(models.Model):
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.name 

    
class Products(models.Model):
    name= models.CharField(max_length=100)
    description= models.TextField(blank=True, null=True)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    quantity= models.PositiveIntegerField(default=1)
    image= models.ImageField(upload_to= 'products/')
    category= models.ForeignKey(Category, on_delete= models.CASCADE, null=True, blank= True)
    discount_percent= models.PositiveIntegerField(null= True, blank= True)
    place= models.CharField(max_length= 100, null=True, blank=True)
    shop_name= models.CharField(max_length=100, null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add= True,)
    updated_at= models.DateTimeField(auto_now= True)


    def __str__(self):
        return self.name
    
    


