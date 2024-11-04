from django import forms
from .models import *
from order.models import *


class user_proForm(forms.ModelForm):
    class Meta:
        model = user_pro
        fields = ('full_name','phone','address')

class reqForm(forms.ModelForm):
    class Meta:
        model = req
        fields = ('link','title','quantity','message','p_image')

class sticketForm(forms.ModelForm):
    class Meta:
        model = sticket
        fields = '__all__'

class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ('country', 'product', 'quantity', 'tracking', 'note', 'image')


        

class add_to_cartForm(forms.ModelForm):


    p_total = forms.CharField(
        required=True,
        widget=forms.widgets.Input(
            attrs={
                "class": "ktotal",
                "type": "number",
            }
        ),
    )
    quantity = forms.CharField(
        required=True,
        widget=forms.widgets.Input(
            attrs={
                "class": "kquantity",
            }
        ),
    )
    image = forms.CharField(
        required=True,
        widget=forms.widgets.Input(
            attrs={
                "class": "imagess",
                "type": "text",
            }
        ),
    )
    color = forms.CharField(
        required=True,
        widget=forms.widgets.Input(
            attrs={
                "class": "extra",
            }
        ),
    )
    class Meta:
        model = add_to_carts
        fields = ('image','product','p_total','quantity','color',)
       



class payformeForm(forms.ModelForm):
    class Meta:
        model = payforme
        fields = ('product_link','product_name','quantity','color','note','product_image',)

      
class ordernumform(forms.Form):
    q = forms.IntegerField()