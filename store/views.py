import datetime
import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from store.models import Order, OrderItem, Product, ShippingAddress
from store.utils import cartData, guestOrder, get_weather_data


def store(request):
	data = cartData(request)
	cartItems = data['cartItems']

	# Get city from request
	city = request.GET.get('city', 'Dublin')  # Default to 'Dublin' if no city is provided

	# Fetch weather data
	weather_data = get_weather_data(city, settings.WEATHER_API_KEY)
	if not weather_data:
		context = {'products': [], 'cartItems': cartItems, 'city': None, 'error': 'Invalid city name. Please enter a valid city.'}
		return render(request, 'store/store.html', context)

	temp = weather_data['main']['temp'] if weather_data else 25  # Default to 25 if no weather data

	# Filter products based on weather
	if temp < 10:
		products = Product.objects.filter(category='winter')
	elif temp < 20:
		products = Product.objects.filter(category='autumn')
	else:
		products = Product.objects.filter(category='summer')

	context = {'products': products, 'cartItems': cartItems, 'city': city}
	return render(request, 'store/store.html', context)

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customerprofile
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Item was updated', safe=False)

def processOrder(request): 
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customerprofile
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = datetime.datetime.now().timestamp()

	# Verify cart total is same in db
	if total == order.get_cart_total:
		order.complete = True
	order.save()

	ShippingAddress.objects.create(
	customer=customer,
	order=order,
	address=data['shipping']['address'],
	city=data['shipping']['city'],
	state=data['shipping']['state'],
	zipcode=data['shipping']['zipcode'],
	)
	
	return JsonResponse('Payment submitted..', safe=False)

def about(request):
	return render(request, 'store/about.html')

def contact(request):
	context = {}
	return render(request, 'store/contact.html')
