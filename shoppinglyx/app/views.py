from django.shortcuts import render, redirect
# View Import a Kela Karan Class Based Function Banavaych Aahe. 
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q 
from django.http import JsonResponse

  
class ProductView(View):
    def get(self, request):
     topwears = Product.objects.filter(category='TW')
     bottomwears = Product.objects.filter(category='BW')
     mobiles = Product.objects.filter(category='M')
     laptops = Product.objects.filter(category='L')

     return render(request, 'app/home.html',{'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops})
 
 
class ProductDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/productdetail.html', {'product':product})

def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70
    total_amount = 0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    # print(cart_product)
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
      return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount': totalamount, 'amount':amount})
    else:
     return render(request, 'app/emptycart.html')


def plus_cart(request):
  if request.method == 'GET':
   prod_id = request.GET['prod_id']
   c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
   c.quantity+=1
   c.save()
   amount = 0.0
   shipping_amount = 70.0
   cart_product = [p for p in Cart.objects.all() if p.user == request.user]
   for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

      data = {
        'quantity': c.quantity,
        'amount': amount,
        'totalamount': amount + shipping_amount
      }  
   return JsonResponse(data)
  
def minus_cart(request):
  if request.method == 'GET':
   prod_id = request.GET['prod_id']
   c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
   c.quantity-=1
   c.save()
   amount = 0.0
   shipping_amount = 70.0
   cart_product = [p for p in Cart.objects.all() if p.user == request.user]
   for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

      data = {
        'quantity': c.quantity,
        'amount': amount,
        'totalamount': amount + shipping_amount
      }  
   return JsonResponse(data)
  
def remove_cart(request):
  if request.method == 'GET':
   prod_id = request.GET['prod_id']
   c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
   c.delete()
   amount = 0.0
   shipping_amount = 70.0
   cart_product = [p for p in Cart.objects.all() if p.user == request.user]
   for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount


      data = {
        'amount': amount,
        'totalamount': amount + shipping_amount
      }  
   return JsonResponse(data)


 

def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'order_placed':op})



def topwear(request, data=None):
 if data == None:
  topwears = Product.objects.filter(category='TW')
 elif data == 'Raymond' or data == 'Adidas' or data == 'Parkavenue' or data == 'Blackberrys':
  topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=400)
 elif data == 'above':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=400)
 return render(request, 'app/topwear.html', {'topwears':topwears})

def bottomwear(request, data=None):
 if data == None:
  bottomwears = Product.objects.filter(category='BW')
 elif data == 'Levis' or data == 'Lee' or data == 'Diesel' or data == 'Spykar':
  bottomwears = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=600)
 elif data == 'above':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=600)
 return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears})


def mobile(request, data=None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'Vivo' or data == 'Samsung' or data == 'Oppo':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
   mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=15000)
 elif data == 'above':
   mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=15000)
 return render(request, 'app/mobile.html', {'mobiles':mobiles})


def laptop(request, data=None):
 if data == None:
  laptops = Product.objects.filter(category='L')
 elif data == 'Lenovo' or data == 'Dell' or data == 'Asus' or data == 'Acer':
  laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'below':
  laptops = Product.objects.filter(category='L').filter(discounted_price__lt=40000)
 elif data == 'above':
  laptops = Product.objects.filter(category='L').filter(discounted_price__gt=40000)
 return render(request, 'app/laptop.html', {'laptops':laptops})



def login(request):
 return render(request, 'app/login.html')

 
class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':form})
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully')
   form.save()
  return render(request, 'app/customerregistration.html', {'form':form})
 


def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0
 totalamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
  totalamount = amount + shipping_amount  

 return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})


def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
  c.delete()
 return redirect("orders") 

class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form':form, 'active':' btn-primary'})
 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
   reg.save()
   messages.success(request, 'Congratulations!! Profile Updated Successfully')
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'}) 
 

def search(request):
 query = request.GET['query']
 allPosts = Product.objects.filter(title__contains=query)
#  params = {'allPosts': allPosts}
 return render(request, 'app/search.html', {'allPosts': allPosts})



