from cart.views import _cart_id
from cart.models import Cart,CartItem


def counter(request):
    totals = 0
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
                for cart_item in cart_items:
                    if cart_item.variations.all():
                        for i in cart_item.variations.all():
                            totals += (i.price * cart_item.quantity)
                    else:
                        totals += (cart_item.product.price * cart_item.quantity)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.all().filter(cart=cart)
                for cart_item in cart_items:
                    if cart_item.variations.all():
                        for i in cart_item.variations.all():
                            totals += (i.price * cart_item.quantity)
                    else:
                        totals += (cart_item.product.price * cart_item.quantity)

            for cart_item in cart_items:
                cart_count += cart_item.quantity
           
        except(Cart.DoesNotExist): 
            cart_count = 0
            totals = 0
    return dict(cart_count=cart_count, totals=totals)

