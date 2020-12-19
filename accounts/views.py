from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from . forms import OrderForm
from .filters import OrderFilter

from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


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
			#Added username after video because of error returning customer name if not added
			Customer.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def logistic(request):

	ordersofd = Order.objects.filter(status='Out for delivery').order_by('-date_created')
	ordersp = Order.objects.filter(status='Pending').order_by('-date_created')
	ordersd = Order.objects.filter(status='Delivered').order_by('-date_created')
	
	#orders = Order.objects.all().order_by('-status')
	
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = Order.objects.all().count()
	delivered = Order.objects.filter(status='Delivered').count()
	pending = Order.objects.filter(status='Pending').count()



	#context = {'customers':customers, 'orders':orders,
	context = {'customers':customers, 'ordersofd':ordersofd, 'ordersp':ordersp,'ordersd':ordersd,
	'total_customers':total_customers,'total_orders':total_orders, 
	'delivered':delivered, 'pending':pending}
	#'delivered':delivered, 'pending':pending}
	return render(request, 'accounts/logistic.html', context)




def designer(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'accounts/designer.html', context)
	
	
def company(request):
	action = 'create'
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	customer = request.POST.get('customer')
	product = request.POST.get('product')
	status = request.POST.get('status')
	
	
	ordersofd = Order.objects.filter(status='Out for delivery').order_by('-date_created')
	ordersp = Order.objects.filter(status='Pending').order_by('-date_created')
	ordersd = Order.objects.filter(status='Delivered').order_by('-date_created')
	
	context =  {'action':action, 'form':form, 'ordersofd':ordersofd, 'ordersp':ordersp,'ordersd':ordersd}
	
	
	
	
	
	#context = {}
	return render(request, 'accounts/company.html', context)

#-------------------(DETAIL/LIST VIEWS) -------------------


@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all().order_by('-status')[0:5]
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = Order.objects.all().count()
	delivered = Order.objects.filter(status='Delivered').count()
	pending = Order.objects.filter(status='Pending').count()



	context = {'customers':customers, 'orders':orders,
	'total_customers':total_customers,'total_orders':total_orders, 
	'delivered':delivered, 'pending':pending}
	return render(request, 'accounts/dashboard.html', context)





@login_required(login_url='login')
def products(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'accounts/products.html', context)


def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	total_orders = orders.count()



	orderFilter = OrderFilter(request.GET, queryset=orders) 
	orders = orderFilter.qs

	context = {'customer':customer, 'orders':orders, 'total_orders':total_orders,
	'filter':orderFilter}
	return render(request, 'accounts/customer.html', context)
	
	


#-------------------(CREATE VIEWS) -------------------
def createOrder(request):
	action = 'create'
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context =  {'action':action, 'form':form}
	return render(request, 'accounts/order_form.html', context)

#-------------------(UPDATE VIEWS) -------------------
def updateOrder(request, pk):
	action = 'update'
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context =  {'action':action, 'form':form}
	return render(request, 'accounts/order_form.html', context)

#-------------------(DELETE VIEWS) -------------------

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		customer_id = order.customer.id
		customer_url = '/customer/' + str(customer_id)
		order.delete()
		return redirect(customer_url)
		
	return render(request, 'accounts/delete_item.html', {'item':order})
