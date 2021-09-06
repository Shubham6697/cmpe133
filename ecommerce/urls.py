from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include, re_path
from . import views
from .views import register, homeMain, about, signin, logout_views, UniqueProduct, search, category, contact
from carts.views import cart, update_cart, delete_cart
from orders.views import checkout, orders, time_shipping
from accounts.views import add_address, profile
urlpatterns = [ 
    # first page, before sign in
    # path('', home, name='home'),
    path('', homeMain, name="homeMain"),
    # to introduce company
    path('about', about, name='about'),
    # to sign in
    path('signin', signin, name='signin'),
    #  to register
    path('register', register, name='register'),
    # to log out
    path("logout", logout_views, name="logout"),
    #to contact us
    path("contact",contact, name="contact"),
    # To change or add address
    path('add_address', add_address, name="add_address"), 

    url(r'^category/$',category, name="category"),

    # this link is to display product after log in
    # This link is for searching, s for search
    url(r'^s/$',search, name='search'),
    # to specific product, have a unique slug (slug is the unique code for a product), and id of product
    # url(r'^product/(?P<slug>[\w-]+)/(?P<id>\d+)/$', product, name='product'),
    #     (?P<all_items>.*)
    #  if use "\d+" to make the url only digit:     (?P<id>\d+)
    # To show unique product
    path('<slug:slug>UniqueProduct', UniqueProduct , name='product'),
    # To show cart
    path('yourCart', cart, name='cart'),
    # To change the cart
    url(r'^yourCart/(?P<slug>[\w-]+)/$',update_cart, name='update_cart'),
    # To remove item
    url(r'^yourCart/delete/(?P<slug>[\w-]+)/$',delete_cart, name='delete_cart'),
    # To checkout
    path('checkout', checkout , name='checkout'),

    # Order of costumers
    path('orders', orders , name='orders'),

    path('success', views.success , name='success'),

    # the profile of costumer
    path('profile', profile, name='profile'), 
    path('time_shipping', time_shipping, name='time_shipping'), 
]
