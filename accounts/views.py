from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, F, Max, Min, Window, ExpressionWrapper, fields
from django.utils import timezone
from django.db.models.functions import Now, Extract
from datetime import datetime


from .models import Customer, Equipment, Order, Images, Videos, OrderComments
from .forms import (CreateOrderForm, UpdateOrderForm, CreateUserForm, CustomerForm,
                    UpdateImageForm, UpdateVideoForm, CreateOrderCommentForm)
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

    duration = ExpressionWrapper(Now() - F('date_created'),
                                 output_field=fields.DurationField())
    non_closed_orders = non_closed_orders.annotate(duration=duration)
    non_closed_orders = non_closed_orders.annotate(duration_days=Extract('duration', 'day'))

    context = {'orders': non_closed_orders, 'customers': customers,
               'opened': opened, 'on_revision': on_revision,
               'closed': closed, 'to_date': datetime.now()}
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
    form_image = UpdateImageForm()
    form_video = UpdateVideoForm()
    if request.method == "POST":
        form = CreateOrderForm(request.POST, initial={'customer': customer,
                                                      'status': 'Abierta'})
        form_image = UpdateImageForm(request.POST, request.FILES)
        form_video = UpdateVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = customer
            form.status = 'Abierta'
            form.save()
            order = Order.objects.get(id=form.pk)
            if form_image.is_valid():
                for img in request.FILES.getlist('images'):
                    Images.objects.create(order=order, image=img)
            if form_video.is_valid():
                for vid in request.FILES.getlist('videos'):
                    Videos.objects.create(order=order, video=vid)
            return redirect("/")
        else:
            print("There is an error. Form is not valid")
    context = {'form': form,
               'form_image': form_image,
               'form_video': form_video}
    return render(request, 'accounts/create_order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'produccion', 'mantenimiento'])
def updateOrder(request, pk):
    customer = request.user.customer
    order = Order.objects.get(id=pk)
    form = UpdateOrderForm(instance=order)
    form_comment = CreateOrderCommentForm(initial={'order': order,
                                                   'customer': customer})
    order_images = Images.objects.filter(order=order).values_list('image').values
    order_videos = Videos.objects.filter(order=order).values_list('video').values
    form_image = UpdateImageForm()
    form_video = UpdateVideoForm()
    order_comments = OrderComments.objects.filter(order=order)
    dict_comments = []
    for comment in order_comments:
        curr_customer = Customer.objects.get(id=comment.author_id)
        dict_comments.append({'author': curr_customer.name,
                              'fecha': comment.date_created,
                              'description': comment.descripcion})
    if request.method == 'POST':
        form = UpdateOrderForm(request.POST, instance=order)
        form_comment = CreateOrderCommentForm(request.POST,
                                              initial={'order': order,
                                                       'author': customer})
        form_image = UpdateImageForm(request.POST, request.FILES)
        form_video = UpdateVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if form.status == "Cerrada":
                form.date_closed = timezone.now()
            if form_comment.is_valid():
                form_comment = form_comment.save(commit=False)
                form_comment.order = order
                form_comment.author = customer
                if form_image.is_valid():
                    for img in request.FILES.getlist('images'):
                        Images.objects.create(order=order, image=img)
                if form_video.is_valid():
                    for vid in request.FILES.getlist('videos'):
                        Videos.objects.create(order=order, video=vid)
                form.save()
                form_comment.save()
            return redirect('/')
        else:
            print("There is an error. Form is not valid")
    context = {'form': form,
               'form_comment': form_comment,
               'order_images': order_images,
               'order_videos': order_videos,
               'dict_comments': dict_comments,
               'form_image': form_image,
               'form_video': form_video,
               }
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
