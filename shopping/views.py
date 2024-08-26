from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse ,JsonResponse
from .forms import ProductDetail, CustomLoginForm, SignUp
from .models import Product, AppUser, Category, CartItem ,Order ,OrderItem
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import stripe
from django.conf import settings




#Stripe Secert Key
stripe.api_key = settings.STRIPE_SECRET_KEY

#Home Page
def home(request):
    data = Product.objects.all()
    category = Category.objects.all()
    return render(request, "home.html", {"products": data, "categories": category})


#Login User Page
@login_required(login_url="user_login")
def login_user_home(request):
    data = Product.objects.all()
    category = Category.objects.all()
    return render(
        request, "login_user_home.html", {"products": data, "categoreis": category}
    )


#Registration Form
def signup(request):
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            contact = form.cleaned_data["contact"]
            address = form.cleaned_data["address"]
            password = form.cleaned_data["password"]

            # Check if a user with this email already exists
            if AppUser.objects.filter(email=email).exists():
                return render(
                    request,
                    "signup.html",
                    {"form": form, "error": "Email already exists"},
                )

            user=User.objects.create(
                username=username,
                password=make_password(password),
                email=email,
            )

            # Create a new AppUser instance
            AppUser.objects.create(
                user=user,
                username=username,
                email=email,
                contact=contact,
                address=address,
            )

            return redirect("user_login")
    else:
        form = SignUp()

    return render(request, "signup.html", {"form": form})


#Login 
def user_login(request):
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        data = Product.objects.all()
        if user:
            print("user authenticte successfully ")
            auth_login(request, user)
            return render(request, "login_user_home.html", {"products": data})
        else:
            return render(
                request, "login.html", {"form": form, "error": "Enter Correct Details"}
            )
    else:
        form = CustomLoginForm()
        print("inside login function")
        return render(request, "login.html", {"form": form})


#Add Product
def add_prdouct(request):
    if request.method == "POST":
        form = ProductDetail(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = ProductDetail()
    return render(request, "add_product.html", {"form": form})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    category = Category.objects.all()
    return render(request, "product_details.html", {"product": product,'categories':category})


#Show Products by Category
def product_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(
        request,
        "product_list.html",
        {"category": category, "products": products, "categories": categories},
    )

#Show user profile
@login_required(login_url="user_login")
def user_profile(request):
    try:
        username1 = request.user.appuser
        print("User is:", username1)
        app_user = AppUser.objects.get(username=username1)
        category = Category.objects.all()
        return render(request, "user_profile.html", {"app_user": app_user ,'categories':category})
    except:
        return render(request, "user_profile.html", {"error": "Not Exists"})

#Update User Profile
@login_required(login_url="user_login")
def update_profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        email = request.POST.get("email")
        print("Email is:", email)
        update_data = AppUser.objects.get(email=email)
        print("Update data :", update_data)
        update_data.username = username
        update_data.contact = contact
        update_data.address = address
        update_data.save()

        user_model_data = User.objects.get(email=email)
        user_model_data.username = username
        user_model_data.save()

        return redirect("user_profile")

    else:
        username = request.user
        app_user = AppUser.objects.get(username=username)
        category = Category.objects.all()
        return render(request, "update_profile.html", {"app_user": app_user,'categories':category})


# View Cart
@login_required(login_url="user_login")
def view_cart(request):
    app_user = request.user.appuser
    print("User inside view_Cart:", app_user)   
    cart_items = CartItem.objects.filter(user=app_user)
    category = Category.objects.all()
    print("Catt_Item:", cart_items)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, "view_cart.html",{"cart_items": cart_items, "total_price": total_price ,'categories':category})


# Add to cart
@login_required(login_url="user_login")
def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    # import pdb; pdb.set_trace()
    app_user = AppUser.objects.filter(email=user.email).first()
    print("Product is:", product)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=app_user)

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()
    return redirect("view_cart")


# Remove Items from Cart
@login_required(login_url="user_login")
def remove_items(request, item_id):
    try:
        app_user = AppUser.objects.get(user=request.user)
        print('APP_USER:',app_user)
        cart_item = CartItem.objects.get(user=app_user, product_id=item_id)
        print('CART_Item is:',cart_item)
        cart_item.delete()
        print('CartItem deleted successfully')  # Debugging line
    except AppUser.DoesNotExist:
        print('AppUser does not exist')  # Debugging line
        return redirect("user_login")
    except CartItem.DoesNotExist:
        print('CartItem does not exist')  # Debugging line
        return redirect("view_cart")
    
    return redirect("view_cart")



@login_required(login_url="user_login")
def delete_account(request):
    try:
        print("inside try block")
        user = request.user
        app_user = AppUser.objects.get(username=user)
        user.delete()
        app_user.delete()
        return redirect("logout_view")
    except AppUser.DoesNotExist:
        print("AppUser does not exist")
        return redirect("login_user_home")
    except Exception as e:
        print("An error occurred: ", e)
        return redirect("login_user_home")
    
#Show Products based on filter
def show_product(request):
    if request.method=='GET':
        query=request.GET.get('search')
        category = Category.objects.all()
        print('Data Filter is:',query)
        if query:
            filter_data=Product.objects.filter(name__icontains=query)
        else:
            filter_data=Product.objects.all()
        return render(request ,'filter_data.html',{'filter_data':filter_data ,'query':query ,'categories':category})
    

#Buy Product
@login_required(login_url='user_login')
def buy_now(request,product_id):
    product =get_object_or_404(Product,id=product_id)
    print("Product Id is:",product_id)
    print('ProductL:',product)
    app_user =  request.user.appuser
    address=app_user.address
    print('Address:',address)   
    total_amount=product.price 
    print('Total Amount:',total_amount)
    shipping_amount=70
    total_amount+= shipping_amount


    return render(request, 'buy_now.html', {
        'product': product,
        'total_amount': total_amount,
        'shipping_amount': shipping_amount,
        'address':  address
    })

#Confirm Order
@login_required(login_url='user_login')
def confirm_order(request ,product_id):
    product =get_object_or_404(Product,id=product_id)
    total_amount=product.price 
    print('Total Amount:',total_amount)
    shipping_amount=70
    total_amount+= shipping_amount
    return render(request ,'order_done.html',{'product':product ,'total_amount':total_amount})

#Payment Getway
@login_required(login_url='user_login')
def order_done(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        try:
            order=Order.objects.create(
                user=request.user.appuser,
            )
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                price=product.price,

            )
             
             
            # Create a Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',  # Change to 'usd' or another supported currency
                        'product_data': {
                            'name': product.name,
                        },
                        'unit_amount': int(product.price * 100),  # Amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(f'/order_summary/{order.id}/'),
                cancel_url=request.build_absolute_uri('/payment_cancel/'),
            )
            return redirect(session.url, code=303)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': f'Stripe error: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


#Order Detail
@login_required(login_url='user_login')
def order_summary(request,order_id):
    order=Order.objects.get(id=order_id,user=request.user.appuser)
    print('Order is:',order)
    return render(request,'order_summary.html',{'order':order})

    
@login_required(login_url='user_login')
def payment_success(request):
    # Handle successful payment here, like updating order status
    return render(request ,'order_summary.html')


@login_required(login_url='user_login')
def payment_cancel(request):
    # Handle payment cancellation here
    return redirect('login_user_home')


@login_required(login_url="user_login")
def logout_view(request):
    logout(request)
    return redirect("home")
