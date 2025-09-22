from django.shortcuts import render,get_object_or_404, redirect
from .models import*
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from .models import Register
from users.models import UserRegister
from users.models import Order
from django.db.models import Q

# Create your views here.

def landingpage(request):
    return render(request, 'owner/landingpage.html')


def welcome(request):
    return render(request, 'owner/welcomepage.html')

def signup(request):
    return render(request, 'owner/register.html')


def register(request):
    if request.method== 'POST':
        name= request.POST['name']
        email= request.POST['email']
        phone= request.POST['phone']
        password= request.POST['password']
        confirm_password= request.POST['confirmpassword']

        email_error = ""
        phone_error = ""
        password_error = ""

        if password!= confirm_password:
            password_error= "passwords do not match"

        if Register.objects.filter(email=email).exists():
            email_error= " This email is already registered"

        if Register.objects.filter(phone=phone).exists():
            phone_error= "This phone number has been registered"  

        if email_error or phone_error or password_error:
            return render(request, 'owner/register.html', { 'name': name, 'email':email, 'phone':phone, 'password':'', 'phone_error': phone_error, 'email_error':email_error, 'password_error': password_error })    

        Register.objects.create(name=name, email=email, phone=phone, password=password)
        return redirect('login')
    return render(request, 'owner/register.html')    


def login(request):
    if request.method== 'POST':
        email= request.POST['email']
        password= request.POST['password']
        
        try:
            user= Register.objects.get(email=email, password=password)
            request.session['user_id']= user.id
            return redirect('home')
        except Register.DoesNotExist:
            return render(request,'owner/login.html',{'error':'invalid credentials'})
    return render(request, 'owner/login.html')  


def header(request):
    return render(request, 'owner/header.html')

def home(request):
    total_products= Products.objects.count()
    total_users= UserRegister.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="Pending").count()  
   

    context= { 
        'total_products': total_products,
        'total_users': total_users,
        'total_orders': total_orders,
        'pending_orders': pending_orders
       
    }
    return render(request, 'owner/home.html', context)

def viewproducts(request):
    allproducts= Products.objects.all()
    return render(request, 'owner/products.html', {'products': allproducts})


def addproducts(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        place= request.POST['place']
        shopname= request.POST['shopname']
        image = request.FILES['imagefile']   
        category_id = request.POST['category']          # comes from dropdown

        product = Products(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            place= place,
            shop_name= shopname,
            image=image,                                # Django saves it into MEDIA_ROOT/products/
            category_id= category_id
        )
        product.save()
        return redirect('viewproducts')
    category = Category.objects.all()
    return render(request, 'owner/addproducts.html', {'category': category})

    


def editproducts(request, pid):
    product= Products.objects.get(id=pid)
    category= Category.objects.all()
    return render(request, 'owner/editproducts.html',{'product':product, 'category': category})
    


def updateproducts(request, pid):
    product= Products.objects.get(id=pid)
    if request.method=="POST":

         product.name= request.POST['name']
         product.description= request.POST['description']
         product.price= request.POST['price']
         product.quantity= request.POST['quantity']
         product.place= request.POST['place']
         product.shop_name= request.POST['shopname']

         category_id= request.POST['category']                  #update category
         product.category_id= category_id

         if 'imagefile' in request.FILES:
            product.image = request.FILES['imagefile']

   
         product.save()
         return redirect('viewproducts')
    
    category= Category.objects.all()
    return render(request, 'owner/editproducts.html', {'product': product, 'category': category})

    


def delproduct(request, pid):
    products= Products.objects.get(id=pid)
    products.delete()
    return redirect('viewproducts')
    



def categories(request):
    categories= Category.objects.all()
    return render(request, 'owner/categories.html',{'categories': categories})    


def category_products(request, cid):
    category= get_object_or_404(Category, id= cid)
    products= Products.objects.filter(category = category)
    return render(request, 'owner/category_products.html', {'products': products, 'category': category })


def discounts(request):
    products= Products.objects.all()
    return render(request, 'owner/discounts.html',{'products': products})

def set_discount(request, pid):
    product= get_object_or_404(Products, id=pid)

    if request.method== 'POST':
        discount= request.POST.get('discountpercent')
        if discount:
            product.discount_percent= discount
            product.save()
            return redirect('discounts')
    return render(request, 'owner/set_discount.html', {'product':product})


def edit_price(request, pid):
    product= get_object_or_404(Products, id=pid)

    if request.method == 'POST':
        newprice= request.POST.get('price')
        if newprice:
            product.price = newprice
            product.save()
            return redirect('discounts')
    return render(request, 'owner/edit_price.html',{ 'product': product})



def orders(request):
    orders = Order.objects.all().select_related('user', 'product')
    return render(request, 'owner/orders.html', {'orders': orders})


def mark_completed(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)
    
    # Only Pending orders can be marked Completed
    if order.status == 'Pending':
        order.status = 'Completed'
        order.save()
    
    return redirect('orders')


def viewprofile(request):
    user_id = request.session.get('user_id')
    if not user_id:   
        return redirect('login')

    user = Register.objects.get(id=user_id)
    return render(request, 'owner/viewprofile.html', {"user": user})


def product_search(request):
    query= request.GET.get('search')
    if query:
        products= Products.objects.filter(
            Q(name__icontains = query) |
            Q(description__icontains = query) |
            Q(price__icontains = query) |
            Q(quantity__icontains = query) |
            Q(discount_percent__icontains = query) |
            Q(category__name__icontains = query) 
        )
        return render(request, 'owner/searchresult.html',{'products': products, 'query':query})
    else:    
        return redirect('home')
    

def logoutpage(request):
    return render(request, 'owner/logoutpage.html')   


def logout(request):
    del request.session['user_id']
    return redirect('login')


      



        









        


    





       
    