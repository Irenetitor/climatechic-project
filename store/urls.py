from django.urls import path
from . import views

urlpatterns = [
	path('', views.store, name="store-home"),
	path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('about/', views.store , name='store-about'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path('menu1/', views.store , name='menu1'),
    path('menu2/', views.store , name='menu2')

]