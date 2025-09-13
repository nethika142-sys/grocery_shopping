from django.db import models
from owner.models import Products
# Create your models here.


class UserRegister(models.Model):
    name= models.CharField(max_length=50)
    email= models.EmailField(unique= True)
    phone= models. CharField(max_length= 15)
    password= models. CharField(max_length= 50)

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user= models.ForeignKey(UserRegister, on_delete= models.CASCADE)
    product= models.ForeignKey(Products, on_delete= models.CASCADE)
    added_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist: {self.user.name} - {self.product.name}"

class Cart(models.Model):
    user= models.ForeignKey(UserRegister, on_delete= models.CASCADE)
    product= models.ForeignKey(Products, on_delete= models.CASCADE)
    quantity= models.PositiveIntegerField(default=1)
    added_at= models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f"Cart: {self.user.name} - {self.product.name} (x{self.quantity})"



class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Override save() so total_price is always product.price * quantity.
        """
        if self.product and self.quantity:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} by {self.user.name} - {self.product.name}"
