import decimal
from django.shortcuts import get_object_or_404
from django.contrib import messages
import os
import re
import time
from cmath import exp
from decimal import *
from http.client import EXPECTATION_FAILED
# from importlib.resources import path
from multiprocessing import context
from urllib import request
# from attrs import attr
import requests
import datetime
from django.conf import settings

from accounts.views import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.db.models import Avg, Count, Max, Min
from django.db.models.functions import ExtractMonth
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
# paypal
from django.urls import URLPattern, reverse
from django.views.decorators.csrf import csrf_exempt
# required imports
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework.settings import api_settings
from rest_framework.test import APIClient
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from selenium.common.exceptions import NoSuchElementException
from store.models import *
from order.models import *
from accounts.models import *
from snipet.models import *
import uuid
from store.forms import *
from order.forms import *
import json
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import generics
from store.serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.core.serializers import serialize
from urllib.parse import urlparse
from .alibaba_api import *
from .amazon_api import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, permissions, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .validations import custom_validation, validate_username, validate_password
from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from decimal import Decimal, ROUND_HALF_UP

dolarrate = D_Rate.objects.first()
dtk = dolarrate.usdTotk

class TotalOrderProductView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            total_orders = OrerPrduct.objects.filter(user=request.user).count()
            return Response({'total_orders': total_orders}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TotalShipingCountView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            total_orders = Shipping.objects.filter(user=request.user).count()
            return Response({'total_orders': total_orders}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AllOrderProductView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            order_products = OrerPrduct.objects.filter(user=request.user)[:10]
            serializer = OrerPrductSerializer(order_products, many=True)  # Serialize a queryset

            return Response({'total_orders': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class payformeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            order_products = payforme.objects.filter(user=request.user)[:10]
            serializer = payformeSerializer(order_products, many=True)  # Serialize a queryset

            return Response({'total_orders': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)

            # Create a custom user instance
            custom_user = CustomUser(user=user, username=user.username, phone=user.username)
            custom_user.save()

            # Generate a random OTP
            # otp = str(randint(1000, 9999))
            otp = str('1234')

            # Create a Profile instance
            profile = Profile(user=user, mobile=user.username, otp=otp)
            profile.save()

            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)



# class UserLogin(APIView):
# 	permission_classes = (permissions.AllowAny,)
# 	authentication_classes = (SessionAuthentication,)
# 	##
# 	def post(self, request):
# 		data = request.data
# 		assert validate_username(data)
# 		assert validate_password(data)
# 		serializer = UserLoginSerializer(data=data)
# 		if serializer.is_valid(raise_exception=True):
# 			user = serializer.check_user(data)
# 			login(request, user)
# 			return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        serializer = UserLoginSerializer(data=data)
        if not username or not password:
            return Response({'error': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.check_user(data)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            error_message = 'User not found'
            return JsonResponse({'error': error_message}, status=404)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class SiteIdentityListView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = Site_Identity.objects.first()
        serializer = SiteIdentitySerializer(queryset)
        return Response({'site_identity': serializer.data}, status=status.HTTP_200_OK)


class FaqpageListView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = Faq_page.objects.all()
        serializer = FaqpageSerializer(queryset, many=True)
        return Response({'site_identity': serializer.data}, status=status.HTTP_200_OK)


class Home_BanneerListView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = Home_Banneer.objects.all()
        print(queryset)
        serializer = HomeBanneerSerializer(queryset, many=True)
        return Response({'Home_banner': serializer.data}, status=status.HTTP_200_OK)

class forbidenitempagen_pageListView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = forbidenitempagen_page.objects.all()
        print(queryset)
        serializer = forbidenitempagenpageSerializer(queryset, many=True)
        return Response({'Forbidden_tems': serializer.data}, status=status.HTTP_200_OK)

class terms_condition_pageListView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = terms_condition_page.objects.all()
        print(queryset)
        serializer = termsconditionpageSerializer(queryset, many=True)
        return Response({'Terms_condition': serializer.data}, status=status.HTTP_200_OK)

class Home_top600px_BanneerListView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = Home_top600px_Banneer.objects.all()[:2]
        serializer = Hometop600pxBanneerSerializer(queryset, many=True)
        return Response({'Home_banner': serializer.data}, status=status.HTTP_200_OK)

class Home_middel502x202px_BanneerListView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = Home_middel502x202px_Banneer.objects.all()[:3]
        serializer = Homemiddel502x202pxBanneerSerializer(queryset, many=True)
        return Response({'Home_banner': serializer.data}, status=status.HTTP_200_OK)

class FooterLinkView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = FooterLinks.objects.all()
        serializer = FooterLinksializer(queryset, many=True)
        return Response({'Footer_links': serializer.data}, status=status.HTTP_200_OK)

class FooterPaymentSuportImageView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = FooterPaymentSuportImage.objects.first()
        serializer = FooterPaymentSuportImageSerializer(queryset)
        return Response({'Home_banner': serializer.data}, status=status.HTTP_200_OK)

class CatagorysListView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = CatagorysList.objects.all()
        serializer = CatagorysListSerializer(queryset, many=True)
        return Response({'Catagory_list': serializer.data}, status=status.HTTP_200_OK)

class Home_4data_breadcumView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = Home_4data_breadcum.objects.all()[:4]
        serializer = Hom4databreadcumSerializer(queryset, many=True)
        return Response({'Catagory_list': serializer.data}, status=status.HTTP_200_OK)

class FooterWidgetsView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = FooterWidget.objects.first()
        serializer = FooterWidgetSerializer(queryset)
        return Response({'Footer_weidgt': serializer.data}, status=status.HTTP_200_OK)



def single_product(product_id):

    product = Product.objects.get(product_no=product_id)
    images = ProductImage.objects.filter(product=product.product_no)
    image = None  # Initialize image variable outside the loop

    for i in images:
        if i.image.startswith('https://video01'):
            pass
        else:
            image = i.image
            break

    # Now 'image' contains the first image that doesn't start with 'https://video01'

    product_data = {
        'id': product.id,
        'product_no': product.product_no,
        'name': product.name,
        'link': product.link,
        'image': image,
    }
    
    product_price = ProductPrice.objects.filter(product=product)
    skusizes = skusize.objects.filter(product=product)
    dolarrate = D_Rate.objects.first()
    dtk = dolarrate.usdTotk
    if product_price:
        price_list = [{'price': i.price, 'saleprice': i.saleprice, 'proprice': i.proprice, 'm1': i.m1, 'm2': i.m2} for i in product_price]
        product_data['prices'] = Decimal(price_list[0]['price'])*Decimal(dtk)
    elif skusizes:
        price_list = [sku.price for sku in skusizes]
        product_data['price'] = Decimal(price_list[0])*Decimal(dtk)

    return product_data

    
def CatagorysListWithSubcategories(request):
    ctname = CatagorysList.objects.filter(is_homepage_active=True)
    kl=[]
    pl = []
    pd= []
    for i in ctname:
        cname = SubCatagorysList.objects.filter(catagory=i)
        for a in cname:
            pl.append(a.name)
        catag = Catagorys.objects.filter(catagory=i)
        for k in catag:
            produ = k.product.product_no
            ls = single_product(produ)
            
            pd.append(ls)
        
        kl.append({i.CategorName:pl,'product':pd})
        pl=[]
        pd=[]
    print(kl)
    return JsonResponse(kl, safe=False)
    # serializer_class = CatagorysListsSerializer
    # queryset = CatagorysList.objects.prefetch_related('CategorName').all()

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    
    
    
class Home_middel680x180px_BanneerListView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = Home_middel680x180px_Banneer.objects.all()[:2]
        serializer = Homemiddel680x180pxBanneerSerializer(queryset, many=True)
        return Response({'Home_banner': serializer.data}, status=status.HTTP_200_OK)

class Home_bottom_sites_BanneerListView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = Home_bottom_sites_Banneer.objects.all()
        serializer = HomebottomsitesBanneerSerializer(queryset, many=True)
        return Response({'Home_banner': serializer.data}, status=status.HTTP_200_OK)

class Home_sliding_selling_text_BanneerListView(APIView):
    permission_classes = []  # Allow both authenticated and unauthenticated access

    def get(self, request):
        queryset = Home_sliding_selling_text_Banneer.objects.first()
        serializer = HomeslidingsellingtextBanneerSerializer(queryset)
        return Response({'Home_banner': serializer.data}, status=status.HTTP_200_OK)

class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    

class UserProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user_profile, created = user_pro.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user_profile, created = user_pro.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Save the User model
            user = serializer.save()

            # Create a CustomUser instance
            custom_user = CustomUser()
            custom_user.user = user
            custom_user.username = user.username  # Assuming you want to set username from the User model
            custom_user.phone = user.username # Assuming 'phone' is a field in your request data
            custom_user.save()

            # Generate a random OTP
            # otp = str(randint(1000, 9999))
            otp = str('1234')

            # Create a Profile instance
            profile = Profile(user=user, mobile=user.username, otp=otp)
            profile.save()
            phn = request.data.get('phone')
            # Send the OTP
            # send_otp(phn, otp)
            
            # Create or retrieve the token for the user
            token, created = Token.objects.get_or_create(user=user)

            # Include the token in the response data
            response_data = {
                "user_data": serializer.data,
                "token": token.key  # Include the token key
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CheckAuthenticationView(APIView):
    def get(self, request, format=None):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            return Response({'authenticated': True}, status=status.HTTP_200_OK)
        else:
            return Response({'authenticated': False}, status=status.HTTP_401_UNAUTHORIZED)

class AddressUpdateOrCreateView(APIView):

    def post(self, request, format=None):
        # Check if the user is logged in and authorized to access this API.
        user = request.user

        # Check if the user is authenticated (logged in).
        if user.is_authenticated:
            # User is logged in, update their address.
            address_data = request.data
            serializer = UserProSerializer(instance=user, data=address_data, partial=True)
        else:
            # User is not logged in, create a new user.
            phone_number = request.data.get('phone')
            user = User.objects.create_user(username=phone_number, password=None)
            address_data = request.data
            serializer = UserProSerializer(data=address_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WalletBalanceView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = walleatSerializer

    def get(self, request):
        user_id = request.user.id

        wall = wallet.objects.filter(user_id=user_id)
        approved_amount = wallet.objects.filter(user_id=user_id, status='Approved').aggregate(approved_total=models.Sum('amount'))['approved_total'] or 0
        cancel_amount = wallet.objects.filter(user_id=user_id, status='Cancel').aggregate(cancel_total=models.Sum('amount'))['cancel_total'] or 0
        sselier = walleatSerializer(wall, many=True)
        wallet_balance = approved_amount - cancel_amount
        return Response({'wallet_balance': wallet_balance, 'History': sselier.data})
 
    def post(self, request):
        user_id = request.user.id
        sk = request.data
        sk['user']=user_id
        serializer = walleatSerializer(data=sk)

        if serializer.is_valid():
            # Call is_valid() before accessing validated_data
            serializer.save(user_id=user_id)
            return Response({'message': 'Wallet entry created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      


class UserProfileViews(APIView):
    def get(self, request):
        # Check if the user is logged in
        if request.user.is_authenticated:
            try:
                # Retrieve the user_pro instance for the logged-in user
                user_profile = user_pro.objects.get(user=request.user)

                # Serialize the data
                serializer = UserProSerializers(user_profile)

                return Response(serializer.data, status=status.HTTP_200_OK)
            except user_pro.DoesNotExist:
                return Response("User profile not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("User not logged in", status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsAuthenticated])
class CompleteOrderView(APIView):
    def post(self, request):
        kalk = request.user
        print(request.data)
        aamount = wallet.objects.filter(user_id=kalk.id, status='Approved')
        camount = wallet.objects.filter(user_id=kalk.id, status='Cancel')
        l = 0
        j = 0
        ska = 0
        for rk in camount:
            t = Decimal(rk.amount)
            j += t
        for rs in aamount:
            total = Decimal(rs.amount)
            l += total
        ska = l - j
        k = 0
        for rs in request.data['products']:
            p_total = Decimal(rs['price'])
            k += p_total

        form = orderssForm(request.data, request.FILES)
        orders = 10000001 if orderss.objects.count() == 0 else orderss.objects.aggregate(max=Max('order_id'))["max"] + 1
        if form.is_valid():
            statusp = request.data.get('t_m')
            paid = request.data.get('paid')
            due = request.data.get('due')
            thought = form.save(commit=False)
            thought.order_id = orders
            thought.user_id = kalk.id
            thought.t_m = statusp
            thought.price = k
            thought.paid = request.data.paid
            thought.due = request.data.due
            if statusp == "Wallet":
                kak = wallet()
                kak.user_id = kalk.id
                kak.status = "Cancel"
                kak.amount = request.data.paid
                kak.note = "order payment"
                kak.t_id = "order payment"
                kak.t_m = "Order Payment"
                thought.p_status = "Paid"
                kak.save()
            thought.save()
            
            for rs in request.data['products']:
                orders_product = 100001 if OrerPrduct.objects.count() == 0 else OrerPrduct.objects.aggregate(
                    max=Max('OrderP_id'))["max"] + 1
                p = Product.objects.get(product_no = rs['product_no'])
                dat = OrerPrduct()
                dat.orderi_id = thought.order_id
                dat.OrderP_id = orders_product
                dat.product_id = p.id
                dat.image = rs['image']
                dat.note = form.validated_data.get('note')
                dat.user_id = kalk.id
                dat.color = rs['size']
                dat.quantity = rs['quantity']
                dat.price = rs['price']
                dat.paid = request.data['paid']
                dat.due = request.data['due']
                dat.save()

            response_data = {'message': 'Product Successfully Added', 'order_id': orders}
            return JsonResponse(response_data, status=200)

        else:
            phone = request.data.get('phone')
            address = request.data.get('addess')
            statusp = request.data.get('t_m')
            tid = request.data.get('t_id')
            paid = request.data.get('paid')
            due = request.data.get('due')
            order = orderss(order_id=orders, user=kalk, phone=phone, price=k, paid=paid, due=due, t_m=statusp, t_id=tid, addess=address)
            order.save()
            for rs in request.data['products']:
                orders_product = 100001 if OrerPrduct.objects.count() == 0 else OrerPrduct.objects.aggregate(
                    max=Max('OrderP_id'))["max"] + 1
                p = Product.objects.get(product_no = rs['product_no'])
                dat = OrerPrduct()
                dat.orderi_id = order.order_id
                dat.OrderP_id = orders_product
                dat.product_id = p.id
                dat.image = rs['image']
                dat.note = request.data.get('note')
                dat.user_id = kalk.id
                size_list = rs['size']
                text_representation = ""

                for item in size_list:
                    text_representation += f"Size: {item['size']}, Price: {item['price']}, Quantity: {item['quantity']}, Color: {item['color']}\n"

                dat.color = text_representation
                dat.quantity = rs['quantity']
                dat.price = rs['price']
                dat.paid = request.data['paid']
                dat.due = request.data['due']
                dat.save()
                print(type(rs['size']))

            response_data = {'message': 'Product Successfully Added', 'order_id': orders}
            return JsonResponse(response_data, status=200)

    def get(self, request):
        return JsonResponse({'message': 'GET request not allowed'}, status=405)

    def put(self, request):
        return JsonResponse({'message': 'PUT request not allowed'}, status=405)

    def delete(self, request):
        return JsonResponse({'message': 'DELETE request not allowed'}, status=405)



@api_view(['GET'])
def productViewSet(request,product_no, id):
    prox = serialize("jsonl", Product.objects.filter(id=id))
    data = serialize("jsonl", skucolor.objects.filter(product_id=product_no))
    size = serialize("jsonl", skusize.objects.filter(product_id=product_no))
    output = json.dumps(json.loads(prox), indent=4) + "\n" + data + "\n" + size
    return HttpResponse(output, content_type="application/json")




from django.core import serializers
def get_single_product(request, product_id):
    try:
        product = Product.objects.get(product_no=product_id)
        images = ProductImage.objects.filter(product=product.product_no)
        image = None  # Initialize image variable outside the loop

        for i in images:
            if i.image.startswith('https://video01'):
                pass
            else:
                image = i.image
                break

        # Now 'image' contains the first image that doesn't start with 'https://video01'

        product_data = {
            'id': product.id,
            'product_no': product.product_no,
            'name': product.name,
            'link': product.link,
            'image': image,
        }
        
        product_price = ProductPrice.objects.filter(product=product)
        skusizes = skusize.objects.filter(product=product)
        
        if product_price:
            price_list = [{'price': Decimal(i.price) * Decimal(dtk), 'saleprice': i.saleprice, 'proprice': i.proprice, 'm1': i.m1, 'm2': i.m2} for i in product_price]
            product_data['prices'] = price_list
        elif skusizes:
            price_list = [sku.price for sku in skusizes]
            product_data['price'] = Decimal(price_list[0])*Decimal(dtk)
        else:
            return JsonResponse({'error': 'Product prices not found'}, status=404)

        return JsonResponse(product_data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


def get_single_product_images(request, id):
    try:
        product = Product.objects.get(product_no=id)

        # Create a list to store image URLs
        image_urls = []

        images = ProductImage.objects.filter(product=product.product_no)
        for image in images:
            image_urls.append({'img':image.image, 'cover':image.image_cover})  # Assuming 'image' is a FileField or ImageField

        return JsonResponse({'images': image_urls})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

def get_all_products(request):
    num_products = request.GET.get('num', 10)  # Default to 10 if 'num' parameter is not provided
    num_products = int(num_products)  # Convert to an integer

    products = Product.objects.all()[:num_products]
    product_list = []
    dollar_ratses = D_Rate.objects.first() 
    dollar_rate = Decimal(dollar_ratses.usdTotk)

    for product in products:
        product_data = {
            'id': product.id,
            'product_no': product.product_no,
            'name': product.name,
            'link': product.link,
        }

        product_price = ProductPrice.objects.filter(product=product).first()

        if product_price:
            product_data['saleprice'] = product_price.saleprice
            product_data['proprice'] = product_price.proprice
            product_data['m1'] = product_price.m1
            product_data['m2'] = product_price.m2
            result = Decimal( product_price.price) * dollar_rate

            # Round the result to two decimal places using quantize
            rounded_result = result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            product_data['price'] = rounded_result
        else:
            skusizes = skusize.objects.filter(product=product)
            if skusizes:
                # Assuming 'price' is an attribute of the 'skusize' model
                # Iterate through all related skusizes and append their prices to a list
                price_list = [sku.price for sku in skusizes]
                
                # Define a regular expression pattern to match decimal numbers
                pattern = r'\d+\.\d+'

                # Find all matches of the pattern in the data
                decimal_numbers = []

                # Iterate through the price_list and extract decimal numbers
                for item in price_list:
                    matches = re.findall(pattern, item)
                    decimal_numbers.extend(matches)

                # Convert the matches to float and store them in a list
                decimal_numbers = [float(match) for match in decimal_numbers]

                # Check if there are valid decimal numbers
                if decimal_numbers:
                    # Find the minimum value
                    minimum_value = min(decimal_numbers)
                    print("Extracted decimal numbers:", decimal_numbers)
                    print("Minimum value:", minimum_value)
                else:
                    print("No valid decimal numbers found in the price list.")

                result = Decimal(minimum_value) * dollar_rate

                # Round the result to two decimal places using quantize
                rounded_result = result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                # You may choose to use the first price or some other logic
                # Here, we're using the first price in the list
                product_data['price'] = rounded_result
        products_ctn = Product.objects.all().count()
        first_image = ProductImage.objects.filter(product=product).first()
        if first_image:
            if 'https://video01' in first_image.image:
                product_data['image'] = first_image.image_cover
            else:
                product_data['image'] = first_image.image
        else:
            product_data['image'] = ''

        product_list.append(product_data)
  

    return JsonResponse({'products': product_list, 'total_count':products_ctn})


class ReqAPIView(APIView):
    def post(self, request):
        kalk = request.user
        note = reqsnote.objects.all()
        ph = Profile.objects.get(user=kalk.id)

        form = reqForm(request.data)  # Use request.data to get POST data

        if form.is_valid():
            orders = 90000001 if req.objects.count() == 0 else req.objects.aggregate(max=Max('order_id'))["max"] + 1
            thought = form.save(commit=False)
            thought.user = request.user
            thought.customer = ph
            thought.order_id = orders
            thought.save()
            messages.success(request, 'Request Order Successfully Added')
            phone = ph.mobile
            name = request.user.first_name
            ordernumber = str(orders)
            message = "Hi " + name + "," + "\n" + "Your Shopping Request Submited Successfully.\n Thank You for Staying With Us.." + "\n Your Shopping Request ID: " + ordernumber + "\n Visit Us: https://ecargo.com.bd/order/"

            url = "http://apismpp.ajuratech.com/sendtext"

            querystring = {"apikey": "a6584c5c4908024d", "secretkey": "80b5d891", "callerID": "quickcartbd",
                           "toUser": phone, "messageContent": message}
            headers = {
                'cache-control': "no-cache",
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            return Response({'message': 'Request Order Successfully Added'}, status=status.HTTP_201_CREATED)

        else:
            return Response({'message': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)

class ShippingPostAPIView(APIView):
    def post(self, request):
        kalk = request.user
        ph = Profile.objects.get(user=kalk.id)

        form = ShippingForm(request.data)  # Use request.data to get POST data

        if form.is_valid():
            orders = 60000001 if Shipping.objects.count() == 0 else Shipping.objects.aggregate(max=Max('shipping_id'))["max"] + 1
            thought = form.save(commit=False)
            thought.shipping_id = orders
            thought.user = request.user
            thought.save()
            messages.success(request, 'Request Order Successfully Added')
            phone = ph.mobile
            name = request.user.first_name
            ordernumber = str(orders)
            message = "Hi " + name + "," + "\n" + "Your Shopping Request Submited Successfully.\n Thank You for Staying With Us.." + "\n Your Shopping Request ID: " + ordernumber + "\n Visit Us: https://ecargo.com.bd/order/"

            url = "http://apismpp.ajuratech.com/sendtext"

            querystring = {"apikey": "a6584c5c4908024d", "secretkey": "80b5d891", "callerID": "quickcartbd",
                           "toUser": phone, "messageContent": message}
            headers = {
                'cache-control': "no-cache",
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            return Response({'message': 'Request Order Successfully Added'}, status=status.HTTP_201_CREATED)

        else:
            return Response({'message': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)


@login_required
def render_ticket(request, template_name, context):
    # This function won't be used, as it renders HTML
    pass

@staff_member_required
def render_ticket_admin(request, template_name, context):
    # This function won't be used, as it renders HTML
    pass



class TicketAPIView(APIView):
    def get(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is an admin
            if request.user.is_staff:
                # User is an admin
                tickets = sticket.objects.all()
                ticket_dict = {}

                for ticket in tickets:
                    sms = smst.objects.filter(ticketi=ticket)
                    sms_serializer = SmstSerializer(sms, many=True)
                    ticket_serializer = SticketSerializer(ticket)

                    ticket_dict[ticket_serializer.data['ticket_no']] = {
                        'ticket': ticket_serializer.data,
                        'sms': sms_serializer.data
                    }

                return Response({'user': request.user.id,'status':'admin','Total':tickets.count(), 'tickets': ticket_dict}, status=status.HTTP_200_OK)
            else:
                tickets = sticket.objects.filter(user=request.user)
                ticket_dict = {}

                for ticket in tickets:
                    sms = smst.objects.filter(ticketi=ticket)
                    sms_serializer = SmstSerializer(sms, many=True)
                    ticket_serializer = SticketSerializer(ticket)

                    ticket_dict[ticket_serializer.data['ticket_no']] = {
                        'ticket': ticket_serializer.data,
                        'sms': sms_serializer.data
                    }
                # User is a normal login user
                return Response({'user': request.user.id,'status':'admin','Total':tickets.count(), 'tickets': ticket_dict}, status=status.HTTP_200_OK)
        else:
            # User is not authenticated
            return Response({'message': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)             

    
    def post(self, request):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({'message': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        orders_product = 100001 if sticket.objects.count() == 0 else sticket.objects.aggregate(max=Max('ticket_no')) ["max"]+1
        sms = request.data
        sms['ticket_no'] = orders_product
        # Deserialize the incoming data
        serializer = SticketSerializer(data=sms)

        if serializer.is_valid():
            # Save the new ticket
            serializer.save(user=request.user)

            return Response({'message': 'Ticket created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class TicketSmsAPIView(APIView):
    def get(self, request, ticket_id):
        ticket = ticket_id
        user_profile = user_pro.objects.get(user=request.user)

        # Serialize the data
        serializers = UserProSerializers(user_profile)
        user_data = serializers.data
        sms = smst.objects.filter(ticketi=ticket)
        sms_serializer = SmstSerializer(sms, many=True)
        # User is a normal login user
        return Response({'user': request.user.id,'sms': sms_serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, ticket_id):
        # Assuming you have the necessary data in the request.data to create a new SMS instance
        request_data = request.data.copy()
        request_data['ticketi'] = ticket_id  # Assuming you have the 'ticketi' field in request.data
        request_data['user'] = request.user.id  # Assuming you have the 'ticketi' field in request.data

        # You may need to adjust the serializer based on your specific requirements
        sms_serializer = SmstSerializer(data=request_data)

        if sms_serializer.is_valid():
            sms_serializer.save()
            return Response(sms_serializer.data, status=status.HTTP_201_CREATED)
        return Response(sms_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
                        
class PaysformePostAPIView(APIView):
    def post(self, request):
        kalk = request.user
        ph = Profile.objects.get(user=kalk.id)

        form = payformeForm(request.data)  # Use request.data to get POST data

        if form.is_valid():
            orders = 90000001 if payforme.objects.count() == 0 else payforme.objects.aggregate(max=Max('payment_id'))["max"] + 1
            thought = form.save(commit=False)
            thought.payment_id = orders
            thought.user = request.user
            thought.phone = ph.mobile
            thought.save()
            messages.success(request, 'Request Order Successfully Added')
            phone = ph.mobile
            name = request.user.first_name
            ordernumber = str(orders)
            message = "Hi " + name + "," + "\n" + "Your Shopping Request Submited Successfully.\n Thank You for Staying With Us.." + "\n Your Shopping Request ID: " + ordernumber + "\n Visit Us: https://ecargo.com.bd/order/"

            url = "http://apismpp.ajuratech.com/sendtext"

            querystring = {"apikey": "a6584c5c4908024d", "secretkey": "80b5d891", "callerID": "quickcartbd",
                           "toUser": phone, "messageContent": message}
            headers = {
                'cache-control': "no-cache",
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            return Response({'message': 'Request Order Successfully Added'}, status=status.HTTP_201_CREATED)

        else:
            return Response({'message': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)



from django.views.generic import TemplateView
from react.mixins import ReactMixin


class IndexView(ReactMixin, TemplateView):
    template_name = 'react/react.html'
    app_root = 'components/app.jsx'

def shop(request):

    
    b = Product.objects.child_of(self).live()
    context = {
        'Product':b,
        }
    

    return render(request, 'shop/shop.html',context)



def Search(query):

    html_contect = requests.get(f'{query}').text
    return html_contect
import threading



def producta_list(products):
    product_list = []
    for product in products:
        product_data = {
            'id': product.id,
            'product_no': product.product_no,
            'name': product.name,
            'link': product.link,
        }

        product_price = ProductPrice.objects.filter(product=product).first()

        if product_price:
            product_data['price'] = Decimal(product_price.price)*Decimal(dtk)
            product_data['saleprice'] = product_price.saleprice
            product_data['proprice'] = product_price.proprice
            product_data['m1'] = product_price.m1
            product_data['m2'] = product_price.m2
        else:
            skusizes = skusize.objects.filter(product=product)
            if skusizes:
                # Assuming 'price' is an attribute of the 'skusize' model
                # Iterate through all related skusizes and append their prices to a list
                price_list = [sku.price for sku in skusizes]
                # You may choose to use the first price or some other logic
                # Here, we're using the first price in the list
                product_data['price'] = Decimal(price_list[0])*Decimal(dtk)

        first_image = ProductImage.objects.filter(product=product).first()
        if first_image:
            if 'https://video01' in first_image.image:
                product_data['image'] = first_image.image_cover
            else:
                product_data['image'] = first_image.image
        else:
            product_data['image'] = ''

        product_list.append(product_data)

    return product_list
    
def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')


        import re

        product_list = []
        validate = URLValidator()


        try:

            x = query
            # Define a regular expression pattern to match URLs
            url_pattern = r'https?://\S+'

            # Find all matches in the string
            matches = re.findall(url_pattern, x)

            # Check if any URLs were found and take the first one
            if matches:
                link = matches[0]
            else:
                link = None

            print(link)
            validate(link)

            try:
                if "alibaba.com" in link:
                    products = Product.objects.filter(link__icontains = link)
                    if products:
                        for product in products:
                            product_data = {
                                'id': product.id,
                                'product_no': product.product_no,
                                'name': product.name,
                                'link': product.link,
                            }

                            product_price = ProductPrice.objects.filter(product=product).first()

                            if product_price:
                                product_data['price'] = Decimal(product_price.price)*Decimal(dtk)
                                product_data['saleprice'] = product_price.saleprice
                                product_data['proprice'] = product_price.proprice
                                product_data['m1'] = product_price.m1
                                product_data['m2'] = product_price.m2
                            else:
                                skusizes = skusize.objects.filter(product=product)
                                if skusizes:
                                    # Assuming 'price' is an attribute of the 'skusize' model
                                    # Iterate through all related skusizes and append their prices to a list
                                    price_list = [sku.price for sku in skusizes]
                                    # You may choose to use the first price or some other logic
                                    # Here, we're using the first price in the list
                                    product_data['price'] = Decimal(price_list[0])*Decimal(dtk)

                            first_image = ProductImage.objects.filter(product=product).first()
                            if first_image:
                                if 'https://video01' in first_image.image:
                                    product_data['image'] = first_image.image_cover
                                else:
                                    product_data['image'] = first_image.image
                            else:
                                product_data['image'] = ''

                            product_list.append(product_data)

                        return JsonResponse({'products': product_list})
                    else:
                        webPage = requests.get(x)
                        l = webPage.text
                        soup = BeautifulSoup(l, "html.parser")
                        try:
                            s = soup.find("script", {"data-from": "server"}).string
                            l = s.replace('window.__INITIAL_DATA__=','')
                            c = json.loads(l)
                            i = c["pageInitialProps"]
                            j = i["data"]
                            k = j["globalData"]
                            l = k["extend"]
                            m = l["seoData"]
                            n = m["canonical"]

                            newurl =  n
                        except:
                            seperator = '?'
                            q = x
                            l = q.split(seperator)[0]
                            newurl = l
                        products = Product.objects.filter(link__icontains=newurl)
                        if not products:
                            thread1 = threading.Thread(target=alibaba_api, args=(newurl,))

                            thread1.start()
                            return JsonResponse({'url': newurl, 'status': 'Searching'})

                if "amazon.com" in link or "a.co" in link:
                    products = Product.objects.filter(link__icontains = link)
                    if products:
                        for product in products:
                            product_data = {
                                'id': product.id,
                                'product_no': product.product_no,
                                'name': product.name,
                                'link': product.link,
                            }

                            product_price = ProductPrice.objects.filter(product=product).first()

                            if product_price:
                                product_data['price'] = Decimal(product_price.price)*Decimal(dtk)
                                product_data['saleprice'] = product_price.saleprice
                                product_data['proprice'] = product_price.proprice
                                product_data['m1'] = product_price.m1
                                product_data['m2'] = product_price.m2
                            else:
                                skusizes = skusize.objects.filter(product=product)
                                if skusizes:
                                    # Assuming 'price' is an attribute of the 'skusize' model
                                    # Iterate through all related skusizes and append their prices to a list
                                    price_list = [sku.price for sku in skusizes]
                                    # You may choose to use the first price or some other logic
                                    # Here, we're using the first price in the list
                                    product_data['price'] = Decimal(price_list[0])*Decimal(dtk)

                            first_image = ProductImage.objects.filter(product=product).first()
                            if first_image:
                                if 'https://video01' in first_image.image:
                                    product_data['image'] = first_image.image_cover
                                else:
                                    product_data['image'] = first_image.image
                            else:
                                product_data['image'] = ''

                            product_list.append(product_data)

                        return JsonResponse({'products': product_list})
                    else:
                        seperator = '?'
                        q = link
                        l = q.split(seperator)[0]
                        newurl = l
                        products = Product.objects.filter(link__icontains=newurl)
                        if not products:
                            thread1 = threading.Thread(target=amazon_api, args=(newurl,request))

                            thread1.start()
                            return JsonResponse({'url': x, 'status': 'Searching'})
                        else:
                            for product in products:
                                product_data = {
                                    'id': product.id,
                                    'product_no': product.product_no,
                                    'name': product.name,
                                    'link': product.link,
                                }

                                product_price = ProductPrice.objects.filter(product=product).first()

                                if product_price:
                                    product_data['price'] = Deciaml(product_price.price)*Decimal(dtk)
                                    product_data['saleprice'] = product_price.saleprice
                                    product_data['proprice'] = product_price.proprice
                                    product_data['m1'] = product_price.m1
                                    product_data['m2'] = product_price.m2
                                else:
                                    skusizes = skusize.objects.filter(product=product)
                                    if skusizes:
                                        # Assuming 'price' is an attribute of the 'skusize' model
                                        # Iterate through all related skusizes and append their prices to a list
                                        price_list = [sku.price for sku in skusizes]
                                        # You may choose to use the first price or some other logic
                                        # Here, we're using the first price in the list
                                        product_data['price'] = Decimal(price_list[0])*Decimal(dtk)

                                first_image = ProductImage.objects.filter(product=product).first()
                                if first_image:
                                    if 'https://video01' in first_image.image:
                                        product_data['image'] = first_image.image_cover
                                    else:
                                        product_data['image'] = first_image.image
                                else:
                                    product_data['image'] = ''

                                product_list.append(product_data)

                            return JsonResponse({'products': product_list})
                        
                products = Product.objects.filter(link__icontains = link)
                product_list = []
                for product in products:
                    product_data = {
                        'id': product.id,
                        'product_no': product.product_no,
                        'name': product.name,
                        'link': product.link,
                    }

                    product_price = ProductPrice.objects.filter(product=product).first()

                    if product_price:
                        product_data['price'] = Decimal(product_price.price)*Decimal(dtk)
                        product_data['saleprice'] = product_price.saleprice
                        product_data['proprice'] = product_price.proprice
                        product_data['m1'] = product_price.m1
                        product_data['m2'] = product_price.m2
                    else:
                        skusizes = skusize.objects.filter(product=product)
                        if skusizes:
                            # Assuming 'price' is an attribute of the 'skusize' model
                            # Iterate through all related skusizes and append their prices to a list
                            price_list = [sku.price for sku in skusizes]
                            # You may choose to use the first price or some other logic
                            # Here, we're using the first price in the list
                            product_data['price'] = Decimal(price_list[0])*Decimal(dtk)

                    first_image = ProductImage.objects.filter(product=product).first()
                    if first_image:
                        if 'https://video01' in first_image.image:
                            product_data['image'] = first_image.image_cover
                        else:
                            product_data['image'] = first_image.image
                    else:
                        product_data['image'] = ''

                    product_list.append(product_data)

                return JsonResponse({'products': product_list})
                
                
                
            # except TimeoutException:
            #     Product.objects.filter(link__icontains = x).delete()
            #     return redirect('rqo')
            # except NoSuchElementException:
            #     Product.objects.filter(link__icontains = x).delete()
            #     return redirect('rqo')
            # except AttributeError:
            #     Product.objects.filter(link__icontains = x).delete()
            #     return redirect('rqo')
            # except ValueError:
            #     Product.objects.filter(link__icontains = x).delete()
              
            #     return redirect('rqo')
                 
            except IntegrityError:

                if query:
                    products = Product.objects.filter(link__icontains=x)
                    product_list = []
                    for product in products:
                        product_data = {
                            'id': product.id,
                            'product_no': product.product_no,
                            'name': product.name,
                            'link': product.link,
                        }

                        product_price = ProductPrice.objects.filter(product=product).first()

                        if product_price:
                            product_data['price'] = Decimal(product_price.price)*Decimal(dtk)
                            product_data['saleprice'] = product_price.saleprice
                            product_data['proprice'] = product_price.proprice
                            product_data['m1'] = product_price.m1
                            product_data['m2'] = product_price.m2
                        else:
                            skusizes = skusize.objects.filter(product=product)
                            if skusizes:
                                # Assuming 'price' is an attribute of the 'skusize' model
                                # Iterate through all related skusizes and append their prices to a list
                                price_list = [sku.price for sku in skusizes]
                                # You may choose to use the first price or some other logic
                                # Here, we're using the first price in the list
                                product_data['price'] = Decimal(price_list[0])*Decimal(dtk)

                        first_image = ProductImage.objects.filter(product=product).first()
                        if first_image:
                            if 'https://video01' in first_image.image:
                                product_data['image'] = first_image.image_cover
                            else:
                                product_data['image'] = first_image.image
                        else:
                            product_data['image'] = ''

                        product_list.append(product_data)

                    return JsonResponse({'products': product_list})

                else:

                    products = Product.objects.filter(name__icontains=query)
                    for product in products:
                        product_data = {
                            'id': product.id,
                            'product_no': product.product_no,
                            'name': product.name,
                            'link': product.link,
                        }

                        product_price = ProductPrice.objects.filter(product=product).first()

                        if product_price:
                            product_data['price'] = Decimal(product_price.price)*Decimal(dtk)
                            product_data['saleprice'] = product_price.saleprice
                            product_data['proprice'] = product_price.proprice
                            product_data['m1'] = product_price.m1
                            product_data['m2'] = product_price.m2
                        else:
                            skusizes = skusize.objects.filter(product=product)
                            if skusizes:
                                # Assuming 'price' is an attribute of the 'skusize' model
                                # Iterate through all related skusizes and append their prices to a list
                                price_list = [sku.price for sku in skusizes]
                                # You may choose to use the first price or some other logic
                                # Here, we're using the first price in the list
                                product_data['price'] = Decimal(price_list[0])*Decimal(dtk)

                        first_image = ProductImage.objects.filter(product=product).first()
                        if first_image:
                            if 'https://video01' in first_image.image:
                                product_data['image'] = first_image.image_cover
                            else:
                                product_data['image'] = first_image.image
                        else:
                            product_data['image'] = ''

                        product_list.append(product_data)

                    return JsonResponse({'products': product_list})



        except:
            try:
                search_query = SearchQuery.objects.get(query=query)
            except:
                search_query = SearchQuery(query=x, status='Searching')
                search_query.save()
                search_query = SearchQuery.objects.get(query=query)
            try:
                try:
                    
                    products = Product.objects.filter(name__icontains=query)
                    if not products:
                        raise ValueError
                    pb = producta_list(products)
                    search_query.status = 'Completed'
                    search_query.save()
                    return JsonResponse({'products': pb})
                except:
                    tl = Catagorys.objects.filter(catagory__icontains=query)
                    productsk=[]
                    for i in tl:
                        products = Product.objects.get(id=i.product.id)
                        productsk.append(products)
                        print(products)
                        print(products)
                        print(products)
                        print(products)
                        print(products)
                        if not products:
                            raise ValueError
                    pb = producta_list(productsk)
                    print(pb)
                    search_query.status = 'Completed'
                    search_query.save()
                    return JsonResponse({'products': pb})
                    
                

            except:
                products = Product.objects.filter(link__icontains=x)
                if not products:
                    raise ValueError
                pb = producta_list(products)
                search_query.status = 'Completed'
                search_query.save()
                return JsonResponse({'products': pb})

                


def check_search_status(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')  # Get the query parameter from the GET request
        # Perform logic to get the search status based on the query
        try:
            seperator = '?'
            q = query
            l = q.split(seperator)[0]
            newurl = l
            search_query = SearchQuery.objects.get(query=newurl)
            print(query)
            status = search_query.status
        except SearchQuery.DoesNotExist:
            status = 'Query not found'

        return JsonResponse({'status': status})


@api_view(['GET'])
def shipformedes_list(request):
    if request.method == 'GET':
        shipformedes_data = shipformedes.objects.all()
        serializer = ShipformedesSerializer(shipformedes_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def shipformecharge_list(request):
    if request.method == 'GET':
        shipformecharge_data = shipformecharge.objects.all()
        serializer = shipformechargeSerializer(shipformecharge_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def shipformemesssages_list(request):
    if request.method == 'GET':
        shipformemesssages_data = shipformemesssages.objects.all()
        serializer = shipformemesssagesSerializer(shipformemesssages_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.http import Http404
@csrf_exempt
def product_detail(request,product_no,name, id):
   

    try:
        products = Product.objects.get(id=id)
    except:
        raise Http404("Product not found")
    l = Product.objects.order_by("-created_at")[:5]
    if products.link.startswith('https://www.alibaba.com/') or products.link.startswith('https://alibaba.com/'):
        productk = l
        images = ProductImage.objects.filter(product_id=product_no)
        priceD = ProductPrice.objects.filter(product_id=product_no)
        sku_color = skucolor.objects.filter(product_id=product_no)
        sku_size = skusize.objects.filter(product_id=product_no)
        info = SellerInfo.objects.filter(product_id=product_no)
        short = ProductDes.objects.filter(product_id=product_no)
        descriptions = description.objects.filter(product_id=product_no)
        reviewsk = reviews.objects.filter(product_id=product_no)


    
        form = add_to_cartForm()

        return render(request, 'home/product.html', {'data': products, 'img': images, 'price': priceD,'reviews': reviewsk, 'colors': sku_color, 'sku_size': sku_size,'SellerInfo':info,'productk':productk,'short':short,'form':form,'descriptions':descriptions,})
    elif products.link.startswith('https://www.amazon.com/') or products.link.startswith('https://amazon.com/') or products.link.startswith('https://a.co/'):
        productk = l
        images = ProductImage.objects.filter(product_id=product_no)
        priceD = ProductPrice.objects.filter(product_id=product_no)
        sku_color = skucolor.objects.filter(product_id=product_no)
        sku_size = skusize.objects.filter(product_id=product_no)
        info = SellerInfo.objects.filter(product_id=product_no)
        short = ProductDes.objects.filter(product_id=product_no)
        descriptions = description.objects.filter(product_id=product_no)
        reviewsk = reviews.objects.filter(product_id=product_no)


    
        form = add_to_cartForm()

        return render(request, 'home/aproduct.html', {'data': products, 'img': images, 'price': priceD,'reviews': reviewsk, 'colors': sku_color, 'sku_size': sku_size,'SellerInfo':info,'productk':productk,'short':short,'form':form,'descriptions':descriptions,})




from django.core.exceptions import ObjectDoesNotExist

def get_description(request, product_no):
    try:
        # Assuming product_no is the product_id you want to filter on
        descriptions = description.objects.filter(product__product_no=product_no)
        print(descriptions)
        serializer = descriptionSerializer(descriptions, many=True)
        serialized_data = serializer.data  # Extract serialized data from serializer

        return JsonResponse({"descriptions": serialized_data}, status=status.HTTP_200_OK, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Product description not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return JsonResponse({"message": "Invalid product number"}, status=status.HTTP_400_BAD_REQUEST)

def get_Review(request, product_no):
    try:
        # Assuming product_no is the product_id you want to filter on
        descriptions = reviews.objects.filter(product__product_no=product_no)
        serializer = reviewsSerializer(descriptions, many=True)
        serialized_data = serializer.data  # Extract serialized data from serializer

        return JsonResponse({"reviews": serialized_data}, status=status.HTTP_200_OK, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Product description not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return JsonResponse({"message": "Invalid product number"}, status=status.HTTP_400_BAD_REQUEST)

def get_color(request, product_id):
    # Assuming you have a Size model with product and color fields
    sizes = skucolor.objects.filter(product=product_id)

    color_data = []
    for size in sizes:
        image_url = size.image if size.image else None  # Get the image URL as a string
        color_data.append({
            'color': size.color,
            'image': str(image_url),  # Include the image URL in the response
        })

    return JsonResponse({'sizes': color_data})

def get_Sku(request, product_id):
    # Assuming you have a Size model with product and color fields
    sizes = sku.objects.filter(product=product_id)

    color_data = []
    for size in sizes:
        color_data.append({
            'name': size.name,
            'option': size.option,  # Include the image URL in the response
        })

    return JsonResponse({'Sku': color_data})

def get_Sellerinfo(request, product_id):
    # Assuming you have a Size model with product and color fields
    info = SellerInfo.objects.filter(product_id=product_id)
    sellerinfo = []
    for i in info:
        sellerinfo.append({'seller':i.seller,'year':i.year,'country':i.country})

    return JsonResponse({'SellerInfo': sellerinfo})


@api_view(['POST'])
def paynowreq_api(request, id):
    permission_classes = [permissions.IsAuthenticated]
    try:
        orderP = req.objects.get(id=id, user=request.user.id)
    except OrerPrduct.DoesNotExist:
        return Response({'error': 'OrderProduct not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        kalk = request.user
        amount = request.data.get('amount')
        t_m = request.data.get('t_m')
        t_id = request.data.get('t_id')
        t_img = request.data.get('t_img')

        if t_m == 'Wallet':
            kak = wallet()
            kak.user_id = kalk.id
            kak.status = "Cancel"
            kak.amount = amount
            kak.note = "order partial payment"
            kak.t_id = "order partial payment"
            kak.t_m = "order partial payment"
            kak.save()

            order_data = {
                'orderi': orderP.order_id,
                'user': kalk.id,
                'p_status': 'Paid',
                'Amount': amount,
                't_m': t_m,
                't_id': t_id,
                't_img': t_img
            }
        else:
            order_data = {
                'orderi': orderP.OrderP_id,
                'user': kalk.id,
                'Amount': amount,
                't_m': t_m,
                't_id': t_id,
                't_img': t_img
            }

        serializer = Order_Partial_PaymentSerializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Payment Successfull. Wait for the confirmation. We will notify you.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def Shippingpaynowreq_api(request, id):
    permission_classes = [permissions.IsAuthenticated]
    try:
        orderP = Shipping.objects.get(shipping_id=id, user=request.user.id)
    except OrerPrduct.DoesNotExist:
        return Response({'error': 'OrderProduct not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        kalk = request.user
        amount = request.data.get('amount')
        t_m = request.data.get('t_m')
        t_id = request.data.get('t_id')
        t_img = request.data.get('t_img')

        if t_m == 'Wallet':
            kak = wallet()
            kak.user_id = kalk.id
            kak.status = "Cancel"
            kak.amount = amount
            kak.note = "order partial payment"
            kak.t_id = "order partial payment"
            kak.t_m = "order partial payment"
            kak.save()

          
            orderP.p_status='Paid'
            orderP.Amount= amount
            orderP.status= "Payment Confirm Pending"
            orderP.t_m= t_m,
            orderP.t_id= t_id,
            orderP.t_img= t_img
            orderP.save()
            
        else:
            orderP.p_status='Paid'
            orderP.Amount= amount
            orderP.status= "Payment Confirm Pending"
            orderP.t_m= t_m,
            orderP.t_id= t_id,
            orderP.t_img= t_img
            orderP.save()
           
            return Response({'message': 'Payment Successfull. Wait for the confirmation. We will notify you.'}, status=status.HTTP_201_CREATED)
        return Response( status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




class CombinedRequestListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CombinedRequestSerializer

    def get_queryset(self,request):
        user_id = request.user.id
        o_requests = ORequest_Delivery.objects.filter(user_id=user_id)
        r_requests = RRequest_Delivery.objects.filter(user_id=user_id)
        s_requests = SRequest_Delivery.objects.filter(user_id=user_id)
        total_requests = o_requests.count() + r_requests.count() + s_requests.count()
        return {
            'o_requests': o_requests,
            'r_requests': r_requests,
            's_requests': s_requests,
            'total_requests': total_requests
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


def get_sizes(request, product_id):
    # Assuming you have a Size model with product and color fields
    sizes = skusize.objects.filter(product=product_id)
    dollar_rate = 130

    size_data = []
    for size in sizes:
        p=size.price
        if p:
            # Define a regular expression pattern to match decimal numbers
            pattern = r'\d+\.\d+'

            # Find all matches of the pattern in the data
            matches = re.findall(pattern, p)

            # Convert the matches to float and store them in a list
            decimal_numbers = [float(match) for match in matches]
        minimum_value = ''
        # Check if there are valid decimal numbers
        if p:
            if decimal_numbers:
                # Find the minimum value
                result = [number * 130 for number in decimal_numbers]
                minimum_value = min(result)
                rounded_result = minimum_value
                print("Extracted decimal numbers:", decimal_numbers)
                print("Minimum value:", minimum_value)
        else:
            product = Product.objects.get(product_no=product_id)
            product_price = ProductPrice.objects.filter(product=product).first()
            
            if product_price:
                minimum_value = Decimal(product_price.price )
            else:
                skusizes = skusize.objects.filter(product=product)
                if skusizes:
                    price_list = [sku.price for sku in skusizes]
                    minimum_value = price_list[0] 
            result = minimum_value * dollar_rate

            # Round the result to two decimal places using quantize
            rounded_result = result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        size_data.append({
            'size': size.size,
            'price': rounded_result,
            'quantity': 0,
        })

    return JsonResponse({'sizes': size_data})


class PayNowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            orderP = OrerPrduct.objects.get(OrderP_id=id, user=request.user.id)
            a = Decimal(str(orderP.due))
            b = Decimal(str(orderP.total_weight_charge))
            d = Decimal(str(orderP.internal_shipping_charge))
            s = len(d.as_tuple().digits) - d.as_tuple().exponent - 1
            c = a + b + d
            serializer = OrderProductSerializer(orderP)

            context = {
                'order': serializer.data,
                'Due': a,
                'charge': b,
                'internal': d,
                'total': c,
            }

            return Response(context, status=status.HTTP_200_OK)
        except OrerPrduct.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class ReqPayNowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            orderP = req.objects.get(order_id=id, user=request.user.id)
            b = Decimal(str(orderP.total_weight_charge))
            d = Decimal(str(orderP.internal_shipping_charge))
            s = len(d.as_tuple().digits) - d.as_tuple().exponent - 1
            c =  b + d
            serializer = REQOrderProductSerializer(orderP)

            context = {
                'order': serializer.data,
             
                'charge': b,
                'internal': d,
                'total': c,
            }

            return Response(context, status=status.HTTP_200_OK)
        except OrerPrduct.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class ShippingPayNowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            orderP = Shipping.objects.get(shipping_id=id, user=request.user.id)
            b = Decimal(str(orderP.total_weight_charge))
            d = Decimal(str(orderP.internal_shipping_charge))
            s = len(d.as_tuple().digits) - d.as_tuple().exponent - 1
            c =  b + d
            serializer = ShippingSerializer(orderP)

            context = {
                'order': serializer.data,
             
                'charge': b,
                'internal': d,
                'total': c,
            }

            return Response(context, status=status.HTTP_200_OK)
        except OrerPrduct.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class PayforMePayNowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            orderP = payforme.objects.get(payment_id=id, user=request.user.id)
    
            serializer = payformeSerializer(orderP)

            context = {
                'order': serializer.data,
             
                'total': orderP.p_total,
            }

            return Response(context, status=status.HTTP_200_OK)
        except OrerPrduct.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


import urllib.parse
def get_sizes_for_color(request, product_id, color):
    decoded_text = urllib.parse.unquote(color)

    print(decoded_text)
    # Assuming you have a Size model with product and color fields
    sizes = skusize.objects.filter(product=product_id, color=decoded_text)
    dollar_rate = 130

    size_data = []
    for size in sizes:
        p=size.price
        if p:
            # Define a regular expression pattern to match decimal numbers
            pattern = r'\d+\.\d+'

            # Find all matches of the pattern in the data
            matches = re.findall(pattern, p)

            # Convert the matches to float and store them in a list
            decimal_numbers = [float(match) for match in matches]
        minimum_value = ''
        # Check if there are valid decimal numbers
        if p:
            if decimal_numbers:
                # Find the minimum value
                result = [number * 130 for number in decimal_numbers]
                minimum_values = min(result)
                minimum_value = Decimal(minimum_values)
                rounded_result = minimum_value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                print("Extracted decimal numbers:", decimal_numbers)
                print("Minimum value:", rounded_result)
        else:
            product = Product.objects.get(product_no=product_id)
            product_price = ProductPrice.objects.filter(product=product).first()
            
            if product_price:
                minimum_value = Decimal(product_price.price )
            else:
                skusizes = skusize.objects.filter(product=product)
                if skusizes:
                    price_list = [sku.price for sku in skusizes]
                    minimum_value = price_list[0] 
            result = Decimal(minimum_value) * dollar_rate

            # Round the result to two decimal places using quantize
            rounded_result = result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        size_data.append({
            'color': size.color,
            'size': size.size,
            'price': rounded_result,
            'quantity': 0,
        })

    return JsonResponse({'sizes': size_data})

def get_highest_lowest_prices(request, product_id):
    # Calculate the highest and lowest prices
    price_stats = skusize.objects.filter(
        price__isnull=False,
        product_id=product_id
    )
    p_list = []
    for i in price_stats:
        if i.price:
            p_list.append(i.price)

    prices = [float(price) for price in p_list[0].split('\n') if price.strip()]
    if len(prices) > 1:
        # Find the highest and lowest prices
        highest_price = max(p_list, key=float)  # Convert to float for numerical comparison
        lowest_price = min(p_list, key=float)
    else:
        # There's only one data point, so it's both the highest and lowest price
        highest_price = p_list[0]
        lowest_price = 'None'

    # Return the results in JSON format
    data = {
        "highest_price": highest_price,
        "lowest_price": lowest_price
    }
    print(data)
    return JsonResponse(data)

def carts(request):
    kalk = request.user
    cart = add_to_carts.objects.filter(User_id = kalk.id)
    cart_count = add_to_carts.objects.filter(User_id = kalk.id).count()
    return render(request, 'pages/cart.html',{'cart':cart,'cart_count':cart_count})

def carts_delete (request, id):
    kalk = request.user
    cart = add_to_carts.objects.filter(id=id,User_id = kalk.id)
    cart.delete()
    messages.success(request, 'Product Successfully Deleted')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

from django.contrib.auth.models import User





def order_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = OrerPrduct.objects.filter(user_id=request.user.id)[offset:offset + limit]
    serializer = OrderProductSerializer(data, many=True)

    return JsonResponse({'orders_p': serializer.data})





from django.db.models import Sum


class ReqOrderAPIView(APIView):
    def get(self, request):
        kalk = request.user
        reqo = req.objects.filter(user_id=kalk.id)
        recount = req.objects.filter(user_id=kalk.id).count()
        unpaid = req.objects.filter(user_id=kalk.id, status='Un Paid').count()
        rq = req.objects.filter(user_id=kalk.id, status='Partial Payment Received').count()
        totalamount = req.objects.filter(user_id=kalk.id, status='Order Received').aggregate(
            total=Sum('total_weight_charge') + Sum('internal_shipping_charge'))['total']
        total_amount = req.objects.filter(user_id=kalk.id, status='Un Paid').aggregate(
            total=Sum('price'))['total']

        serializer = ReqOrderSerializer({
            'reqo': reqo,
            'recount': recount,
            'rq': rq,
            'unpaid': unpaid,
            'totalamount': totalamount,
            'total_amount': total_amount,
        }, context={'user': request.user, 'reqo': reqo}, many=False)

        return Response(serializer.data)
    
    
class ShippingAPIView(APIView):
    def get(self, request):
        user = request.user
        reqo = Shipping.objects.filter(user=user)
        recount = reqo.count()
        unpaid = reqo.filter(p_status='Un_Paid').count()
        rq = reqo.filter(status='Partial Payment Received').count()
        
        totalamount = reqo.filter(status='Order Received').aggregate(
            total=Sum('total_weight_charge') + Sum('internal_shipping_charge')
        )['total'] or 0

        total_amount = reqo.filter(p_status='Un_Paid').aggregate(
            total=Sum('total_weight_charge') + Sum('internal_shipping_charge')
        )['total'] or 0

        serializer = ShippingSerializer(reqo, many=False)

        return Response(serializer.data)
    

class PaymentOrderAPIView(APIView):
    def get(self, request):
        user = request.user
        shipping_orders = payforme.objects.filter(user_id=user.id)
        total_amount = shipping_orders.filter(status='Un_Paid').aggregate(
            total=Sum('p_total'))['total']

        serializer = PaymentOrderSerializer({
            'paymentorder': shipping_orders,
            'total_orders': shipping_orders.count(),
            'unpaid_orders': shipping_orders.filter(status='Un_Paid').count(),
            'partial_payment_received_orders': shipping_orders.filter(status='Partial Payment Received').count(),
            'total_amount': total_amount,
        }, context={'user': user, 'shipping_orders': shipping_orders}, many=False)

        return Response(serializer.data)
    

class ShippingOrderAPIView(APIView):
    def get(self, request):
        user = request.user
        shipping_orders = Shipping.objects.filter(user_id=user.id)
        total_amount = shipping_orders.filter(status='Un_Paid').aggregate(
            total=Sum('total_weight_charge'))['total']

        serializer = ShippingOrderSerializer({
            'shipping_orders': shipping_orders,
            'total_orders': shipping_orders.count(),
            'unpaid_orders': shipping_orders.filter(status='Un_Paid').count(),
            'partial_payment_received_orders': shipping_orders.filter(status='Partial Payment Received').count(),
            'total_amount': total_amount,
        }, context={'user': user, 'shipping_orders': shipping_orders}, many=False)

        return Response(serializer.data)


class OrderPartialPaymentCreateAPIView(APIView):
    serializer_class = Order_Partial_PaymentSerializer

    def post(self, request, *args, **kwargs):
        print(request.data['orderi'])
        print(request.user)
        odr = OrerPrduct.objects.filter(orderi=request.data['orderi'])
        print(odr)
        # Modify the serializer data to include the current user
        serializer_data = {
            'user': request.user,  # Assuming user is a foreign key field in Order_Partial_Payment
            'orderi': odr,  # Assuming user is a foreign key field in Order_Partial_Payment
            **request.data,
        }
        print(serializer_data)
        serializer = Order_Partial_PaymentSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)

        # Save the Order_Partial_Payment instance
        self.perform_create(serializer)

        # Update the related OrerPrduct status
        orderi_instance = serializer.validated_data['orderi']
        orderi_instance.status = 'Partial Payment Pending'
        orderi_instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    

@login_required
def reqorderd(request, id):
    kalk = request.user
    
  
    user_profile = User.objects.filter(username = kalk)
    reqo = req.objects.filter(id = id)
    aamount = wallet.objects.filter(user_id = kalk.id, status = 'Approved')
    camount = wallet.objects.filter(user_id = kalk.id, status = 'Cancel')
    l = 0
    j = 0
    ska = 0
    for rk in camount:
        t = (Decimal(rk.amount))
        j =(j+t)
    for rs in aamount:
        total = (Decimal(rs.amount))
        l =(l+total)
    ska = l-j
    
    context = {
        'profile':user_profile,
        'reqo':reqo,
        'wallettotal':ska,
        
        
        }
    return render(request, 'pages/reqorderd.html',context)

@login_required
def reqpay(request,  id):
    kalk = request.user
    
  
    user_profile = User.objects.filter(username = kalk)
    reqo = req.objects.filter(id = id)
    if request.method == "POST":
        link = request.POST.get('link')
        title = request.POST.get('title')
        message = request.POST.get('message')
        p_image = request.POST.get('p_image')
        weight_charge = request.POST.get('weight_charge')
        price = request.POST.get('price')
        created_at = datetime.datetime.now()
        quantity = request.POST.get('quantity')
        order_id = request.POST.get('order_id')
        t_m = request.POST.get('t_m')
        t_id = request.POST.get('t_id')
        t_img = request.POST.get('t_img')
        if t_m == "Wallet":
            kak = wallet()
            kak.user_id = kalk.id
            kak.status = "Cancel"
            kak.amount = price
            kak.note = "order payment"
            kak.t_id = "order payment"
            kak.t_m = "order payment"
            kak.save()
            emp = req(
                id = id,
                link = link,
                title = title,
                p_image = p_image,
                weight_charge = weight_charge,
                created_at = created_at,
                price = price,
                quantity = quantity,
                user = kalk,
                order_id = order_id,
                message = message,
                ps_status = "Paid",
                t_m = t_m,
                t_id = t_id,
                t_img = t_img,
            )
            emp.save()
        else:
            emp = req(
                id = id,
                link = link,
                title = title,
                p_image = p_image,
                weight_charge = weight_charge,
                created_at = created_at,
                price = price,
                quantity = quantity,
                user = kalk,
                order_id = order_id,
                message = message,
                ps_status = "Un_Paid",
                t_m = t_m,
                t_id = t_id,
                t_img = t_img,
            )
            emp.save()
        messages.success(request, 'Payment Sent Succefull')
           
           
       
    else:
        print("something wents wrong last")


    context = {
        'profile':user_profile,
        'reqo':reqo,
        
        
        }
    return redirect('reqorderd',id)


@login_required
def shipped(request):
    kalk = request.user
    
  
    user_profile = User.objects.filter(username = kalk)
    shipping = Shipping.objects.filter(user_id = kalk.id).order_by("-created_at")
    sc = Shipping.objects.filter(user_id = kalk.id, status = 'Payment Confirm').count()
    scs = Shipping.objects.filter(user_id = kalk.id, status = 'Payment Confirm')
    aamount = wallet.objects.filter(user_id = kalk.id, status = 'Approved')
    camount = wallet.objects.filter(user_id = kalk.id, status = 'Cancel')
    l = 0
    j = 0
    ska = 0
    for rk in camount:
        t = (Decimal(rk.amount))
        j =(j+t)
    for rs in aamount:
        total = (Decimal(rs.amount))
        l =(l+total)
    ska = l-j
    
    context = {
        'profile':user_profile,
        'shipping': shipping,
        'wallettotal':ska,
        'sc':sc,
        'scs':scs,
        
        }
    return render(request, 'pages/shipped.html',context)
    
@login_required
def shippedpay(request,  id):
    kalk = request.user
    
  
    user_profile = User.objects.filter(username = kalk)
    shippingd = Shipping.objects.filter(id = id)
    if request.method == "POST":
        shipping_id = request.POST.get('shipping_id')
        product = request.POST.get('product')
        quantity = request.POST.get('quantity')
        note = request.POST.get('note')
        tracking = request.POST.get('tracking')
        image = request.POST.get('image')
        created_at = datetime.datetime.now()
        s_total = request.POST.get('s_total')
        status = request.POST.get('status')
        total_weight = request.POST.get('total_weight')
        weight_charge = request.POST.get('weight_charge')
        country = request.POST.get('country')
        t_m = request.POST.get('t_m')
        t_id = request.POST.get('t_id')
        t_img = request.POST.get('t_img')
        emp = Shipping(
            id = id,
            shipping_id = shipping_id,
            product = product,
            quantity = quantity,
            note = note,
            created_at = created_at,
            tracking = tracking,
            image = image,
            user = kalk,
            s_total = s_total,
            total_weight = total_weight,
            weight_charge = weight_charge,
            status = status,
            country = country,
            t_m = t_m,
            p_status = "Un_Paid",
            t_id = t_id,
            t_img = t_img,
        )
        emp.save()
        messages.success(request, 'Payment Sent Succefull')
           
           
       
    else:
        print("something wents wrong last")


    
    return redirect('shipped')


@login_required
def delivery(request):
    kalk = request.user
    user_profile = User.objects.filter(username = kalk)
    
  
    
    context = {
        'profile':user_profile,
        
        }
    return render(request, 'pages/delivery.html',context)

@login_required
def payment(request):
    kalk = request.user
    user_profile = User.objects.filter(username = kalk)
    payments = payforme.objects.filter(user_id = kalk.id).order_by("-created_at")
    
    
    context = {
        'profile':user_profile,
        'payments':payments
        
        }
    return render(request, 'pages/paysforme.html',context)

@login_required
def paymentpayss(request,  id):
    kalk = request.user
    user_profile = User.objects.filter(username = kalk)
    shippingd = payforme.objects.filter(payment_id = id)

    context = {
        'profile':user_profile,
        'shippingd':shippingd,
        
        }
    return render(request, 'pages/partial/pays.html',context)


@login_required
def paymentpay(request,  id):
    kalk = request.user
    
  
    user_profile = User.objects.filter(username = kalk)
    if request.method == "POST":
        t_m = request.POST.get('t_m')
        t_id = request.POST.get('t_id')
        t_img = request.POST.get('t_img')
        shippingd = payforme.objects.get(payment_id = id)
        if t_m == 'Wallet':
            shippingd.t_m = t_m
            shippingd.p_status = 'Paid'
            shippingd.status = 'Payment SucessFull'
            shippingd.t_id = t_id
            shippingd.t_img = t_img
            shippingd.save()
            messages.success(request, 'Payment Sent Succefull')
        else:
            shippingd.t_m = t_m
            shippingd.t_id = t_id
            shippingd.t_img = t_img
            shippingd.save()
            messages.success(request, 'Payment Sent Succefull')
    else:
        pass
    return redirect('payment')


@login_required
def partial_payments(request):
    kalk = request.user
    user_profile = User.objects.filter(username = kalk)
    op = Order_Partial_Payment.objects.filter(user_id = kalk.id)
    rq = Req_Order_Partial_Payment.objects.filter(user_id = kalk.id)
    
    context = {
        'profile':user_profile,
        'op' : op,
        'rq' : rq,
        
        }
    return render(request, 'pages/partial_payments.html',context)
@login_required
def delivery_req(request):
    kalk = request.user
    user_profile = User.objects.filter(username = kalk)
    od = ORequest_Delivery.objects.filter(user_id = kalk.id)
    qd = RRequest_Delivery.objects.filter(user_id = kalk.id)
    sd = SRequest_Delivery.objects.filter(user_id = kalk.id)
    
    context = {
        'profile':user_profile,
        'op' : od,
        'qd' : qd,
        'sd' : sd,
        
        }
    return render(request, 'pages/delivery_req.html',context)

@login_required
def ticket(request):
    kalk = request.user
    user_profile = User.objects.filter(username = kalk)
    tickets = sticket.objects.filter(user_id = kalk.id)
    
  
    
    context = {
        'profile':user_profile,
        'tickets':tickets,
        
        }
    return render(request, 'pages/ticket.html',context)
@staff_member_required 
def ticketadmin(request):
    kalk = request.user
    user_profile = User.objects.filter(username = kalk)
    tickets = sticket.objects.all()
    
  
    
    context = {
        'profile':user_profile,
        'tickets':tickets,
        
        }
    return render(request, 'pages/ticket_admin.html',context)
@login_required
def ticketdetails(request,ticket_no, id):
    kalk = request.user
    

    user_profile = User.objects.filter(username = kalk)
    ticket = sticket.objects.filter(id=id)
    tsms = smst.objects.filter(ticketi = ticket_no)


    
    context = {
        'profile':user_profile,
        'ticket':ticket,
        'tsms':tsms,
 
        
        }
    return render(request, 'pages/ticket_detail.html',context)

from django.core import serializers
def ticket_details_ajax(request, ticket_no, id):
    tsms = smst.objects.filter(ticketi=ticket_no)
    tsms_list = []
    for i in tsms:
        tsms_list.append({
            'user': i.user.username,
            'created_at': i.created_at,
            'message': i.messae,
        })
    return JsonResponse(tsms_list, safe=False)

@login_required
def ticketdetailsreq(request, ticket_no):
    kalk = request.user
    if request.method == "POST":
        msg = request.POST.get('messae')
        id = sticket.objects.get(ticket_no=ticket_no)
        sms = smst(ticketi=id, user=kalk, messae=msg)
        sms.save()
        response_data = {'success': True, 'message': 'Message Sent Successfully'}
        return JsonResponse(response_data)
    else:
        response_data = {'success': False, 'message': 'Something Went Wrong'}
        return JsonResponse(response_data)

@login_required
def ticketadd(request):
    kalk = request.user
    user_profile = User.objects.filter(username = kalk)
    form = sticketForm()
    
    context = {
        'profile':user_profile,
        'form':form,
        
        }
    return render(request, 'pages/ticket_add.html',context)
@login_required
def ticketaddreq(request):
    kalk = request.user
    user_profile = User.objects.filter(username = kalk)
    if request.method == "POST":
        form = sticketForm(request.POST, request.FILES)
        orders = 60000001 if sticket.objects.count() == 0 else sticket.objects.aggregate(max=Max('ticket_no')) ["max"]+1
        if form.is_valid():
            thought = form.save(commit=False)
            thought.ticket_no = orders
            thought.order_id = form.cleaned_data['order_id']
            thought.subject = form.cleaned_data['subject']
            thought.message = form.cleaned_data['message']
            thought.user_id = kalk.id
            thought.save()
           
            messages.success(request, 'Ticket Creacted Succefull')
            ticket = sticket.objects.filter(ticket_no = orders)
            context = {
                'profile':user_profile,
                'ticket':ticket,
                }
            return redirect('ticket')
        else:
            messages.error(request, 'Something Wents Wrong')

            form = sticketForm()
    else:
        form = sticketForm()
    
  
    return redirect('ticketadd')

@login_required
def walletall(request):
    kalk = request.user
    user_profile = User.objects.filter(username = kalk)
    w1 = wallet.objects.filter(user_id = kalk.id)

    context = {
        'profile':user_profile,
        'w1' : w1,
        
        }
    return render(request, 'pages/wallet.html',context)
@login_required
def walletadd(request):
    kalk = request.user
    user_profile = User.objects.filter(username = kalk)
    
  
    if request.method == "POST":
        form = walletForm(request.POST, request.FILES)
        if form.is_valid():
            thought = form.save(commit=False)
            thought.user_id = kalk.id
            thought.amount = form.cleaned_data['amount']
            thought.note = form.cleaned_data['note']
            thought.t_m = form.cleaned_data['t_m']
            thought.t_id = form.cleaned_data['t_id']
            thought.save()
           
            messages.success(request, 'Wallet Requestt Succefull')
            
            return redirect('wallet')
        else:
            messages.error(request, 'Something Wents Wrong')

            form = walletForm()
    else:
        form = walletForm()

    form = walletForm()
    context = {
        'profile':user_profile,
        'form':form,
        
        
        }
    return render(request, 'pages/walletadd.html',context)


def about(request):

    return render(request, 'pages/about.html')

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        form = add_to_cartForm(request.POST)
        if form.is_valid():
            thought = form.save(commit=False)
            thought.User = request.user
            thought.save()
            messages.success(request, 'Product Successfully Added')
        else:
            return HttpResponse('invalid Form', status=200)
    form = add_to_cartForm()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def shop(request):
    product = Product.objects.all().order_by("-created_at")[:10]
    total_data = Product.objects.count()
    context = {
        'product': product,
        'total_data':total_data,
        }
    return render(request, 'pages/shop.html', context)


# class ShopAPIView(generics.GenericAPIView):
#     def ShopAPI(self, request):
#         products = Product.objects.all().order_by("-created_at")[:10]
#         total_data = Product.objects.count()
#         serializer = ProductSerializer(products, many=True)

#         response_data = {
#             'products': serializer.data,
#             'total_data': total_data,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)



def ShopAPIView(request):
    num_products = 10
    num_products = int(num_products)  # Convert to an integer

    products = Product.objects.all()[:num_products]
    product_list = []

    for product in products:
        product_data = {
            'id': product.id,
            'product_no': product.product_no,
            'name': product.name,
            'link': product.link,
        }

        product_price = ProductPrice.objects.filter(product=product).first()

        if product_price:
            product_data['price'] = product_price.price
            product_data['saleprice'] = product_price.saleprice
            product_data['proprice'] = product_price.proprice
            product_data['m1'] = product_price.m1
            product_data['m2'] = product_price.m2
        else:
            skusizes = skusize.objects.filter(product=product)
            if skusizes:
                # Assuming 'price' is an attribute of the 'skusize' model
                # Iterate through all related skusizes and append their prices to a list
                price_list = [sku.price for sku in skusizes]
                # You may choose to use the first price or some other logic
                # Here, we're using the first price in the list
                product_data['price'] = price_list[0]

        first_image = ProductImage.objects.filter(product=product).first()
        if first_image:
            product_data['image'] = first_image.image
        else:
            product_data['image'] = ''

        product_list.append(product_data)

    return JsonResponse({'products': product_list})
    

def load_more_data(request):
    try:
        offset = int(request.GET['offset'])
        limit = int(request.GET['limit'])
    except ValueError:
        return JsonResponse({'error': 'Invalid offset or limit provided'})

    data = Product.objects.all()[offset:offset+limit]

    product_list = []

    for product in data:
        product_data = {
            'id': product.id,
            'product_no': product.product_no,
            'name': product.name,
            'link': product.link,
        }

        product_price = ProductPrice.objects.filter(product=product.product_no).first()

        if product_price:
            product_data['price'] = product_price.price
            product_data['saleprice'] = product_price.saleprice
            product_data['proprice'] = product_price.proprice
            product_data['m1'] = product_price.m1
            product_data['m2'] = product_price.m2
        else:
            skusizes = skusize.objects.filter(product=product.product_no)
            if skusizes:
                price_list = [sku.price for sku in skusizes]
                product_data['price'] = price_list[0]

        first_image = ProductImage.objects.filter(product=product.product_no).first()
        second_image = ProductImage.objects.filter(product=product.product_no).exclude(id=first_image.id).first()
        if first_image.image.startswith('https://video01'):
            product_data['image'] = second_image.image # Assuming 'image' is a FileField
        else:
            product_data['image'] = first_image.image # Assuming 'image' is a FileField
               
      

        product_list.append(product_data)
    pro_ctn = Product.objects.all().count()

    return JsonResponse({'product': product_list, 'total': pro_ctn})


# # catagory lists

# apparel_list
def apparel_list(request):
    product = Catagorys.objects.filter(catagory ='Apparel')[:10]
    total_data = Catagorys.objects.filter(catagory ='Apparel').count()
    context = {
        'product': product,
        'total_data':total_data,
        }
    return render(request, 'pages/afilter.html', context)

def apparel_list_more(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data = Catagorys.objects.filter(catagory ='Apparel')[offset:offset+limit]
	t = render_to_string('pages/partial/myaccount/list.html',{'product':data})
	return JsonResponse({'product':t})


# Shoes_Accessories
def Shoes_Accessories(request):
    product = Catagorys.objects.filter(catagory ='Shoes & Accessories')[:10]
    total_data = Catagorys.objects.filter(catagory ='Shoes & Accessories').count()
    context = {
        'product': product,
        'total_data':total_data,
        }
    return render(request, 'pages/ssfilter.html', context)

def Shoes_Accessoriesmore(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data = Catagorys.objects.filter(catagory ='Shoes & Accessories')[offset:offset+limit]
	t = render_to_string('pages/partial/myaccount/list.html',{'product':data})
	return JsonResponse({'product':t})


# Luggage_Bags 
def Luggage_Bags(request):
    product = Catagorys.objects.filter(catagory ='Luggage, Bags & Cases')[:10]
    total_data = Catagorys.objects.filter(catagory ='Luggage, Bags & Cases').count()
    context = {
        'product': product,
        'total_data':total_data,
        }
    return render(request, 'pages/llfilter.html', context)

def Luggage_Bags_more(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data = Catagorys.objects.filter(catagory ='Luggage, Bags & Cases')[offset:offset+limit]
	t = render_to_string('pages/partial/myaccount/list.html',{'product':data})
	return JsonResponse({'product':t})

# Vehicle_Accessories_list
def Vehicle_Accessories_list(request):
    product = Catagorys.objects.filter(catagory ='Vehicle Parts & Accessories')[:10]
    total_data = Catagorys.objects.filter(catagory ='Vehicle Parts & Accessories').count()
    context = {
        'product': product,
        'total_data':total_data,
        }
    return render(request, 'pages/vfilter.html', context)

def Vehicle_Accessories_list_more(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data = Catagorys.objects.filter(catagory ='Vehicle Parts & Accessories')[offset:offset+limit]
	t = render_to_string('pages/partial/myaccount/list.html',{'product':data})
	return JsonResponse({'product':t})

# Sports_Entertainment_list
def Sports_Entertainment_list(request):
    product = Catagorys.objects.filter(catagory ='Sports & Entertainment')[:10]
    total_data = Catagorys.objects.filter(catagory ='Sports & Entertainment').count()
    context = {
        'product': product,
        'total_data':total_data,
        }
    return render(request, 'pages/sfilter.html', context)

def Sports_Entertainment_list_more(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data = Catagorys.objects.filter(catagory ='Sports & Entertainment')[offset:offset+limit]
	t = render_to_string('pages/partial/myaccount/list.html',{'product':data})
	return JsonResponse({'product':t})
	
	
# machinery_list
def machinery_list(request):
    product = Catagorys.objects.filter(catagory ='Machinery')[:10]
    total_data = Catagorys.objects.filter(catagory ='Machinery').count()
    context = {
        'product': product,
        'total_data':total_data,
        }
    return render(request, 'pages/mfilter.html', context)


def machinery_list_more(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data = Catagorys.objects.filter(catagory ='Machinery')[offset:offset+limit]
	t = render_to_string('pages/partial/myaccount/list.html',{'product':data})
	return JsonResponse({'product':t})


# consumer_electronic
def consumer_electronic(request):
    product = Catagorys.objects.filter(catagory ='Consumer Electronics')[:10]
  
    total_data = Catagorys.objects.filter(catagory ='Consumer Electronics').count()
    context = {
        'product': product,
        'total_data':total_data,
        }
    return render(request, 'pages/efilter.html', context)


def consumer_electronic_more(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data = Catagorys.objects.filter(catagory ='Consumer_Electronic')[offset:offset+limit]
	t = render_to_string('pages/partial/myaccount/list.html',{'product':data})
	return JsonResponse({'product':t})


# Fabric_Material
def Fabric_Material(request):
    product = Catagorys.objects.filter(catagory ='Fabric & Textile Raw Material')[:10]
    total_data = Catagorys.objects.filter(catagory ='Fabric & Textile Raw Material').count()
    context = {
        'product': product,
        'total_data':total_data,
        }
    return render(request, 'pages/fffilter.html', context)


def Fabric_Material_more(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data = Catagorys.objects.filter(catagory ='Fabric & Textile Raw Material')[offset:offset+limit]
	t = render_to_string('pages/partial/myaccount/list.html',{'product':data})
	return JsonResponse({'product':t})

# home_garden
def home_garden(request):
    product = Catagorys.objects.filter(catagory ='Home & Garden')[:10]
    total_data = Catagorys.objects.filter(catagory ='Home & Garden').count()
    context = {
        'product': product,
        'total_data':total_data,
        }
    return render(request, 'pages/hfilter.html', context)


def home_garden_more(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data = Catagorys.objects.filter(catagory ='Home & Garden')[offset:offset+limit]
	t = render_to_string('pages/partial/myaccount/list.html',{'product':data})
	return JsonResponse({'product':t})



# beauty_personal_care
def beauty_personal_care(request):
    product = Catagorys.objects.filter(catagory ='Beauty & Personal Care')[:10]
    total_data = Catagorys.objects.filter(catagory ='Beauty & Personal Care').count()
    context = {
        'product': product,
        'total_data':total_data,
        }
    return render(request, 'pages/bfilter.html', context)


def beauty_personal_care_more(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data = Catagorys.objects.filter(catagory ='Beauty & Personal Care')[offset:offset+limit]
	t = render_to_string('pages/partial/myaccount/list.html',{'product':data})
	return JsonResponse({'product':t})

# Tools_Hardware_list
def Tools_Hardware_list(request):
    product = Catagorys.objects.filter(catagory ='Electrical Equipment & Supplies')[:10]
    total_data = Catagorys.objects.filter(catagory ='Electrical Equipment & Supplies').count()
    context = {
        'product': product,
        'total_data':total_data,
        }
    return render(request, 'pages/bfilter.html', context)


def Tools_Hardware_list_more(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data = Catagorys.objects.filter(catagory ='Electrical Equipment & Supplies')[offset:offset+limit]
	t = render_to_string('pages/partial/myaccount/list.html',{'product':data})
	return JsonResponse({'product':t})
	
	
	

@login_required
def Shippingsk(request):
    kalk = request.user
    spfd = shipformedes.objects.all()
    spfs = shipformecharge.objects.all()
    spfz = shipformemesssages.objects.all()
    note = shipformenote.objects.all()
    pro = Profile.objects.get(user = kalk.id)
    
  
    if request.method == "POST":
        form = ShippingForm(request.POST, request.FILES)
        orders = 40000001 if Shipping.objects.count() == 0 else Shipping.objects.aggregate(max=Max('shipping_id')) ["max"]+1
        if form.is_valid():
            thought = form.save(commit=False)
            thought.shipping_id = orders
            thought.country = form.cleaned_data['country']
            thought.product = form.cleaned_data['product']
            thought.quantity = form.cleaned_data['quantity']
            thought.tracking = form.cleaned_data['tracking']
            thought.note = form.cleaned_data['note']
            thought.phone = pro.mobile
            thought.image = form.cleaned_data['image']
            thought.user_id = kalk.id
            thought.save()
            
            messages.success(request, 'Requested Successfully')
            ph = pro.mobile
            name =  pro.user.username
            ordernumber = str(orders)
            message = "Hi " + name + ","+"\n"+"Your Shipping Request Submited Successfully.\n Thank You for Staying With Us.." +"\n Your Shipping Request ID: "+ ordernumber+  "\n Visit Us: https://ecargo.com.bd/order/"
            
            url = "http://apismpp.ajuratech.com/sendtext"

            querystring = {"apikey":"a6584c5c4908024d","secretkey":"80b5d891","callerID":"quickcartbd","toUser":ph,"messageContent":message}
            headers = {
                'cache-control': "no-cache",
                }

            response = requests.request("GET", url, headers=headers, params=querystring)
     
        
            
        else:
            messages.success(request,'Somethting Wents Wrong!!')
    form = ShippingForm()
   

    context = {
      'form': form,
      'shipdes': spfd,
      'note':note,
      'spfs':spfs,
      'spfz':spfz,
      
        }
    return render(request, 'pages/shipforme.html', context)



@login_required
def paysforme(request):
    kalk = request.user
    note = payformenote.objects.all()
    pro = Profile.objects.get(user = kalk.id)
    
  
    if request.method == "POST":
        form = payformeForm(request.POST, request.FILES)
        orders = 50000001 if payforme.objects.count() == 0 else payforme.objects.aggregate(max=Max('payment_id')) ["max"]+1
        if form.is_valid():
            thought = form.save(commit=False)
            thought.payment_id = orders
            thought.user_id = kalk.id
            thought.product_link = form.cleaned_data['product_link']
            thought.product_name = form.cleaned_data['product_name']
            thought.phone = pro.mobile
            thought.note = form.cleaned_data['note']
            thought.save()
            
            messages.success(request, 'Requested Successfully')
            ph = pro.mobile
            name =  pro.user.username
            ordernumber = str(orders)
            message = "Hi " + name + ","+"\n"+"Your Payment Request Submited Successfully.\n Thank You for Staying With Us.." +"\n Your Payment Request ID: "+ ordernumber+  "\n Visit Us: https://ecargo.com.bd/order/"
            
            url = "http://apismpp.ajuratech.com/sendtext"

            querystring = {"apikey":"a6584c5c4908024d","secretkey":"80b5d891","callerID":"quickcartbd","toUser":ph,"messageContent":message}
            headers = {
                'cache-control': "no-cache",
                }

            response = requests.request("GET", url, headers=headers, params=querystring)

            
        else:
            messages.success(request,'Somethting Wents Wrong!!')
    form = payformeForm()
   

    context = {
      'form': form,
      'note':note,
      
        }
    return render(request, 'pages/payforme.html', context)
    
    
    
def faqs(request):
    
    faq = Faq_page.objects.all()
    context = {
        
        'faq':faq
        }
    return render(request, 'pages/faqs.html',context)
    
def terms_condition(request):
    faq = terms_condition_page.objects.all()
    context = {
        
        'faq':faq
        }
    return render(request, 'pages/terms_condition.html',context)
    
def forbidenitempagen(request):
    faq = forbidenitempagen_page.objects.all()
    context = {
        
        'faq':faq
        }
    return render(request, 'pages/forbidenitempagen.html',context)

def Shipping_refund_Pollicy(request):
    faq = Shipping_refund_Pollicy_page.objects.all()
    context = {
        
        'faq':faq
        }
    return render(request, 'pages/Shipping_refund_Pollicy_page.html',context)


def Privacy_Policy(request):
    faq = Privacy_Policy_page.objects.all()
    context = {
        
        'faq':faq
        }
    return render(request, 'pages/Privacy_Policy.html',context)



