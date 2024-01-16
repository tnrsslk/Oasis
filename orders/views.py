import json
import datetime
import uuid


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import QueryDict
from django.http import HttpResponseBadRequest
from .models import OrderProduct
from django.utils.datastructures import MultiValueDictKeyError

from cart.models import CartItem, Cart
from cart.views import _cart_id
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm
from .models import Order, OrderProduct
from cart.models import CartItem
from shop.models import Product
from django.urls import reverse


@login_required(login_url='accounts:login')
def payment_method(request):
    # Возвращает страницу с выбором метода оплаты
    return render(request, 'shop/orders/payment_method.html')


@login_required(login_url='accounts:login')
def checkout(request, total=0, total_price=0, quantity=0, cart_items=None):
    # Проверка корзины и перенаправление на страницу магазина, если корзина пуста
    tax = 0.00
    handling = 0.00
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total_price += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        total = total_price + 10

    except ObjectDoesNotExist:
        pass  # Просто игнорируем

    tax = round(((2 * total_price) / 100), 2)
    grand_total = total_price + tax
    handling = 15.00
    total = float(grand_total) + handling

    context = {
        'total_price': total_price,
        'quantity': quantity,
        'cart_items': cart_items,
        'handing': handling,
        'vat': tax,
        'order_total': total,
    }
    return render(request, 'shop/orders/checkout/checkout.html', context)


@login_required(login_url='accounts:login')
def payment(request, total=0, quantity=0):
    # Обработка оплаты заказа пользователя
    current_user = request.user
    handling = 15.0

    # Если корзина пуста, перенаправляем на страницу магазина
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('shop:shop')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = round(((2 * total) / 100), 2)

    grand_total = total + tax
    handling = 15.00
    total = float(grand_total) + handling

    if request.method == 'POST':
        print(request.POST)
        order_id = uuid.uuid4().hex[:10]

        # Combine form data and order_id
        request.POST = request.POST.copy()
        request.POST['order_id'] = order_id
        form = OrderForm(request.POST)
        print(form.errors)
        if form.is_valid():
            # Сохраняем всю биллинговую информацию в таблице Order
            data = Order()
            print("Form is valid")
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = total
            data.tax = tax
            data.order_id = order_id  # Assign the generated order ID
            data.ip = request.META.get('REMOTE_ADDR')

            data.save()

            # Предположим, что у вас есть поле order_id в модели Order
            order = get_object_or_404(Order, user=request.user, is_ordered=False, order_id=order_id)
            print("Order retrieved from database")

            context = {
                'order': order,
                'cart_items': cart_items,
                'handing': handling,
                'vat': tax,
                'order_total': total,
            }
            return render(request, 'shop/orders/checkout/payment.html', context)
        else:
            print(form.errors)
            ("Form is not valid")
            messages.error(request, 'Your information is not valid')
            return redirect('orders:checkout')

    else:
        return redirect('shop:shop')


def payments(request):
    if request.method == 'POST' and request.body:
        try:
            form_data = QueryDict(request.body)
            order_id = form_data.get('order_id')
            
            # Поиск заказа в базе данных
            order = get_object_or_404(Order, user=request.user, is_ordered=False, order_id=order_id)
            order.is_ordered = True
            order.save()

            # Перемещение товаров из корзины в таблицу OrderProduct
            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                orderproduct.user_id = request.user.id
                orderproduct.product_id = item.product_id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.price
                orderproduct.ordered = True
                orderproduct.save()

                # Добавление вариаций в таблицу OrderProduct
                cart_item = CartItem.objects.get(id=item.id)
                product_variation = cart_item.variation.all()
                orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                orderproduct.variations.set(product_variation)
                orderproduct.save()

                 # Уменьшение количества проданных товаров на складе
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

            # Очистка корзины
            CartItem.objects.filter(user=request.user).delete()

            # Очистка корзины
            request.session['order_id'] = order.order_id

            return redirect('orders:order_completed')

        except MultiValueDictKeyError:
            return JsonResponse({'error': 'Invalid request data'}, status=400)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': 'An error occurred while processing the payment'}, status=500)

    # Return a response if the request is not a POST request or if the body is empty
    return JsonResponse({'error': 'Invalid request'}, status=400)


from django.shortcuts import render

def order_completed(request):
     # Отображение шаблона завершенного заказа без получения order_id из сессии
    return render(request, 'shop/orders/order_completed/order_completed.html')
