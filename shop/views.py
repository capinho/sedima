from cart.models import CartItem
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.views import _cart_id
from .models import Category, Product,ProductAttribute
from django.db.models import Max,Min

@login_required        
def product_list(request, category_slug=None):
    user=request.user
    category = None
    categories = Category.objects.all().order_by('-id')
    products = Product.objects.filter(available=True)
    min_price = ProductAttribute.objects.aggregate(Min('price'))
    max_price = ProductAttribute.objects.aggregate(Max('price'))

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,'min_price':min_price,'max_price':max_price})

@login_required        
def product_detail(request,category_slugg,product_slugg):
    product = get_object_or_404(Product,
                                slug=product_slugg,
                                category__slug=category_slugg,
                                available=True)
    related_products = Product.objects.filter(category=product.category).exclude(slug=product_slugg)[:4]
    sizes = ProductAttribute.objects.filter(product=product).values('size__id','size__title','price').distinct()

    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'sizes':sizes,
                   'in_cart':in_cart,
                   'related_products':related_products})

@login_required        
def search(request):
    q = request.GET['q']
    products = Product.objects.filter(name__icontains=q).order_by('-id')
    return render(request,'shop/product/search.html', {'products':products})


