from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('wishlist/', include('wishlist.urls', namespace='wishlist')),
]

# Добавление маршрутов для обработки медиафайлов (изображений и т. д.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Добавление маршрутов для обработки статических файлов (CSS, JavaScript и т. д.)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)