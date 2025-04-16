from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .forms import ProductDetail, CustomLoginForm, SignUp
from .models import Product, AppUser, Category, CartItem, OrderItem
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import stripe
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


#Stripe Secert Key
stripe.api_key = settings.STRIPE_SECRET_KEY

#Home Page
class Home(View):
    def get(self, request):
       data = Product.objects.all()
       category = Category.objects.all()
       return  render(request, 'home.html', {'products' : data,'categories':category})


#Login User Page
class LoginUserHome(LoginRequiredMixin, View):
    login_url = 'user_login'
    def get(self, request):
       data= Product.objects.all()
       category= Category.objects.all()
       return  render(request, 'login_user_home.html', {'products':data,'categories':category})


#Registration Form
class Signup(View):

    def post(self,request):
        form = SignUp(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            contact = form.cleaned_data["contact"]
            address = form.cleaned_data["address"]
            password = form.cleaned_data["password"]

            # Check if a user with this email already exists
            if AppUser.objects.filter(email = email).exists():
                return render(request, "signup.html", {"form": form, "error": "Email already exists"})
                
            user = User.objects.create(
                username = username,
                password = make_password(password),
                email = email,
            )
            
            # Create a new AppUser instance
            AppUser.objects.create(
                user = user,
                username = username,
                email = email,
                contact = contact,
                address = address,
            )
            subject = 'Welcome on shoppinglyx'
            message = f"Hi,{user.username} thank you for joining india's best service provider group"
            email_from = settings.EMAIL_HOST_USER
            recepient_list = [user.email]
            send_mail(subject, message, email_from ,recepient_list)
 
            return redirect("user_login")

        else:
            return render(request, 'signup.html', {"form": form , "error" : 'Please correct below errors'})

    def get(self, request):
        form = SignUp()
        return render(request, 'signup.html', {'form' : form})


#Login 
class UserLogin(View):

    def post(self ,request):
        form = CustomLoginForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)
        data = Product.objects.all()
        if user:
            auth_login(request, user)
            #Welcome message on every time when user login
            subject = 'Welcome on shoppinglyx'
            message = f"Hi {username} Welcome to shoppinglyx"
            email_from = settings.EMAIL_HOST_USER
            recepient_list = [request.user.appuser.email]
            send_mail(subject, message, email_from, recepient_list)
            return render(request, "login_user_home.html", {"products" : data})
        else:
            return render(request, "login.html", {"form" : form , "error" : "Enter Correct Details"})
    
    def get(self ,request):
        form = CustomLoginForm()
        return render(request, "login.html", {"form" : form})


#Add Product
class AddProduct(View):
    def post(self, request):
        form = ProductDetail(request.POST, request.FILES)
        if form.is_valid():          
                name = form.cleaned_data['name']
                desc = form.cleaned_data['desc']
                price = form.cleaned_data['price']
                stock = form.cleaned_data['stock']
                image = form.cleaned_data['image']
                category = form.cleaned_data['category']
                existing_product = Product.objects.filter(name = name)
                if existing_product:
                    existing_product.update(
                        stock = existing_product.first().stock + stock,
                        desc = desc,   
                        price = price,   
                    )
                     
                else:
                    Product.objects.create(
                        name = name,
                        desc = desc,
                        price = price,
                        stock = stock,
                        image = image,
                        category = category,
                    )
                return redirect("home")

           
        return render(request, "add_product.html", {"form" : form, "error" : "Invalid Data...please follow the rules"})

    def get(self ,request):
        form = ProductDetail()
        return render(request, "add_product.html", {"form" : form})
    

