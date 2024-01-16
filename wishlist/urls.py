from django.urls import path
from .views import wishlist, add_to_wishlist, remove_from_wishlist

app_name = 'wishlist'

urlpatterns = [
    path('wishlist/', wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:wishlist_item_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
