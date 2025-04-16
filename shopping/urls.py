from django.contrib import admin
from django.urls import path 
from  . views import *
from django.conf import settings
from django.conf.urls.static import static




urlpatterns=[
    path("admin/",admin.site.urls),
    path('', Home.as_view(),name='home'),
    path('add_product/',AddProduct.as_view(),name='add_product'),
    path('product_detail/<int:product_id>/',ProductDetails.as_view(),name='product_detail'),
    path('user_login/',UserLogin.as_view() ,name='user_login'),
    path('signup/',Signup.as_view(),name='signup'),
    path('login_user_home/',LoginUserHome.as_view(),name='login_user_home'),
    path('logout/',Logout.as_view(),name='logout_view'),
    path('user_profile/',UserProfile.as_view() ,name='user_profile'),
    path('update_profile/',UpdateProfile.as_view(),name='update_profile'),
    path('delete_account/',DeleteAccount.as_view() ,name='delete_account'),
    path('category/<int:category_id>/', ProductListByCategory.as_view(), name='product_list_by_category'),
    path('view_cart/',ViewCart.as_view() ,name='view_cart'),
    path('add_to_cart/<int:product_id>/',AddToCart.as_view(),name='add_to_cart'),
    path('remove_items/<int:item_id>/',RemoveItems.as_view() ,name='remove_items'),
    path('show_product/',ShowProduct.as_view() ,name='show_product'),
    path('buy_now/<int:product_id>/' ,BuyNow.as_view() ,name='buy_now'),
    # path('confirm_order/<int:product_id>/',ConfirmOrder.as_view(), name='confirm_order'),
    path('order_done/<int:product_id>/',OrderDone.as_view(),name='order_done'),
    #path('order_summary/<int:order_id>/',order_summary,name='order_summary'),
    path('payment_success/', PaymentSuccess.as_view(), name='payment_success'),
    path('payment_cancel/', PaymentCancel.as_view(), name='payment_cancel'),
    path('show_order_list/',ShowOrderList.as_view() ,name='show_order_list'),
    path('order_using_cart/',OrderDone.as_view()  ,name='order_using_cart'),
    path('cancel_order/<int:product_id>/',CancelOrder.as_view() ,name='cancel_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