#Show Product with description 
class ProductDetails(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        category = Category.objects.all()
        return render(request, "product_details.html", {"product": product,'categories':category})


#Show Products by Category
class ProductListByCategory(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id = category_id)
        products = Product.objects.filter(category = category)
        categories = Category.objects.all()
        return render(request, "product_list.html", {"category" : category, "products" : products, "categories" : categories})


#Show user profile
class UserProfile(LoginRequiredMixin, View):
    login_url = 'user_login'
    def get(self, request):
        try:
            username1 = request.user.appuser
            app_user = AppUser.objects.get(username = username1)
            category = Category.objects.all()
            return render(request, "user_profile.html", {"app_user" : app_user, 'categories' : category})
        except:
            return render(request, "user_profile.html", {"error" : "Not Exists"})


#Update User Profile
class UpdateProfile(LoginRequiredMixin,View):
        login_url='user_login'
        def post(self,request):
            username = request.POST.get("username")
            contact = request.POST.get("contact")
            address = request.POST.get("address")
            email = request.POST.get("email")
            update_data = AppUser.objects.get(email = email)
            update_data.username = username
            update_data.contact = contact
            update_data.address = address
            update_data.save()

            user_model_data = User.objects.get(email = email)
            user_model_data.username = username
            user_model_data.save()

            return redirect("user_profile")

        def get(self, request):
            username = request.user
            app_user = AppUser.objects.get(username = username)
            category = Category.objects.all()
            return render(request, "update_profile.html", {"app_user" : app_user, 'categories' : category})


# View Cart
class ViewCart(LoginRequiredMixin, View):
    login_url = 'user_login'
    def get(self, request):
        app_user = request.user.appuser
        cart_items = CartItem.objects.filter(user = app_user)
        category = Category.objects.all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, "view_cart.html", {"cart_items" : cart_items, "total_price": total_price, 'categories' : category})
 

# Add to cart
class AddToCart(LoginRequiredMixin, View):
    login_url='user_login'
    def get(self, request, product_id):
        user = request.user
        product = get_object_or_404(Product, id = product_id)
        app_user = AppUser.objects.filter(email = user.email).first()
        cart_item, created = CartItem.objects.get_or_create(product = product, user = app_user)

        if not created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1

        cart_item.save()
        return redirect("view_cart")


# Remove Items from Cart
class RemoveItems(LoginRequiredMixin, View):
    login_url = 'user_login'
    def get(self,request, item_id):
        try:
            app_user = AppUser.objects.get(user = request.user)
            cart_item = CartItem.objects.get(user = app_user, product_id = item_id)
            cart_item.delete()
        except AppUser.DoesNotExist:
            return redirect("user_login")
        except CartItem.DoesNotExist:
            return redirect("view_cart")
   
        return redirect("view_cart")


#Delete User Account
class DeleteAccount(LoginRequiredMixin, View):
    login_url = 'user_login'
    def get(self, request):
        try:
            user = request.user
            app_user = AppUser.objects.get(username = user)
            user.delete()
            app_user.delete()
            return redirect("logout_view")
        except AppUser.DoesNotExist:
            return redirect("login_user_home")
        except Exception as e:
            return redirect("login_user_home")
    
#Show Products based on filter
class ShowProduct(View):
    def get(self, request):
        query = request.GET.get('search')
        category = Category.objects.all()
        if query:
            filter_data = Product.objects.filter(name__icontains = query)
        else:
            filter_data = Product.objects.all()
        return render(request, 'filter_data.html', {'filter_data' : filter_data, 'query' : query, 'categories' : category})
    

#Buy Product
class BuyNow(LoginRequiredMixin, View):
    login_url = 'user_login'
    def get(self, request, product_id):
        product = get_object_or_404(Product, id = product_id)
        app_user =  request.user.appuser
        address = app_user.address
        total_amount = product.price 
        return render(request, 'buy_now.html', {
            'product' : product,
            'total_amount' : total_amount,
            'address' :  address
        })

#Confirm Order
# class ConfirmOrder(LoginRequiredMixin,View):
#     login_url='user_login'
#     def get(self,request ,product_id):
#         product =get_object_or_404(Product,id=product_id)
#         total_amount=product.price 
#         print('Total Amount:',total_amount)
#         shipping_amount=70
#         total_amount+= shipping_amount
#         return render(request ,'order_done.html',{'product':product ,'total_amount':total_amount})


