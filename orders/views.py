from cart.models import CartItem
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import views as auth_views

from .forms import *
from .models import *
from .task import *
from datetime import timedelta
import datetime
from datetime import date

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Order, Payment, OrderProduct


# @login_required
# def list_commande(request):
#     #filter = OrderFilter(request.GET, queryset=OrderItem.objects.select_related('product').filter(order__user=request.user))
#     listorderuser = Order.objects.filter(user=request.user).order_by('created')
#     return render(request, 'orders/order/list.html', {'listorderuser':listorderuser})

# @login_required
# def view_list(request,pk):
#     #if pk:
#         #order= OrderItem.objects.values_list('price').get(pk=pk)
#     #    order= Order.objects.get(pk=pk)
#     #else:
#     order = Order.objects.get(pk=pk)
#     orderitems = order.items.all()
#     total = order.items.aggregate(Sum('price'))

#     return render(request, 'orders/order/detail_list.html', {'orderitems':orderitems,'total':total,})

# @login_required
# def order_create(request):
#     user=request.user
#     todayDate = datetime.date.today()
#     current_month = todayDate.month
#     current_day = todayDate.day
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             if Order.objects.filter(created__month=current_month,user=user):
#                 return redirect('/', messages.error(request, 'Vous avez deja fait une commande ce mois ci','alert-danger'))
#             else:
#                 order.user=user
#                 order.save()
#                 for item in cart:
#                         OrderItem.objects.create(order=order,
#                                                 product=item['product'],
#                                                 price=item['price'],
#                                                 quantity=item['quantity'])
#                 # effacer panier
#                 cart.clear()
#                 if user.email!='':
#                     order_created(order.id)
#                     request.session['order_id'] = order.id
#                     return redirect('/', messages.success(request, 'Votre commande a été prise avec succes', 'alert-success'))
#                 else:
#                     request.session['order_id'] = order.id
#                     # redirect to the payment
#                     #return redirect('payment:process')
#                     return redirect('/', messages.success(request, 'Votre commande a été prise avec succes', 'alert-success'))


#     else:
#         form = OrderCreateForm()
#     return render(request,
#                   'orders/order/create.html',
#                   {'cart': cart, 'form': form})

def place_order(request, grand_total=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    todayDate = datetime.date.today()
    current_month = todayDate.month
    current_day = todayDate.day

    if cart_count <= 0:
        return redirect('shop:product_list')

    for cart_item in cart_items:
        if cart_item.variations.all():
            for i in cart_item.variations.all():
                grand_total += (i.price * cart_item.quantity)
        else:
                grand_total += (cart_item.product.price * cart_item.quantity)

    if request.method == 'POST':
        # Store all the billing information inside Order table
        if current_user.status=='is_collaborateur':
            if grand_total > 50000:
                messages.error(request, 'votre statut ne vous permet pas de depasser 50000 FCFA de commande')
                return redirect('cart:cart')


        if Order.objects.filter(created_at__month=current_month,user=current_user,is_ordered=True):
            messages.error(request, 'Vous avez deja fait une commande ce mois ci')
            return redirect('shop:product_list')
        else:
            data = Order()
            data.user = current_user
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
                # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.is_ordered = True
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=True, order_number=order_number)

            # Move the cart items to Order Product table
            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
    #            orderproduct.payment = payment
                orderproduct.user_id = current_user.id
                orderproduct.product_id = item.product_id
                orderproduct.quantity = item.quantity
                if item.variations.all():
                    for i in item.variations.all():
                        orderproduct.product_price = i.price
                else:
                    orderproduct.product_price = item.product.price
                orderproduct.ordered = True
                orderproduct.save()

                cart_item = CartItem.objects.get(id=item.id)
                product_variation = cart_item.variations.all()
                orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                orderproduct.variations.set(product_variation)
                orderproduct.save()

            # Clear cart
            CartItem.objects.filter(user=request.user).delete()

            # Send order recieved email to customer
            mail_subject = 'Nous vous remercions de votre commande!'
            message = render_to_string('orders/order_recieved_email.html', {
                'user': request.user,
                'order': order,
            })
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            try:
                ordered_products = OrderProduct.objects.filter(order_id=order.id)
                subtotal = 0
                for i in ordered_products:
                    subtotal += i.product_price * i.quantity

                context = {
                    'order': order,
                    'ordered_products': ordered_products,
                    'order_number': order.order_number,
                    'subtotal': subtotal,
                }
                return render(request, 'orders/order_complete.html', context)
            except (Order.DoesNotExist):
                return redirect('cart:checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity


        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Order.DoesNotExist):
        return redirect('shop:product_list')
