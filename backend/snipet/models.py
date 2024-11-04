from django.db import models
from store.models import *
from ckeditor.fields import RichTextField
# Create your models here.


class D_Rate(models.Model):
    usdTotk = models.CharField(max_length = 228,null=True,blank=True)
    class Meta:
        verbose_name = "Dollar Rate"
        verbose_name_plural = "Dollar Rate"


class shipformedes(models.Model):
    China = models.TextField(max_length=800, null=True)
    USA = models.TextField(max_length=800, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Ship for me Description"
        verbose_name_plural = "Ship for me Description"
        
class shipformemesssages(models.Model):
    China = models.TextField(max_length=800, null=True)
    USA = models.TextField(max_length=800, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Ship for me Message"
        verbose_name_plural = "Ship for me Message"
    
class shipformecharge(models.Model):
    China_charge = models.TextField(max_length=800, null=True)
    China_days = models.TextField(max_length=800, null=True)
    USA_charge = models.TextField(max_length=800, null=True,blank=True)
    USA_days = models.TextField(max_length=800, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Ship for me Shipping Charge"
        verbose_name_plural = "Ship for me Shipping Charge"

class shipformenote(models.Model):
    Description = models.TextField(max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Ship for me Note"
        verbose_name_plural = "Ship for me Note"
    def __str__(self):
        return self.Description
class reqsnote(models.Model):
    Description = models.TextField(max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Request Order Note"
        verbose_name_plural = "Request Order Note"
    def __str__(self):
        return self.Description

    


class payformenote(models.Model):
    Description = models.TextField(max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Pay For Me Note"
        verbose_name_plural = "Pay For Me Note"
    def __str__(self):
        return self.Description


class Site_Identity(models.Model):
    logo = models.ImageField(upload_to="static/images/", null=True,blank=True)
    icon = models.ImageField(upload_to="static/images/", null=True,blank=True)
    name = models.CharField(max_length=120,null=True,blank=True)
    phone = models.CharField(max_length=120,null=True,blank=True)
    mail = models.CharField(max_length=120,null=True,blank=True)
    page_link = models.CharField(max_length=120,null=True,blank=True)
    wp_link = models.CharField(max_length=120,null=True,blank=True)
    tag_line = models.CharField(max_length=120,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Site Identity"
        verbose_name_plural = "Site Identity"

class FooterWidget(models.Model):
    logo = models.ImageField(upload_to="static/images/", null=True,blank=True)
    name = models.CharField(max_length=120,null=True,blank=True)
    slogan = RichTextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Footer Weight"
        verbose_name_plural = "Footer Weight"

class FooterPaymentSuportImage(models.Model):
    logo = models.ImageField(upload_to="static/images/", null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Footer Payment Method Image"
        verbose_name_plural = "Footer Payment Method Image"

class FooterLinks(models.Model):
    name = models.CharField(max_length=120)
    url = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Footer Other Page Links"
        verbose_name_plural = "Footer Other Page Links"

class Home_Banneer(models.Model):
    image = models.ImageField(upload_to="static/images/", null=True,blank=True)
    name = models.CharField(max_length=120,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Home Page Banners"
        verbose_name_plural = "Home Page Banners"

class Home_top600px_Banneer(models.Model):
    image = models.ImageField(upload_to="static/images/", null=True,blank=True)
    name = models.CharField(max_length=120,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Home Page  600px Banners"
        verbose_name_plural = "Home Page  600px Banners"

class Home_middel502x202px_Banneer(models.Model):
    image = models.ImageField(upload_to="static/images/", null=True,blank=True)
    title = models.CharField(max_length=120,null=True,blank=True)
    slogan = RichTextField()
    url = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Home Page  502px * 202px Banners"
        verbose_name_plural = "Home Page  502px * 202px Banners"

class Home_middel680x180px_Banneer(models.Model):
    image = models.ImageField(upload_to="static/images/", null=True,blank=True)
    name = models.CharField(max_length=120,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Home Page  1680px * 180px Banners"
        verbose_name_plural = "Home Page  1680px * 180px Banners"
    
class Home_sliding_selling_text_Banneer(models.Model):
    name = models.CharField(max_length=224,null=True,blank=True)
    Scorlling_Text = models.CharField(max_length=224,null=True,blank=True)
    url = models.CharField(max_length=224,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Home Page  Slidign Sccrolling Text"
        verbose_name_plural = "Home Page  Slidign Sccrolling Text"
    
class Home_4data_breadcum(models.Model):
    name = models.CharField(max_length=224,null=True,blank=True)
    Text = models.CharField(max_length=224,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Home Page Top 4 Data"
        verbose_name_plural = "Home Page Top 4 Data"

class Home_bottom_sites_Banneer(models.Model):
    image = models.ImageField(upload_to="static/images/", null=True,blank=True)
    name = models.CharField(max_length=120,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Home Page Bottom Banner"
        verbose_name_plural = "Home Page Bottom Banner"

class Home_Faq(models.Model):
    question = models.CharField(max_length=120,null=True,blank=True)
    answer = models.TextField(max_length=120,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Home Page FAQ"
        verbose_name_plural = "Home Page FAQ"

class Payment_numbers(models.Model):
    bkash = models.CharField(max_length=120,null=True,blank=True)
    Nagad = models.CharField(max_length=120,null=True,blank=True)
    bank = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Payment Method Data"
        verbose_name_plural = "Payment Method Data"

class Google_Tag_Manager(models.Model):
    head = models.TextField(null=True,blank=True)
    body = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Head Body Code Snipet For SEO"
        verbose_name_plural = "Head Body Code Snipet For SEO"


class Faq_page(models.Model):
    question = models.CharField(max_length=120,null=True)
    answer = RichTextField(null=True,
                            external_plugin_resources=[(
                            "youtube",
                            "/static/base/vendor/skeditor plugins/youtube/youtube/",
                            "plugin.js",
                            )],
                           )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "FAQ Page Questions & Answers"
        verbose_name_plural = "FAQ Page Questions & Answers"


class forbidenitempagen_page(models.Model):
    Item_Name = RichTextField(null=True,
                            external_plugin_resources=[(
                            "youtube",
                            "/static/base/vendor/skeditor plugins/youtube/youtube/",
                            "plugin.js",
                            )],
                           )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Forbidden Item Import From Abroad"
        verbose_name_plural = "Forbidden Item Import From Abroad"

class terms_condition_page(models.Model):
    question = models.CharField(max_length=120,null=True,blank=True)
    answer = RichTextField(null=True,
                            external_plugin_resources=[(
                            "youtube",
                            "/static/base/vendor/skeditor plugins/youtube/youtube/",
                            "plugin.js",
                            )],
                           )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Terms & Condition Page Question & Answer"
        verbose_name_plural = "Terms & Condition Page Question & Answer"

class Shipping_refund_Pollicy_page(models.Model):
    question = models.CharField(max_length=120,null=True,blank=True)
    answer = RichTextField(null=True,
                            external_plugin_resources=[(
                            "youtube",
                            "/static/base/vendor/skeditor plugins/youtube/youtube/",
                            "plugin.js",
                            )],
                           )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Shipping Refund Policy Page Question & Answer"
        verbose_name_plural = "Shipping Refund Policy Page Question & Answer"

class Privacy_Policy_page(models.Model):
    question = models.CharField(max_length=120,null=True,blank=True)
    answer = RichTextField(null=True,
                            external_plugin_resources=[(
                            "youtube",
                            "/static/base/vendor/skeditor plugins/youtube/youtube/",
                            "plugin.js",
                            )],
                           )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "Privacy Policy Policy Page Question & Answer"
        verbose_name_plural = "Privacy Policy Policy Page Question & Answer"

class aboustuspage(models.Model):
    aboutus = RichTextField(null=True,
                            external_plugin_resources=[(
                            "youtube",
                            "/static/base/vendor/skeditor plugins/youtube/youtube/",
                            "plugin.js",
                            )],
                           )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        verbose_name = "About Us Page"
        verbose_name_plural = "About Us Page"









class Home_Catagorys(models.Model):
    catagory = models.CharField(max_length=120, null=True)
    name = models.CharField(max_length=120, null=True,blank = True)
    home_page = models.BooleanField(blank=True,null=True)
    class Meta:
        verbose_name = "Home Page Category"
        verbose_name_plural = "Home Page Category"

    def save(self, *args, **kwargs):
        if self.name is None:
            self.name = self.catagory
            super().save(*args, **kwargs)
            
        else:
            super().save(*args, **kwargs)

