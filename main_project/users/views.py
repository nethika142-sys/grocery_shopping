from django.shortcuts import render, redirect, get_object_or_404
from .models import*
from owner.models import Category, Products
from django.db.models import Q


# Create your views here.

def user_welcome(request):
    return render(request, 'users/welcome.html')

def getstarted(request):
    return render(request,'users/userregister.html')

def loginpage(request):
    return render(request, 'users/userlogin.html')

def  registerview(request):
    if request.method== 'POST':
        name= request.POST['name']
        email= request.POST['email']
        phone= request.POST['phone']
        password= request.POST['password']
        confirm_password= request.POST['confirmpassword']

        if password != confirm_password:
            return render(request, 'users/userregister.html', {'error':'passwords do not match'})
        UserRegister.objects.create(name=name, email= email, phone= phone, password= password)
        return redirect('loginpage')
    return render(request, 'users/useregister.html')



def loginview(request):
    if request.method== 'POST':
        email= request.POST['email']
        password= request.POST['password']

        try:
            users= UserRegister.objects.get(email=email, password= password)
            request.session['users_id']= users.id
            return redirect('userhome')
        except UserRegister.DoesNotExist:
            return render(request, 'users/userlogin.html',{'error': 'invalid credentials'})
    return render(request, 'users/userregister.html')    

def base(request):
    return render(request,'users/base.html')

def userhome(request):
    return render(request,'users/userhome.html')


def shopnow(request):
    products= Products.objects.all()
    return render(request,'users/shop.html',{'products': products})


def add_to_wishlist(request, product_id):
    user_id= request.session.get('users_id')
    if not user_id:
        return redirect("userslogin")
    user= get_object_or_404(UserRegister, id= user_id)
    product= get_object_or_404(Products, id= product_id)

    Wishlist.objects.get_or_create(user=user, product=product)
    return redirect('wishlistview')




def wishlist_view(request):
    user_id= request.session.get('users_id')
    if not user_id:
        return redirect("userslogin")
    user= get_object_or_404(UserRegister, id= user_id)
    wishlist_items= Wishlist.objects.filter(user= user)
    return render(request, 'users/wishlist.html', {'wishlistitems': wishlist_items})


def remove_from_wishlist(request, product_id):
    user_id= request.session.get('users_id')
    if not user_id:
        return redirect('userlogin')
    user = get_object_or_404(UserRegister, id=user_id)
    product = get_object_or_404(Products, id=product_id)
    Wishlist.objects.filter(user=user, product=product).delete()
    return redirect('wishlistview') 


def add_to_cart(request, product_id):
    user_id= request.session.get('users_id')
    if not user_id:
        return redirect('userslogin')
    user= get_object_or_404(UserRegister, id= user_id)
    product= get_object_or_404(Products, id= product_id)

    Cart.objects.get_or_create(user=user, product= product )
    return redirect('cartview')

def cart_view(request):
    user_id= request.session.get('users_id')
    if not user_id:
        return redirect('userslogin')
    user= get_object_or_404(UserRegister, id= user_id)
    cart_items= Cart.objects.filter(user=user)
    return render(request, 'users/cart.html', {'cartitems': cart_items})

def remove_from_cart(request, product_id):
    user_id= request.session.get('users_id')
    if not user_id:
        return redirect('userslogin')
    user= get_object_or_404(UserRegister, id= user_id)
    products= get_object_or_404(Products, id= product_id)
    Cart.objects.filter(user=user, product=products).delete()
    return redirect('cartview')

def profile(request):
    user_id= request.session.get('users_id')
    if not user_id:
        return redirect('userslogin')
    user= UserRegister.objects.get(id= user_id)
    return render(request, 'users/profile.html',{'user': user})


def categorypage(request):
    categories= Category.objects.all()
    return render (request, 'users/categorypage.html', {'categories': categories})

def category(request, cid):
    category_obj= get_object_or_404(Category, id=cid)
    products= Products.objects.filter(category= category_obj)
    return render(request, 'users/categoryproducts.html', {'products': products, 'category': category_obj})


def search_product(request):
    query= request.GET.get('search')
    discount= request.GET.get('discount')

    products= Products.objects.all()

    if query:
        products= products.filter(
            Q(name__icontains= query) |
            Q(description__icontains= query) |
            Q(category__name__icontains= query) |       
            Q(place__icontains= query) |
            Q(shop_name__icontains= query)
        )

    if discount:
        products= products.filter(discount_percent__gte= discount)

    return render(request, 'users/search.html', {'products': products, 'query': query, 'discount': discount})    

      




    

    

    






   











def aboutus(request):
    return render(request,'users/aboutus.html')













    
        





