from django.shortcuts import render,get_object_or_404, redirect
from .models import*
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from .models import Register
from users.models import UserRegister
from django.db.models import Q

# Create your views here.


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
        if password != confirm_password:
            return render(request, 'owner/register.html', {'error': "passwords do not match"})
        Register.objects.create(name=name, email=email, password=password, phone=phone)
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

    context= { 
        'total_products': total_products,
        'total_users': total_users,
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
    return render(request, 'owner/orders.html')


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


      



        









        


    





       
    