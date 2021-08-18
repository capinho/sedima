from shop.models import Product, ProductAttribute
from accounts.models import Account
from django.db import models


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('En cours', 'En cours'),
        ('Traiter', 'Traiter'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
  #  payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    order_total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='En cours')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    full_name.short_description = ("Nom Complet")

    def __str__(self):
        return self.order_number

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
   # payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(ProductAttribute, blank=True)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=0)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_variations(self):
        return [v.size.title for v in self.variations.all()]
    get_variations.short_description = ("Variations")

    def __str__(self):
        return self.product.name

    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
  
    def sub_total(self):
        return self.product_price * self.quantity
