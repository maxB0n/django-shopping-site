# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # This says: "If they are at the base route, run the product_list view"
    path('', views.product_list, name='product_list'),
]