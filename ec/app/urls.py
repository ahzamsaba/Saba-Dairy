from django.contrib import admin
from django.urls import path
from .views import *
from .forms import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',home,name="home"),
    path('about/',about,name="about"),
    path('contact/',contact,name="contact"),
    path('category/<slug:val>/',CategoryView.as_view(),name="category"),
    path('category-title/<val>',CategoryTitle.as_view(),name="category-title"),
    path('product-detail/<int:pk>/',ProductDetail.as_view(),name="product-detail"),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('address/',address,name='address'),
    path('updateAddress/<int:pk>/',updateAddress.as_view(),name='updateAddress'),
    
    path('add-to-cart/',add_to_cart, name="add-to-cart"),
    path('cart/',show_cart, name="showcart"),
    path('checkout/',checkout.as_view(), name="checkout"),
    path('paymentdone/',payment_done,name='paymentdone'),
    path('orders/',orders,name="orders"),
    path('wishlist/',wishlist,name="wishlist"),

    path('search/',search,name="search"),
    
    path('pluscart/',plus_cart),
    path('minuscart/',minus_cart),
    path('removecart/',remove_cart),

    path("pluswishlist/",plus_wishlist),
    path("minuswishlist/",minus_wishlist),


    #login authentication
    path('registration/',CustomerRegView.as_view(),name='registration'),
    path('accounts/login',auth_view.LoginView.as_view(template_name='app/login.html' , authentication_form=LoginForm), name='login'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm ,success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    
    #forgot password
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html' , form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html' , form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Saba Dairy"
admin.site.site_title = "Saba Dairy"
admin.site.index_title = "Welcome to Saba Dairy"