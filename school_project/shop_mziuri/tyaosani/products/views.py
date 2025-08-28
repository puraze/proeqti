from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import get_language

PROTECTED_CATEGORY_NAMES = ['ვეფხისტყაოსანი', 'პერსონაჟები']

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.utils.translation import get_language
from django.http import Http404

from .models import Product, Category
from .forms import ProductForm
from django.http import HttpResponseForbidden

def home(request):
    language = get_language()  # current selected language ('ka', 'en', 'ru', etc.)
    
    products = Product.objects.filter(language_visibility=language).order_by('-id')
    categories = Category.objects.all()
    
    # Search filter
    product_name = request.GET.get('product_name')
    category_id = request.GET.get('category')
    
    if product_name:
        products = products.filter(name__icontains=product_name)
    if category_id:
        products = products.filter(category__id=category_id)
    
    # Pagination
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'products': products_page,
        'categories': categories,
    }
    return render(request, 'home.html', context)


@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect("product_detail", pk=product.pk)
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Remove the "language" check
    product.views = (product.views or 0) + 1
    product.save(update_fields=['views'])

    return render(request, 'product_detail.html', {'product': product})

@login_required
def update_product(request, id):
    product = get_object_or_404(Product, id=id)

    if not request.user.is_superuser and hasattr(product, 'author') and product.author != request.user:
        messages.error(request, 'You do not have permission to update this product.')
        return redirect('home')

    form = ProductForm(instance=product, user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product has been updated successfully.')
            return redirect('home')

    return render(request, 'product_form.html', {'form': form})

@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    if not request.user.is_superuser and hasattr(product, 'author') and product.author != request.user:
        messages.error(request, 'You do not have permission to delete this product.')
        return redirect('home')

    product.delete()
    messages.success(request, 'Product has been deleted successfully.')
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! You are now registered and logged in.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'user_form.html', {'form': form})
