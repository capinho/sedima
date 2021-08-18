import re

from django.contrib import messages
import cart
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from shop.models import Product, ProductAttribute, Size
from .models import Cart
from cart.models import CartItem
from django.db.models import F, Sum



from django.core.exceptions import ObjectDoesNotExist

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product

    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            # size = request.POST['size']
            # if size ==" ":
            #     messages.error(request, 'veuillez choisir une taille de poulets')
            #     return redirect()
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = ProductAttribute.objects.get(product=product,size__title__iexact=value)
                    product_variation.append(variation)
                except :
                    pass            

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user=current_user
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart:cart')
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = ProductAttribute.objects.get(product=product,size__title__iexact=value)
                    product_variation.append(variation)
                except :
                    pass            
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart:cart')






def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart:cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart:cart')


def cart_detail(request, grand_total=0, quantity=0, cart_items=None):

    try:
                
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by('-id')
            for cart_item in cart_items:
                if cart_item.variations.all():
                    for i in cart_item.variations.all():
                       grand_total += (i.price * cart_item.quantity)
                else:
                      grand_total += (cart_item.product.price * cart_item.quantity)
                
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('-id')
            for cart_item in cart_items:
                if cart_item.variations.all():
                    for i in cart_item.variations.all():
                        grand_total += (i.price * cart_item.quantity)
                else:
                    grand_total += (cart_item.product.price * cart_item.quantity)
                    

    except ObjectDoesNotExist:
        pass
    context = {
       # 'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total':grand_total

    }
    return render(request, 'cart/detail.html', context)


@login_required
def checkout(request, grand_total=0, quantity=0, cart_items=None):
    try:

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by('-id')
            for cart_item in cart_items:
                if cart_item.variations.all():
                    for i in cart_item.variations.all():
                       grand_total += (i.price * cart_item.quantity)
                else:
                      grand_total += (cart_item.product.price * cart_item.quantity)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('-id')
            for cart_item in cart_items:
                if cart_item.variations.all():
                    for i in cart_item.variations.all():
                        grand_total += (i.price * cart_item.quantity)
                else:
                    grand_total += (cart_item.product.price * cart_item.quantity)

    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        #'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
    }
    return render(request, 'shop/checkout.html', context)
