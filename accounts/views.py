from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from .models import Customer, Equipment, Order
from django.contrib.auth.forms import UserCreationForm
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user, name=user.username)
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
    opened = orders.filter(status='Abierta').count()
    on_revision = orders.filter(status='En revisión').count()
    closed = orders.filter(status='Cerrada').count()

    context = {'orders': orders, 'customers': customers,
               'opened': opened, 'on_revision': on_revision, 'closed': closed}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    opened = orders.filter(status='Abierta').count()
    on_revision = orders.filter(status='En revisión').count()
    closed = orders.filter(status='Cerrada').count()

    context = {'orders': orders, 'opened': opened,
               'on_revision': on_revision, 'closed': closed}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
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
@allowed_users(allowed_roles=['admin'])
def equipments(request):
    equipment = Equipment.objects.all()
    # TODO: Add Tags to the visualizer
    return render(request, 'accounts/equipment.html', {'equipment': equipment})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = Order.objects.filter(customer=customer)

    # orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders,
               'order_count': order_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {"form": form}
    # TODO: Fix input to get default value as the current customer
    # print("PK:", pk)
    # OrderFormSet = inlineformset_factory(Customer, Order, fk_name="customer",
    #                                      fields=('equipo', 'status'), extra=10)
    # print("OrderFormSet:", OrderFormSet)
    # customer = Customer.objects.get(id=pk)
    # print("Customer: ", customer)
    # # form = OrderForm(initial={'customer': customer})
    # formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # if request.method == 'POST':
    #     # print('Printing POST', request.POST)
    #     formset = OrderFormSet(request.POST, instance=customer)
    #     if formset.is_valid():
    #         formset.save()
    #         return redirect('/')

    # context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        # print('Printing POST', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
