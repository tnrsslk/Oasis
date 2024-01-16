from django.shortcuts import render, get_object_or_404, redirect
from .models import Wishlist
from shop.models import Product
from django.contrib import messages
from django.urls import reverse

def wishlist(request):
    if request.user.is_authenticated:
        # Получаем все элементы избранного для текущего пользователя
        wishlist_items = Wishlist.objects.filter(user=request.user)
        return render(request, 'shop/wishlist/wishlist.html', {'wishlist_items': wishlist_items})
    else:
        messages.warning(request, 'Please register to use the wishlist.')
        return redirect(reverse('accounts:register'))  


def add_to_wishlist(request, product_id):
    if request.user.is_authenticated:
        # Получаем продукт по его идентификатору
        product = get_object_or_404(Product, id=product_id)
        # Получаем или создаем объект Wishlist для данного пользователя и продукта
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if not created:
            messages.warning(request, 'This item is already in your wishlist.')
        else:
            messages.success(request, 'Item added to your wishlist.')

        return redirect('shop:product_details', category_slug=product.category.slug, product_details_slug=product.slug)
    else:
        messages.warning(request, 'Please register to add items to your wishlist.')
        return redirect(reverse('accounts:register')) 


def remove_from_wishlist(request, wishlist_item_id):
    if request.user.is_authenticated:
        wishlist_item = get_object_or_404(Wishlist, id=wishlist_item_id, user=request.user)
        wishlist_item.delete()
        messages.success(request, 'Item removed from your wishlist.')
    else:
        messages.warning(request, 'Please log in to remove items from your wishlist.')

    return redirect('wishlist:wishlist')