#Payment Getway
class OrderDone(LoginRequiredMixin, View):
    def post(self, request, product_id = None):
        try:
            if product_id:  # If product_id is provided
                product = get_object_or_404(Product, id = product_id)

                if product.stock < 1:
                    return render(request, "order_done.html", {'errors' : f'Insufficient stock for {product.name}.'})
                
                product.stock -= 1
                product.save()

                OrderItem.objects.create(
                    user = request.user.appuser,
                    product = product,
                    quantity = 1,
                    price = product.price,
                )
                
                # Create a Stripe Checkout Session
                session = stripe.checkout.Session.create(
                    payment_method_types = ['card'],
                    line_items = [{
                        'price_data' : {
                            'currency' : 'inr',
                            'product_data' : {
                                'name': product.name,
                            },
                            'unit_amount': int(product.price * 100) ,
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url = request.build_absolute_uri('/payment_success/'),
                    cancel_url = request.build_absolute_uri('/payment_cancel/'),
                )
                return redirect(session.url, code=303)

            else:  # Process all cart items
                items = CartItem.objects.filter(user = request.user.appuser)
                line_items = []
                for item in items:
                    product = item.product

                    if product.stock < item.quantity :
                        return render(request, "view_cart.html", {'errors': f'Insufficient stock for {product.name}. Available: {product.stock}, Requested: {item.quantity}'})
                    
                    product.stock -= item.quantity
                    product.save()

                    OrderItem.objects.create(
                        user=request.user.appuser,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,
                    )
                  
                    line_items.append({
                        'price_data': {
                            'currency': 'inr',
                            'product_data': {
                                'name': item.product.name,
                            },
                            'unit_amount': int(item.product.price * 100)  ,
                        },
                        'quantity': item.quantity,
                    })
                items.delete()
                # Create a Stripe Checkout Session with all cart items
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri('/payment_success/'),
                    cancel_url=request.build_absolute_uri('/payment_cancel/'),
                )
                return redirect(session.url, code=303)

        except stripe.error.StripeError as e:
            return render(request,"order_done.html",{'error': f'Stripe error: {str(e)}'})
        except Exception as e:
            return render(request,"order_done.html",{'error': f'Error: {str(e)}'})


#Order Detail
class OrderSummary(LoginRequiredMixin ,View):
    login_url='user_login'
    def get(self,request):
        return render(request,'order_summary.html')

#Payment Success
class PaymentSuccess(LoginRequiredMixin ,View):
    login_url='user_login'
    def get(self,request):
        # Handle successful payment here, like updating order status
        app_user=request.user.appuser.email
        print('Email :',app_user)
        subject ='Order Successful'
        message= '''Thank you for order please visit again..... ,have a nice day'''
        email_from= settings.EMAIL_HOST_USER
        recepient_list= [app_user]
        send_mail(subject ,message ,email_from ,recepient_list)
        category = Category.objects.all()
        return render(request ,'order_summary.html',{'categories':category})

#Payment Cancel
class PaymentCancel(LoginRequiredMixin,View):
    login_url='user_login'
    def get(self,request):
        # Handle payment cancellation here
        return redirect('login_user_home')


#Show Order History
class ShowOrderList(LoginRequiredMixin ,View):
    login_url='user_login'
    def get(self,request):
        app_user=request.user.appuser
        order_details=OrderItem.objects.filter(user=app_user) 
        print('OrderItems :',order_details)
        category = Category.objects.all()        
        return render(request,'show_order_list.html',{'orders':order_details,'categories':category})

#Cancel Order
class CancelOrder(LoginRequiredMixin ,View):
    login_url='user_login'
    def get(self,request ,product_id):
        order=get_object_or_404(OrderItem ,id =product_id)
        order.delete()
        return redirect('show_order_list')



#Logout
class Logout(LoginRequiredMixin,View):
    login_url='user_login'
    def get(self,request):
        logout(request)
        return redirect("home")
