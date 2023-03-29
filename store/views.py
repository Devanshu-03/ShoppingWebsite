from django.shortcuts import get_object_or_404, render,redirect
from .models import Cart
from .models import CartItem
from .models import Product
from .models import Customer
from .models import OrderDetails
from django.views import View
from django.http import HttpResponse
from store.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password,check_password


# Create your views here.

class Index(View):
    def get(self,request):
        product = Product.objects.all()
        product_count = product.count()
        context = {
            'product':product,
            'product_count':product_count,
        }

        return render(request,'index.html',context)
    


class Store(View):
    @method_decorator(auth_middleware)
    def get(self,request):
        product = Product.objects.all()
        product_count = product.count()
        context = {
            'product':product,
            'product_count':product_count
        }
        return render(request,'store.html',context)
    
#searchbar 
  
class search(View):  
    @method_decorator(auth_middleware)
    def get(self,request):
        product = Product.objects.all()
        #print(prod)
        if request.method == 'GET':
            sh = request.GET.get('search')
            if sh != None:
                product = Product.objects.filter(name__icontains=sh)
                #print(prod)

        context = {
            'product':product,
        }
        return render(request,'index.html',context)
        

class Register(View):
    def post(self,request):
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        print(firstname)

        error_message = None

        if not (firstname):
            error_message = "firstname is required !!"
        
        elif len(firstname)<1:
            error_message = "firstname should be greater then 1 !!"
        
        elif len(lastname)<1:
            error_message = "lastname should be greater then 1 !!"
        
        elif len(email)<1:
            error_message = "email should be greater then 1 !!"

        elif len(password)<1:
            error_message = "password should be greater then 1"

        if not error_message:
            customer = Customer(firstname=firstname,lastname=lastname,email=email,password=password)
            customer.password = make_password(customer.password)
            customer.save()
            return redirect('index')
        else:
            return render(request,'register.html',{'error':error_message})



    def get(self,request):
        return render(request,'register.html')


class Login(View):
    def post(self,request):
        email = request.POST['email']
        print(email)
        password = request.POST['password']
        print(password)
        customer = Customer.get_customer_by_email(email)
        print(customer)
        error_message = None 
        if customer:
            flag = check_password(password,customer.password)

            if flag:
                request.session['customer'] = customer.id
                return redirect('index')
            else:
                error_message = "invalid email or password"
                return render(request,'signin.html',{'error':error_message})
        return render(request,'signin.html')

    def get(self,request):
        return render(request,'signin.html')
    

def Logout(request):
    request.session.clear()
    return redirect('index')
    


def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
        print(cart)
    return cart


def add_cart(request,product_id):
        #print(product_id)
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
        cart_id = cart_id(request)

    )
    cart.save()
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
    
        cart_item.save()
    return redirect('cart')

def remove_cart(request , product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request,product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')


 
class cart(View):
    @method_decorator(auth_middleware) 
    def get(self,request,total=0,quantity=0,cart_items=None):
        try:
            cart = Cart.objects.get(cart_id=cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total +tax 
        
        except:
            pass

        context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'tax':tax,
            'grand_total':grand_total,
        }
        return render(request,'cart.html',context)

class Placeorder(View):
    def post(self,request):
        country = request.POST['country']
        state = request.POST['state']
        street = request.POST['street']
        building =request.POST['building']
        houseno = request.POST['houseno']
        postalno = request.POST['postalno']
        zip = request.POST['zip']
        error_message = None 
        if not (country):
            error_message = "country name is required"
        elif len(state)<1:
            error_message = "state is required"
        
        elif len(street)<1:
            error_message = "street is required"
        elif len(houseno)<1:
            error_message = "house number is required"
        elif len(postalno)<1:
            error_message = "postal not is required"
        if not error_message:
            order = OrderDetails(country=country,state=state,street=street,building=building,houseno=houseno,postalno=postalno,zip=zip)
            order.save()
            return redirect('cart')
        else:
            return render(request,'placeorder.html',{'error':error_message})
        
    @method_decorator(auth_middleware)
    def get(self,request):
        return render(request,'placeorder.html')
        

    

