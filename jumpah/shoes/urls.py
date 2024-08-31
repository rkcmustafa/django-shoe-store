from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.shoes, name="products"),
    path('favorites/', views.favorites, name="favorites"),
    path('basket/', views.basket, name="basket"),
    path('<slug:slug>/', views.shoe, name="shoe")
]
