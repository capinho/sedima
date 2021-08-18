from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from django.utils.html import mark_safe
from io import BytesIO
from PIL import Image
from django.core.files import File
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Size(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title


class Product(models.Model):

    category = models.ForeignKey(Category,
                                 related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
   #image = models.ImageField(upload_to='products/%Y/%m/%d',null=True,blank=True)
    #image = CloudinaryField('image', null=True,blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',null=True,blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = _('Produit')
        verbose_name_plural = _('Produits')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.category.slug, self.slug])       

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))       


    
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return self.size.title

    def image_tag1(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.product.image.url))       

