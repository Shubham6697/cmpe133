from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
# from .forms import UserRegisterForm
from .models import User, Product, ProductImage, Contact
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from accounts.views import *

# from .forms import ContactForm

def homeMain(request):
    product = Product.objects.all()
    try:
        cart = Cart.objects.get(user=request.user, ordered=False)
        totalCount = cart.cartitem_set.count()
        request.session['key'] = totalCount
    except:
        pass
    context = {'product': product,
               'title': 'Home Page', }
    template = 'html/homeMain.html'
    return render(request, template, context)

def search(request): 
    try:
        search = request.GET.get('search')
    except: 
        search = None

    if search: 
        product = Product.objects.filter(title__icontains = search)
        context = {'query': search, 'product': product}
        template = 'html/search.html'
    else: 
        return redirect('homeMain')
    return render(request, template, context)

def category(request):
    try: 
        chooseCategory= request.GET.get('category')
    except: 
        raise Http404(" A category does not exist")

    if chooseCategory: 
        category = Product.objects.filter(category = chooseCategory)

        context = {'category': category, }
        template = 'html/category.html'
    else: 
        return redirect('homeMain')
    
    return render(request, template, context)

def about(request):
    # u = User.objects.get(username=request.user.username)

    return render(request, 'html/about.html', {'title': 'About'})

#  sign in function
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homeMain')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('signin')
    else:
        return render(request, 'html/signin.html', {'title': 'Sign in'})

# Logout function
# should set name function is different than logout unless the recusion problem happens.
def logout_views(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('homeMain')


# register function
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                password=password, email=email)
                user.save()
                messages.success(request, f'Account created {user.username}!')
                return redirect('signin')
        else:
            messages.error(request, 'Does not match password')
    # else:
    #     form = UserCreationForm()
    return render(request, 'html/register.html')

# for a specific product
# @login_required
def UniqueProduct(request,slug):
    try:
        product = Product.objects.get(slug=slug)
        # print(products.title)
        # images = ProductImage.productimage_set.all()
        images = ProductImage.objects.filter(product=product)
        context = {'product': product,'images': images, 
                   'title': 'Home Page'}
        template = 'html/product.html'
        return render(request, template, context) 
    except product.DoesNotExist:
        raise Http404("Does not exist")


def contact(request): 
    request.session.set_expiry(120000)
    try:
        user = request.user
        context = { 'user':user, }
    except: 
        pass
    
    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        if request.user.is_authenticated: 
            contact = Contact.objects.create( user=request.user, firstName=firstName, lastName=lastName,email=email)
            contact.save()
        else:
            contact = Contact.objects.create(firstName=firstName, lastName=lastName,email=email)
            contact.save()
        messages.info(request, "Your feedback / questions has sent")
        return redirect('add_address')

    template = 'accounts/newaddress.html'
    return render(request, template, context)

def success(request):
    template = 'html/success.html'
    return render(request, template)
    


