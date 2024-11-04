# models.py
from enum import unique
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.fields import ParentalManyToManyField
from django import forms
from ckeditor.fields import RichTextField 
from django.contrib.auth.models import User
from accounts.models import *





class Product(models.Model):
    """
    Simple single type product.
    """
    
    product_no = models.CharField(max_length=255, unique=True, null= True)

    name = models.CharField(max_length=255)
    link = models.CharField(max_length=800, null=True, blank=True,  unique=True)
    price = models.CharField(max_length=50, null=True, blank=True)

    Product_id = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_price(self, request):
        return self.price

    @property
    def code(self):
        return str(self.id)


    class Meta:
        unique_together = [ "name","link"]





class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='product_no')
    image =models.CharField(null=True, max_length=1800)
    image_cover =models.CharField(null=True, max_length=1800,blank=True)
    caption = models.CharField(blank=True, max_length=800, null=True)

    
class ProductDes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='product_no')
    shortdes = models.CharField(max_length=2400, null=True)
    fulldes = models.CharField(max_length=800, null=True)

class SellerInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='product_no')
    seller = models.CharField(max_length=80, null=True,blank=True)
    brand = models.CharField(max_length=80, null=True,blank=True)
    year = models.CharField(max_length=80, null=True,blank=True)
    country = models.CharField(max_length=80, null=True,blank=True)
    totalbuyer = models.CharField(max_length=80, null=True,blank=True)


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='product_no')
    price = models.CharField(max_length=80)
    saleprice = models.CharField(max_length=80, null=True)
    proprice = models.CharField(max_length=80, null=True,blank=True)
    m1 = models.CharField(max_length=80, null=True)
    m2 = models.CharField(max_length=80, null=True)

class SearchQuery(models.Model):
    id = models.AutoField(primary_key=True)  # Ensure that id is set as an AutoField.
    query = models.TextField(unique=True)
    status = models.CharField(max_length=20, default='Searching')
    updated_at = models.DateTimeField(auto_now=True)



# product sku color
class skucolor(models.Model):
    product = models.ForeignKey(Product, to_field='product_no', on_delete=models.CASCADE)
    color = models.CharField(max_length=220, null=True)
    image = models.ImageField(upload_to="static/images/", null=True,blank=True)

    class Meta:
        verbose_name_plural = 'product colors'

    def __str__(self):
        return self.product.name
class sku(models.Model):
    product = models.ForeignKey(Product, to_field='product_no', on_delete=models.CASCADE)
    name = models.CharField(max_length=220, null=True)
    option = models.CharField(max_length=220, null=True)

    class Meta:
        verbose_name_plural = 'product Skus'

    def __str__(self):
        return self.product.name


# product sku size
class skusize(models.Model):
    product = models.ForeignKey(Product, to_field='product_no', on_delete=models.CASCADE)
    color = models.CharField(max_length=120, null=True)
    size = models.CharField(max_length=120, null=True)
    price = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'product sizes'

    def __str__(self):
        return self.product.name



class Catagorys(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='product_no')
    catagory = models.CharField(blank=True, max_length=250)
    def __str__(self):
        return self.catagory


class CatagorysList(models.Model):
    image = models.ImageField(upload_to="static/images/", null=True,blank=True)
    CategorName = models.CharField(blank=True, max_length=250,unique=True)
    is_homepage_active = models.BooleanField(default=False)
    def __str__(self):
        return self.CategorName

class SubCatagorysList(models.Model):
    catagory = models.ForeignKey(CatagorysList, on_delete=models.CASCADE, to_field='CategorName',null=True)
    image = models.ImageField(upload_to="static/images/", null=True,blank=True)
    name = models.CharField(blank=True, max_length=250,unique=True)
    def __str__(self):
        return self.name


class add_to_carts(models.Model):

    User = models.ForeignKey(User, on_delete=models.CASCADE,to_field='id', null=True)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE, to_field='id')
    quantity =models.CharField(max_length=800, null=True)
    p_total = models.CharField(max_length=80, null=True)
    color = models.TextField(null=False)
    note  = models.CharField(max_length=80, null=True,blank=True)
    image = models.CharField(null=True, max_length=1800)




class user_pro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,to_field='id',null=True)
    full_name = models.CharField(max_length=800, null=True)
    phone = models.CharField(max_length=800, null=True)
    address = models.CharField(max_length=800, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

   

class categoryhome(models.Model):
    image = models.ImageField(upload_to="static/images/", null=True)
    catagory = models.CharField(max_length=800, null=True)

   




class description(models.Model):
    product = models.ForeignKey(Product, to_field='product_no', on_delete=models.CASCADE)
    des = models.TextField()

class reviews(models.Model):
    product = models.ForeignKey(Product, to_field='product_no', on_delete=models.CASCADE)
    Buyer_name = models.CharField(max_length = 245,null=True,blank=True)
    Country = models.CharField(max_length = 228,null=True,blank=True)
    Review_time = models.CharField(max_length = 228,null=True,blank=True)
    Review_text = models.TextField()
    Review_rating = models.TextField(null=True,blank=True)


