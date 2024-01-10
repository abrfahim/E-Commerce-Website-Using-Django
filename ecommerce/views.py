from django.shortcuts import redirect, render
from firstapp.models import Slider, Banner_Area, MainCategory, Product, Category, Color, Brand, CouponCode
# Registration
from django.contrib.auth.models import User
# Login
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#ajax
from django.template.loader import render_to_string
from django.http import JsonResponse
# Maximum Minimum
from django.db.models import Max, Min, Sum

#django shopping cart
from cart.cart import Cart





def base(request):
    return render (request, 'base.html')
    

def home(request):
    sliders = Slider.objects.all().order_by('-id')[0:3]
    banners = Banner_Area.objects.all().order_by('-id')[0:3]
    mainCategories = MainCategory.objects.all()
    products = Product.objects.filter(section__name='Top Deals Of The Day')
    
    
    dict = {'sliders': sliders, 'banners':banners, 'mainCategories': mainCategories, 'products':products}
    return render (request, 'main/home.html', context=dict)

def product_details(request,slug):
    products = Product.objects.filter(slug=slug)
    if products.exists():
        products = Product.objects.get(slug=slug)
    else:
        return redirect('404')

        
    dict ={'products':products,}
    return render (request, 'product/product_detail.html', context=dict)

def error404(request):
    return render (request, 'error/404.html')


def account_details(request):
    dict={}
    return render (request, 'registration/login.html', context=dict)


def register_account(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request,'username is already exists!')
            return redirect('account_details')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,'email is already exists!')
            return redirect('account_details')
        
        
        user = User(
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()
        
        print(username, email, password)
    
    
    dict={}
    return redirect('account_details')


def login_account(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')
    
    # dict={}
    # return render (request, 'account/user_ac.html', context=dict )
    

@login_required(login_url='/accounts/login/')    
def user_profile(request):
    dict = {}
    return render (request, 'profile/user_profile.html', context=dict)



@login_required(login_url='/accounts/login/')    
def user_profile_update(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id
        
        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        
        if password != None and password !="":
            user.set_password(password)
        user.save()
        messages.success(request,'profile successfully updated!')
        return redirect('user_profile')
    

def about_us(request):
    dict = {}
    return render(request, 'main/about.html', context=dict)

def contact_us(request):
    dict = {}
    return render(request, 'main/contact.html', context=dict)

def product(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    colorID = request.GET.get('colorID') 
    FilterPrice = request.GET.get('FilterPrice')
    
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)
    elif colorID:
        product = Product.objects.filter(color = colorID)
    else:
        product = Product.objects.all()        
    
    
    dict = {
        'categories': categories, 
        'products': products,
        'min_price': min_price, 
        'max_price': max_price,
        'FilterPrice': FilterPrice,
        'color': color,
        'brand': brand,
    }
    
    return render(request, 'product/product.html', context=dict)



def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    brand = request.GET.getlist('brand[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()

    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})



#django shopping cart

@login_required(login_url='/accounts/login/')   
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url='/accounts/login/')   
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")

@login_required(login_url='/accounts/login/')   
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url='/accounts/login/')   
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url='/accounts/login/')   
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url='/accounts/login/')   
def cart_detail(request):
    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)
    delivery_cost = sum(i['delivery_cost'] for i in cart.values() if i)
    
    coupon = None
    valid_coupon = None
    invalid_coupon = None
    
    if request.method == 'GET':
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = CouponCode.objects.get(code=coupon_code)
                valid_coupon = 'Are Applicable on Current Offer!'
            except:
                invalid_coupon = 'Invalid coupon code!'
    
    dict = {
        'packing_cost': packing_cost,
        'tax': tax,
        'delivery_cost': delivery_cost,
        'coupon': coupon,
        'valid_coupon': valid_coupon,
        'invalid_coupon': invalid_coupon,
    }
    
    return render(request, 'cart/cart.html', context=dict)

@login_required(login_url='/accounts/login/')   
def checkout(request):
    # coupon_discount = None
    # if request.method == 'POST':
    #     coupon_discount = request.POST.get('coupon_discount')
    #     cart = request.session.get('cart')
        
    #     packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    #     tax = sum(i['tax'] for i in cart.values() if i)
        
    #     tax_and_packing_cost = (packing_cost + tax)
        
    #     dict = {
    #         'tax_and_packing_cost': tax_and_packing_cost,
    #         'coupon_discount': coupon_discount,
    #     }

    return render(request, 'checkout/checkout.html')