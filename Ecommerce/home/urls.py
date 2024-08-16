from django.contrib import admin
from django.urls import path

from home import views

app_name ='home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', views.HomeView.as_view(), name='category_filter'),
    path('<slug:slug>/', views.ProductDetailView.as_view(),name='product_detail'),
    

]