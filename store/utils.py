import json

from store.models import Order, Product


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