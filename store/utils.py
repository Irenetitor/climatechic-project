import json
import requests

from store.models import Order, OrderItem, Product
from users.models import CustomerProfile


def cookieCart(request):
    #Create empty cart for guest user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':True}
    cartItems = order['get_cart_items']

    for i in cart:
        # prevent items in cart that may have been removed from causing error
        try:	
            if(cart[i]['quantity']>0):  
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                'id':product.id,
                'product':{'id':product.id,'name':product.name, 'price':product.price, 
                'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
                'get_total':total,
                }
                items.append(item)
        except:
             pass

    return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customerprofile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems ,'order':order, 'items':items}

def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    # Create a customer profile for guest user
    customer, created = CustomerProfile.objects.get_or_create(
            email=email,
            )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
        )

    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order

def get_weather_data(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None