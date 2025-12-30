from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, FileResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import ProductForm
import os

def index(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    # Mock data for trending if needed, or use logic
    trending_products = products[:5] 
    return render(request, 'store/index_final.html', {
        'products': products,
        'categories': categories,
        'trending_products': trending_products
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'store/detail.html', {'product': product})

def search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(title__icontains=query)
    else:
        products = Product.objects.none()
    
    return render(request, 'store/search.html', {'products': products, 'query': query})

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category.html', {'category': category, 'products': products})

def about(request):
    return render(request, 'store/about.html')

def contact(request):
    return render(request, 'store/contact.html')

def contact(request):
    return render(request, 'store/contact.html')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()
    
    return render(request, 'store/add_product.html', {'form': form})

def download_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.file:
        # For local development, serving file directly. 
        # In production, use X-Sendfile or similar.
        response = FileResponse(product.file.open(), as_attachment=True)
        return response
    else:
        messages.error(request, "File not available for download.")
        return redirect('product_detail', product_id=product.id)

def buy_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # Mock payment flow
    messages.success(request, f"Thank you for purchasing {product.title}!")
    return redirect('product_detail', product_id=product.id)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome back, {username}!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')
