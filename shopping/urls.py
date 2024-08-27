from django.contrib import admin
from django.urls import path 
from  . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import order_done, payment_success, payment_cancel



urlpatterns=[
    path("admin/",admin.site.urls),
    path('',views.home,name='home'),
    path('add_product/',views.add_prdouct,name='add_product'),
    path('product_detail/<int:product_id>/',views.product_detail,name='product_detail'),
    path('user_login/',views.user_login ,name='user_login'),
    path('signup/',views.signup,name='signup'),
    path('login_user_home/',views.login_user_home,name='login_user_home'),
    path('logout/',views.logout_view,name='logout_view'),
    path('user_profile/',views.user_profile ,name='user_profile'),
    path('update_profile/',views.update_profile,name='update_profile'),
    path('delete_account/',views.delete_account ,name='delete_account'),
    path('category/<int:category_id>/', views.product_list_by_category, name='product_list_by_category'),
    path('view_cart/',views.view_cart ,name='view_cart'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart ,name='add_to_cart'),
    path('remove_items/<int:item_id>/',views.remove_items ,name='remove_items'),
    path('show_product/',views.show_product ,name='show_product'),
    path('buy_now/<int:product_id>/' ,views.buy_now ,name='buy_now'),
    path('confirm_order/<int:product_id>/',views.confirm_order, name='confirm_order'),
    path('order_done/<int:product_id>/',views.order_done,name='order_done'),
    #path('order_summary/<int:order_id>/',views.order_summary,name='order_summary'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path('show_order_list/',views.show_order_list ,name='show_order_list'),
    path('order_using_cart/',views.order_done ,name='order_using_cart'),
    path('cancel_order/<int:product_id>/',views.cancel_order ,name='cancel_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)