from django.urls import path
from . import views

urlpatterns = [
	path('', views.store, name="store-home"),
    path('about/', views.store , name='store-about'),

    path('menu1/', views.store , name='menu1'),
    path('menu2/', views.store , name='menu2')

]