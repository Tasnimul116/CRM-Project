from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users,admin_only
from .forms import OrderForm,CreateUserForm,CustomerForm


@unauthenticated_user
def registerPage(request):

        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user= form.save()
                username = form.cleaned_data.get('username')

               

                messages.success(request,'Account was created for '+username)
                return redirect('loginPage')

        context={'form':form}
        return render (request,'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
        
        if request.method =="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request,username = username, password= password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Username or Password is incorrect')

        context={}
        return render (request,'accounts/login.html',context)



@login_required(login_url='loginPage')
def logoutUser(request):
    logout(request)
    return redirect('loginPage')

@login_required(login_url='loginPage')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count() 

    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='pending').count()

    context= {'orders':orders , 'customers':customers, 'total_customers':total_customers,'total_orders': total_orders,'delivered':delivered,'pending':pending}

    return render(request, 'accounts/dashboard.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['customer'])
def userPage(request):



    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='pending').count()

    print('ORDERS: ',orders)
    context={'orders':orders,'total_orders': total_orders,'delivered':delivered,'pending':pending}
    return render (request,'accounts/user.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer= request.user.customer
    form= CustomerForm(instance=customer)
    if request.method== "POST":
        form= CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context={'form':form}
    return render(request,'accounts/account_settings.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def products(request):

    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk_no):
    customer = Customer.objects.get(id=pk_no)
    orders = customer.order_set.all()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders= myFilter.qs
    context ={'customer':customer, 'orders':orders,'myFilter':myFilter}
    return render(request, 'accounts/customer.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk): 
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'), extra=4)
    customer = Customer.objects.get(id=pk)
    #form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method =="POST":
        #print ("printing POST",request.POST)
        #form= OrderForm(request.POST)
        formset = OrderFormSet( request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect("/")


    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance= order)

    if request.method =="POST":
        form= OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")


    context={'form':form}
    return render(request,"accounts/order_form.html",context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method=="POST":
        order.delete()
        return redirect("/")


    context={'item':order}
    return render (request, 'accounts/delete.html',context)