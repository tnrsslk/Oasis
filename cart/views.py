from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from shop.models import Product, Variation
from django.contrib import messages


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        request.session.create()
        cart_id = request.session.session_key

    # Update the Cart model's cart_id field
    cart, created = Cart.objects.get_or_create(cart_id=cart_id)
    
    return cart.cart_id


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    product_variation = []

    if current_user.is_authenticated:
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass

        is_cart_item_exist = CartItem.objects.filter(product=product, user=current_user).exists()

        # Проверка наличия товара на складе и его доступности
        if product.stock > 0 and product.is_available:
            if is_cart_item_exist:
                # Если товар уже есть в корзине пользователя
                cart_item = CartItem.objects.filter(product=product, user=current_user)
                ex_var_list = []
                id_list = []

                for item in cart_item:
                    existing_variation = item.variation.all()
                    ex_var_list.append(list(existing_variation))
                    id_list.append(item.id)

                if product_variation in ex_var_list:
                    # Увеличиваем количество товара в корзине
                    index = ex_var_list.index(product_variation)
                    item_id = id_list[index]
                    item = CartItem.objects.get(product=product, id=item_id)

                    # Добавляем новый товар в корзину пользователя
                    if item.quantity + 1 <= product.stock:
                        item.quantity += 1
                        item.save()
                    else:
                        messages.error(request, 'It is not possible to add more items than are in stock.')
                else:
                    # Если товара еще нет в корзине пользователя
                    if product.stock >= 1:
                        item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                        if len(product_variation) > 0:
                            item.variation.clear()
                            item.variation.add(*product_variation)
                        item.save()
                    else:
                        messages.error(request, 'The product is not available for purchase.')
            else:
                # Проверка на превышение доступного количества на складе
                if product.stock >= 1:
                    cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                    if len(product_variation) > 0:
                        cart_item.variation.clear()
                        cart_item.variation.add(*product_variation)
                    cart_item.save()
                else:
                    messages.error(request, 'The product is not available for purchase.')
            return redirect('cart:cart')
        else:
            messages.error(request, 'The product is not available for purchase.')
            return redirect('shop:product_details', category_slug=product.category.slug, product_details_slug=product.slug)



    else:  # Если пользователь не аутентифицирован
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                    variation_value__iexact=value)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # Получаем корзину по идентификатору из сессии
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        cart.save()

        is_cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exist:
            # Если товар уже есть в корзине
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id_list = []

            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id_list.append(item.id)

            if product_variation in ex_var_list:
                # Увеличиваем количество товара в корзине
                index = ex_var_list.index(product_variation)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)

                # Проверка на превышение доступного количества на складе
                if item.quantity + 1 <= product.stock:
                    item.quantity += 1
                    item.save()
                else:
                    messages.error(request, 'It is not possible to add more items than are in stock.')
            else:
                # Проверка на превышение доступного количества на складе
                if product.stock >= 1:
                    item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                    if len(product_variation) > 0:
                        item.variation.clear()
                        item.variation.add(*product_variation)
                    item.save()
                else:
                    messages.error(request, 'The product is not available for purchase.')
        else:
            # Проверка на превышение доступного количества на складе
            if product.stock >= 1:
                cart_item = CartItem.objects.create(
                    product=product,
                    quantity=1,
                    cart=cart,
                )
                if len(product_variation) > 0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)
                cart_item.save()
            else:
                messages.error(request, 'The product is not available for purchase.')

        return redirect('cart:cart')

# Функция для удаления товара из корзины
def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        if request.user.is_authenticated:
            # Если пользователь аутентифицирован
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            # Если пользователь не аутентифицирован
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        
        if cart_item.quantity > 1:
            # Если количество товара больше 1, уменьшаем количество
            cart_item.quantity -= 1
            cart_item.save()
        else:
            # Если количество товара равно 1, удаляем товар из корзины
            cart_item.delete()
    except:
        pass

    return redirect('cart:cart')



# Функция для удаления конкретного товара из корзины
def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        # Если пользователь аутентифицирован
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        # Если пользователь не аутентифицирован
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    
    cart_item.delete()
    return redirect('cart:cart')

# Функция для отображения корзины
def cart(request, total_price=0, quantity=0, cart_items=None):
    grand_total = 0
    tax = 0

    try:
        if request.user.is_authenticated:
            # Если пользователь аутентифицирован
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            # Если пользователь не аутентифицирован
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total_price += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    
    except ObjectDoesNotExist:
        pass
    
    # Вычисление налога и общей суммы заказа Налог рассчитывается как 2% от общей стоимости товаров в корзине
    tax = round(((2 * total_price) / 100), 2)
    grand_total = total_price + tax
    handling = 15.00 #В коде задается фиксированная стоимость обработки заказа в размере 15.00.
    total = float(grand_total) + handling

    context = {
        'total': total_price,
        'quantity': quantity,
        'cart_items': cart_items,
        'order_total': total,
        'vat': tax,
        'handling': handling,
    }

    return render(request, 'shop/cart/cart.html', context)
