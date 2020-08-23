from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Customer, Equipment, Order
from .forms import CreateOrderForm, UpdateOrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # user = form.save()
            username = form.cleaned_data.get('username')
            # group = Group.objects.get(name='produccion')
            # user.groups.add(group)
            # Customer.objects.create(user=user, name=user.username)
            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    non_closed_orders = orders.filter(Q(status='Abierta') | Q(status='En revisión'))
    opened = orders.filter(status='Abierta').count()
    on_revision = orders.filter(status='En revisión').count()
    closed = orders.filter(status='Cerrada').count()

    context = {'orders': non_closed_orders, 'customers': customers,
               'opened': opened, 'on_revision': on_revision, 'closed': closed}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['produccion'])
def userPage(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer)
    opened = orders.filter(status='Abierta').count()
    on_revision = orders.filter(status='En revisión').count()
    closed = orders.filter(status='Cerrada').count()

    context = {'orders': orders, 'opened': opened,
               'on_revision': on_revision, 'closed': closed,
               'customer': customer}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['produccion', 'mantenimiento'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mantenimiento', 'admin'])
def equipments(request):
    equipment = Equipment.objects.all()
    # TODO: Add Tags to the visualizer
    return render(request, 'accounts/equipment.html', {'equipment': equipment})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'produccion'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = Order.objects.filter(customer=customer)
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer,
               'orders': orders,
               'order_count': order_count,
               'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'produccion'])
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CreateOrderForm(initial={'customer': customer,
                                    'status': 'Abierta'})
    if request.method == "POST":
        form = CreateOrderForm(request.POST, initial={'customer': customer,
                                                      'status': 'Abierta'})
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = customer
            form.status = 'Abierta'
            form.save()
            return redirect("/")
        else:
            print("There is an error. Form is not valid")
    context = {"form": form}
    return render(request, 'accounts/create_order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'produccion', 'mantenimiento'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = UpdateOrderForm(instance=order)
    if request.method == 'POST':
        form = UpdateOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print("There is an error. Form is not valid")

    context = {'form': form}
    return render(request, 'accounts/update_order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
