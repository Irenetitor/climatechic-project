import datetime
import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from store.models import Order, OrderItem, Product, ShippingAddress
from store.utils import cartData, guestOrder, get_weather_data


# Create your views here.

# Function to fetch product data from the API
def fetch_products_from_api():
	response = requests.get('https://dummyjson.com/products')
	if response.status_code == 200:
		return response.json().get('products', [])
	return []

def store(request):
	data = cartData(request)
	cartItems = data['cartItems']

	# Fetch products from the API
	# products = fetch_products_from_api()

	# Fetch products from the database
	products = Product.objects.all()

	# Fetch weather data
	city = 'London'
	weather_data = get_weather_data(city, settings.WEATHER_API_KEY)
	print (weather_data['main']['temp'])

	# Filter products based on weather
	if weather_data:
		# temp = weather_data['main']['temp']
		temp = 25
		if temp < 10:
			products = products.filter(category='winter')
		elif temp < 20:
			products = products.filter(category='autumn')
		else:
			products = products.filter(category='summer')

	context = {'products': products, 'cartItems': cartItems}
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
