from django.shortcuts import render, HttpResponseRedirect
from .models import *
from ecommerce.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from ecommerce.views import *
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session
from orders.models import *


# Cart interface
@login_required
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user, ordered=False)
        cartItem = CartItem.objects.filter(cart=cart)

        # To print the image on cart #######################################
        productImage = []
        for cartItem in cartItem:
            image = ProductImage.objects.get(product=cartItem.product, featured=True)
            productImage.append(image.image)
            cartItem.imageName = image.image
            cartItem.save()

        ###################################################################

        context = {'cart': cart, 'cartItem': cartItem, 'productImage': productImage, 'empty': False, }
    except:
        # if not, the status will be none
        message_empty = "Cart is empty"
        context = {'empty': True, 'message_empty': message_empty}

    template = 'cart/cart.html'
    return render(request, template, context)


# For the updated cart (add cart)
# https://www.codehub.vn/Session-La-Gi
def update_cart(request, slug):
    request.session.set_expiry(120000)  # session expire in 120,000 seconds

    # Check cart
    try:
        cart = Cart.objects.get(user=request.user, ordered=False)
        # cart = request.session['cart_id']
    except:
        createCart = Cart(user=request.user, ordered=False)
        createCart.save()

    cart = Cart.objects.get(user=request.user, ordered=False)

    # Check product
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass
    except:
        pass

    # cart_item = CartItem.objects.get_or_create(cart = cart,product=product)
    if CartItem.objects.filter(cart=cart, product=product).exists():
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item = CartItem.objects.create(cart=cart, product=product)

    CartItem.totalItem(cart_item)
    Cart.cartTotal(cart)

    totalCount = cart.cartitem_set.count()
    cart.totalCount = totalCount
    cart.save()

    request.session['key'] = totalCount

    return HttpResponseRedirect(reverse("homeMain"))


# Delete and update in the cart
def delete_cart(request, slug):
    product = Product.objects.get(slug=slug)

    cart = Cart.objects.get(user=request.user, ordered=False)

    item = CartItem.objects.get(cart=cart, product=product)

    try:
        qty = request.GET.get('qty')
        update_qty = True
    except:
        qty = None
        update_qty = False

    if qty and update_qty:
        if int(qty) == 0:
            cartItem = CartItem.objects.filter(product=product)
            cartItem.delete()
        elif int(qty) < 0:
            messages.error(request, 'The number of' + item.product.title + ' must be  bigger than 1!!!')
        else:
            item.quantity = qty
            item.save()
    else:
        pass

    if request.method == 'POST':
        qty = request.POST['delete']
        if int(qty) == 0:
            cartItem = CartItem.objects.filter(product=product)
            cartItem.delete()
        elif int(qty) < 0:
            messages.error(request, 'The number of ' + item.product.title + ' must be bigger than 1!!!')
        else:
            item.quantity = qty
            item.save()
            totalItem = CartItem.totalItem(item)
    else:
        pass

    Cart.cartTotal(cart)

    totalCount = cart.cartitem_set.count()

    if totalCount == 0:
        cart1 = Cart.objects.filter(user=request.user, ordered=False)
        cart1.delete()
        try:
            order = Order.objects.filter(user=request.user, cart=cart1)
            order.delete()
        except:
            pass
    else:
        cart.totalCount = totalCount
        cart.save()

    request.session['key'] = totalCount

    return HttpResponseRedirect(reverse("cart"))
