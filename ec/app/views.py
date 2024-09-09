from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.views import View
import razorpay
from django.conf import settings
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())

# @login_required
def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/about.html",locals())

# @login_required
def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/contact.html",locals())

# @method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product=Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())

# @method_decorator(login_required, name='dispatch')    
class CategoryTitle(View):
    def get(self,request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

# @method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        totalitem = 0
        wishitem = 0
        wishlist = []

        # Check if user is authenticated
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            wishitem = Wishlist.objects.filter(user=request.user).count()
            product = get_object_or_404(Product, pk=pk)
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        else:
            product = get_object_or_404(Product, pk=pk)

        return render(request,"app/productdetail.html",locals())
    
# @method_decorator(login_required, name='dispatch')
class CustomerRegView(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        return render(request, 'app/customerreg.html', locals())
    
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User registered successfully")
            # return render(request,"app/home.html")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/customerreg.html', locals())

@method_decorator(login_required, name='dispatch')   
class ProfileView(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            phone_number=form.cleaned_data['phone_number']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,phone_number=phone_number,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congrates! Profile saved successfully")
        else:
            messages.warning(request,"Invalid input data")

        return render(request, 'app/profile.html',locals())

@login_required
def address(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    states = dict(Customer._meta.get_field('state').choices)#not working for states name to render in address page
    add = Customer.objects.filter(user=request.user)
    context = {
        'add': add,
        'states': states,
        'totalitem' : totalitem,
    }
    return render(request,'app/address.html',context)

@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        customer = get_object_or_404(Customer, pk=pk, user=request.user)
        form = CustomerProfileForm(instance=customer) 
        return render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        customer = get_object_or_404(Customer, pk=pk, user=request.user)
        form=CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request,"Congrats ! Successfull update")
        else:
            messages.warning(request,"Invalid input data")
        return redirect('address')

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)

    # Check if the product is already in the cart
    if Cart.objects.filter(user=user, product=product).exists():
        messages.info(request, "This product is already in your cart.")
    else:
        Cart(user=user, product=product).save()
        messages.success(request, "Product added to your cart successfully!")

    return redirect('/cart')

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value=p.quantity * p.product.discounted_price
        amount = amount +value
    totalamount = amount + 40 
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))   
    return render(request,'app/addtocart.html',locals())

@login_required
def wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))   
    return render(request,'app/wishlist.html',locals())

def plus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart =Cart.objects.filter(user=user)
        amount =0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount = amount+40
        # print(prod_id)
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        if c.quantity == 0:
            c.delete()  # Delete the cart item
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount += value
            totalamount = amount + 40
            data = {
                'quantity': 0,  # Indicate the item is removed
                'amount': amount,
                'totalamount': totalamount,
                'remove': True  # Add a flag to indicate the item is removed
            }
            return JsonResponse(data)
        
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
            'remove': False  # Item not removed, just updated
        }
        return JsonResponse(data)

    
def remove_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart =Cart.objects.filter(user=user)
        amount =0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount = amount+40
        # print(prod_id)
        data = {
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def plus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data = {
            'message' : 'Product added successfully into Wishlist'
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data = {
            'message' : 'Product removed successfully from Wishlist'
        }
        return JsonResponse(data)

@method_decorator(login_required, name='dispatch')    
class checkout(View):
    def get(self,request,prod_id=None):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add = Customer.objects.filter(user=user)
        if not add.exists():
            messages.error(request, "Please select an address before proceeding to payment.")
            return redirect('checkout') 

        cart_items = []
        famount = 0
        prod_id = request.GET.get('prod_id')
        print(f"Received prod_id: {prod_id}")

        if prod_id:
            # If a product ID is provided, only include that product
            product = Product.objects.get(id=prod_id)
            cart_items.append({'product': product, 'quantity': 1})
            famount = product.discounted_price
        else:
            # Otherwise, proceed with the user's full cart
            cart_items = Cart.objects.filter(user=user)
            for p in cart_items:
                value = p.quantity * p.product.discounted_price
                famount += value
        totalamount = famount + 40
        razoramount =int(totalamount *100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = {'amount':razoramount,'currency':"INR","receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'amount': 27000, 'amount_due': 27000, 'amount_paid': 0, 'attempts': 0, 'created_at': 1725693933, 'currency': 'INR', 'entity': 'order', 'id': 'order_OuC2ejmmlQETSS', 'notes': [], 'offer_id': None, 'receipt': 'order_rcptid_12', 'status': 'created'} 
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        
        return render(request,'app/checkout.html',locals())

@login_required    
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    prod_id = request.GET.get('prod_id')
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    if prod_id:
        product = Product.objects.get(id=prod_id)
        OrderPlaced(user=user,customer=customer,product=product,quantity=1,payment=payment).save()
    else:
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
            c.delete()
    return redirect("orders")

@login_required  
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',locals())

# @login_required  
def search(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    query = request.GET['search']
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html",locals())