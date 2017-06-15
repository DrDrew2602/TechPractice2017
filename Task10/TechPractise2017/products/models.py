from django.contrib.auth.models import User
from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категория товаров'


class Product(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    countVoice = models.IntegerField( default=0)
    discount = models.IntegerField(default=0)
    user = models.ForeignKey(User, null=True, default= None)
    category = models.ForeignKey(ProductCategory, blank=True, null=True, default=None)
    short_description = models.TextField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s, %s" % (self.countVoice, self.name)

    class Meta:
        verbose_name = 'Петиция'
        verbose_name_plural = 'Петиции'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    image = models.ImageField(upload_to='products_images/')
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

class votes(models.Model):
    user = models.ForeignKey(User,null=False)
    petition = models.ForeignKey(Product,null=False)

class comment(models.Model):
    user = models.ForeignKey(User,null=False)
    petition = models.ForeignKey(Product,null=False)
    description = models.TextField( null=True, default=None)
