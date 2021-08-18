from django.db import models
from shop.models import Product, ProductAttribute
from django.db.models import F, Sum
from accounts.models import Account
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(ProductAttribute, blank=True)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        return self.product.price * self.quantity

    @property
    def sub_total_variation(self):  
        return self.variations.aggregate(
            price_sum=Sum(self.quantity * F('price'))
        )['price_sum'] 

    def __str__(self):
        return self.product.name
