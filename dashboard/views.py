from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages


@login_required
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()

    worker_count = User.objects.all().count     # display dynamically the numbers of registered staffs in /dashboard
    product_count = Product.objects.all().count()   # display dynamically the numbers of products in /dashboard
    order_count = Order.objects.all().count()

    if request.method == 'POST':    #User making request from their profile
        form = OrderForm(request.POST)
        if form.is_valid():
            # assign a user to whoever is making an order request || Assign a staff to the order being made
            instance = form.save(commit=False) #False - form not yet saved
            instance.staff = request.user #assign the activity to the loggedin user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()

    context = {
        'orders': orders,
        'form': form,
        'products': products,
        'worker_count': worker_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def staff(request):
    worker = User.objects.all()

    worker_count = worker.count() # display dynamically the numbers of registered staffs
    product_count = Product.objects.all().count()   # display dynamically the numbers of products in /staff
    order_count = Order.objects.all().count()

    context = {
        'worker': worker,
        'worker_count': worker_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/staff.html', context)


def staff_detail(request, pk):
    worker = User.objects.get(id=pk)
    context = {
        'worker': worker,
    }
    return render(request, 'dashboard/staff_detail.html', context)


@login_required
def product(request):
    items = Product.objects.all() #Using ORM to diaplay items to the dashboard
    # items = Product.objects.raw('SELECT * FROM dashboard_product') #use sql to query the database

    product_count = items.count()   # display dynamically the numbers of products
    worker_count = User.objects.all().count()     # display dynamically the numbers of registered staffs in /products
    order_count = Order.objects.all().count()

    #creating adding items in dashboard frontend
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            
            # Flash message (product added)
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added !' )
            return redirect ('dashboard-product')
    else:
        form = ProductForm()

    context = {
        'items': items,
        'form': form,
        'product_count': product_count,
        'worker_count': worker_count,
        'order_count': order_count,
    }

    return render(request, 'dashboard/product.html', context)

# Deleting a product
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render (request, 'dashboard/product_delete.html')


def product_update(request, pk):
    items = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=items) #post prefilled form 
        if form.is_valid():
            form.save()
            return redirect ('dashboard-product')
    else:
        form = ProductForm(instance=items)
    
    context = {
        'form': form,
    }

    return render(request, 'dashboard/product_update.html', context)


@login_required
def order(request):
    orders = Order.objects.all()

    order_count = orders.count()    
    worker_count = User.objects.all().count()     # display dynamically the numbers of registered staffs in /orders
    product_count = Product.objects.all().count()   # display dynamically the numbers of products in /orders

    context = {
        'orders': orders,
        'order_count': order_count,
        'worker_count': worker_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/order.html', context)