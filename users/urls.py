from django.urls import path
from users import views
from django.contrib.auth import views as auth_views


urlpatterns = [
   path('', views.home , name='store-home'),
   path('about/', views.home , name='store-about'),
   
   path('login/', views.user_login , name='login'),
   path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

   path('register/', views.register , name='register'),
   path('profile/', views.user_profile , name='profile'),

   path('password-reset/', views.home , name='password_reset'),
   path('menu1/', views.home , name='menu1'),
   path('menu2/', views.home , name='menu2')

]