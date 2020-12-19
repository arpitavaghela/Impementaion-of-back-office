from django.urls import path
from . import views





urlpatterns = [
	path('', views.home, name="home"),
	path('products/', views.products, name="products"),
	path('customer/<str:pk>/', views.customer, name="customer"),

	path('create_order/', views.createOrder, name="create_order"),  
	path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
	path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
	
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
	path('designer', views.designer, name="designer"),
	
	path('company/', views.company, name="company"),
	path('logistic/', views.logistic, name="products"),
	
	path('products', views.products, name="products")



]
