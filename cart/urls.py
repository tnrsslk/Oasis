from django.urls import path
from . import views as cart_views  # Use alias 'cart_views' for the cart app views
from shop import views as shop_views  # Use alias 'shop_views' for the shop app views

app_name = 'cart'

urlpatterns = [
    path('', cart_views.cart, name='cart'),
    path('add_cart/<int:product_id>/', cart_views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', cart_views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', cart_views.remove_cart_item, name='remove_cart_item'),
    path('shop/<slug:category_slug>/<slug:product_details_slug>/', shop_views.product_details, name='product_details'),
]
