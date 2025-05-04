from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User

def home(request):
    product_name = request.GET.get('product_name')
    category = request.GET.get('category')

    filters = {}

    if product_name:
        filters['name__icontains'] = product_name
    if category:
        filters['category'] = category

    products = Product.objects.filter(**filters)
    categories = Category.objects.all()

    return render(request, 'home.html', {'products': products, 'categories': categories})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    protected_categories = ['ვეფხისტყაოსანი', 'პერსონაჟები']

    if product.category:

        return render(request, 'product_detail.html', {'product': product})

@login_required
def create_product(request):
    form = ProductForm(user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            product = form.save(commit=False)

            # Check if the category is protected and restrict non-superusers from selecting it
            if product.category and product.category.name in ['ვეფხისტყაოსანი', 'პერსონაჟები']:
                if not request.user.is_superuser:
                    messages.error(request, 'You cannot create products under this category.')
                    return redirect('home')

            product.save()
            messages.success(request, 'Product has been created successfully.')
            return redirect('home')

    return render(request, 'product_form.html', {'form': form})


@login_required
def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    
    if not request.user.is_superuser and product.category.created_by != request.user:
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

    if not request.user.is_superuser and product.category.created_by != request.user:
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
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Ensures login works immediately
            login(request, user)
            messages.success(request, 'Welcome! You are now registered and logged in.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'user_form.html', {'form': form})