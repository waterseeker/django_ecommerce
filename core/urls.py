from django.urls import path
from .views import item_list, checkout, product

app_name = 'core'

urlpatterns = [
    path('', item_list, name='item_list.html'),
    path('checkout/', checkout, name='checkout.html'),
    path('product/', product, name='product.html'),
]
