from decimal import Context
from orders.models import Order, OrderProduct
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from cart.views import _cart_id
from cart.models import Cart, CartItem
import requests
from .models import Account
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id
                    product_variation = []
                    test1 = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                        test1.append(list(item.exclude(variation)))

                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    test = []

                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        test.append(list(item.exclude(id__in=existing_variation.id)))
                        id.append(item.id)
                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()


            except:
                pass
            auth.login(request, user)
            messages.success(request, 'Vous êtes maintenant connecté.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)                
            except:

                return redirect('shop:product_list')

        else:
            messages.error(request, 'Identifiants de connexion non valides')
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'Vous êtes maintenant déconnecté.')
    return redirect('accounts:login')

@login_required
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    context = {
        'orders_count':orders_count
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders':orders
    }
    return render(request, 'accounts/my_orders.html',context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Réinitialisation de votre mot de passe'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Un e-mail de réinitialisation du mot de passe a été envoyé à votre adresse e-mail.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Le compte n\'existe pas!')
            return redirect('accounts:forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Veuillez réinitialiser votre mot de passe')
        return redirect('accounts:resetPassword')
    else:
        messages.error(request, 'Ce lien a expiré!')
        return redirect('accounts:login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Réinitialisation du mot de passe réussie')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Les mot de passe ne correspondent pas!')
            return redirect('accounts:resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact=request.user.email)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Mot de passe modifié avec succes')
                return redirect('accounts:change_password')
            else:
                messages.error(request, 'veuillez entrer un mot de passe actuel valide')
                return redirect('accounts:change_password')

        else:
            messages.error(request, 'Les 2 nouveaux mot de passe ne correspondent pas')
            return redirect('accounts:change_password')

    return render(request, 'accounts/change_password.html')


@login_required
def order_detail(request,pk):
    #if pk:
        #order= OrderItem.objects.values_list('price').get(pk=pk)
    #    order= Order.objects.get(pk=pk)
    #else:
    #order = Order.objects.get(pk=pk)
    order = OrderProduct.objects.filter(order__pk=pk,user=request.user).order_by('-created_at')
    test = Order.objects.get(pk=pk)
   # orderitems = order.orderproduct.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context= {
        #'orderitems':orderitems
        'order':order,
        'test':test,
    }
    return render(request, 'accounts/order_detail.html', context)
