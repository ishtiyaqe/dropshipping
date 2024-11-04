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
from bs4 import BeautifulSoup
from django.conf import settings
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
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import (ElementNotSelectableException,
                                        ElementNotVisibleException, TimeoutException,)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework.settings import api_settings
from rest_framework.test import APIClient
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from selenium.common.exceptions import NoSuchElementException
from store.views import *
from store.models import *
from order.models import *
from accounts.models import *
from snipet.models import *
import uuid
from store.forms import *
from order.forms import *
import json
# import chromedriver_binary
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import generics
from store.serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.core.serializers import serialize
from urllib.parse import urlparse
from .models import *
from django.http import request
import requests
import threading


def replace_single_quotes_with_double_quotes(match):
                return f'"{match.group(1)}"'


def descriptions(ps, newurl):
    chrome_driver_path = r"C:\\Users\\gisht\\AppData\\Local\\Google\\Chrome SxS\\Application\\chrome.exe"

    # set chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.binary_location = chrome_driver_path
    # set desired capabilities
    # capabilities = DesiredCapabilities.CHROME.copy()
    # capabilities["pageLoadStrategy"] = "none"

    # create webdriver instance
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 5)

    # navigate to the URL
    driver.get(newurl)


    time.sleep(5)

    # wait for the element to load
    try:
        wait.until(EC.presence_of_element_located((By.ID, 'detail-next-loading-wrap')))
    except:
        wait.until(EC.presence_of_element_located((By.ID, 'module_product_specification')))
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'module-detailRecommendProducts')))
        # wait.until(EC.presence_of_element_located((By.ID, 'product_detail_property')))

    # stop the page load using JavaScript Executor
    driver.execute_script("window.stop();")

    # short description
    try:
        shortd = driver.find_element(By.CLASS_NAME, 'do-overview')
        kd = shortd.get_attribute("outerHTML")
        sd = BeautifulSoup(kd, 'html.parser')
        kd = sd.find('div', attrs={'class': 'do-entry do-entry-separate'})
        kdd = kd.find_all('dt')
        kll = kd.find_all('dd')
        for i,j in  zip(kdd,kll):
            kas = i.text
            kad = j.text
            ProductDes.objects.create(product_id=ps, shortdes=kas,fulldes=kad)
    except:
        pass


    # full description
    try:
        prodes = driver.find_element(By.ID, 'module_product_specification')
        pdes = prodes.get_attribute('outerHTML')
        proddes = BeautifulSoup(pdes, 'html.parser')

        img_tags = proddes.find_all('img')
        for img in img_tags:
                data_src = img.get('data-src')
                if data_src is not None:
                    description.objects.create(product_id=ps,des = data_src)    
      
    except:
             
        pass    
    
    # reviews
    reviewsk = driver.find_element(By.CLASS_NAME,'review-list')
    rew = reviewsk.get_attribute('outerHTML')
    ravi = BeautifulSoup(rew, 'html.parser')
    review_items = ravi.find_all('div', class_='review-item')
    try:
        for item in review_items:
            buyer_name = item.find('div', class_='name').text
            text_list = item.find('div', class_='country').text.split('\n')
            country = [text for text in text_list if text.strip()][0]
            review_time = item.find('div', class_='time').text
            review_text = item.find('div', class_='content').text.strip()
            reviews.objects.create(product_id=ps,Buyer_name = buyer_name,Country = country,Review_time = review_time,Review_text  = review_text )            
    except:
        for item in review_items:
            print(item)
            name_div = item.select_one('div.review-item div.avatar-item div.name')

            # Check if the div with class 'name' exists before accessing its text
            buyer_name = name_div.text if name_div else None
            imgs_with_flags = item.select('div.review-item img[src*="/flags/"]')
            l=''
            # Print the results
            for img in imgs_with_flags:
                l = img['src']
                print(img['src'])
            try:
                review_time = item.select_one('span.date').text
            except:
                review_time = None
            review_text = item.find('div', class_='review-info').text.strip()
            reviews.objects.create(product_id=ps,Buyer_name = buyer_name,Country = l,Review_time = review_time,Review_text  = review_text )            
        


    driver.close()
    return



def product_class(products):
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
                valid_price = next((price for price in price_list if price.replace('.', '').isdigit()), None)
                # You may choose to use the first price or some other logic
                # Here, we're using the first price in the list
                product_data['price'] = Decimal(valid_price)*Decimal(dtk)

        first_image = ProductImage.objects.filter(product=product).first()
        last_image = ProductImage.objects.filter(product=product).last()
        if first_image:
            if 'https://video01' in first_image.image:
                product_data['image'] = first_image.image_cover
            else:
                product_data['image'] = last_image.image
        else:
            product_data['image'] = ''

        product_list.append(product_data)

    return product_list

    


def alibaba_api(x):
    try:
        # Attempt to retrieve an existing record with the same query
        search_query = SearchQuery.objects.get(query=x)
        if search_query.status == 'Completed':
            products = Product.objects.filter(link__icontains=x)
            product_list = product_class(products)
            
            return JsonResponse({'products': product_list})
        else:
            return JsonResponse({'url': x, 'status': search_query.status})
    except SearchQuery.DoesNotExist:
        # If no existing record is found, create a new one
        search_query = SearchQuery(query=x, status='Searching')
        search_query.save()
    except IntegrityError as e:
         return JsonResponse({'url': x, 'status': e})
    product_data = None
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
        q = x
        l = q
        newurl = l

    try:
        products = Product.objects.filter(link__icontains=newurl)
        if not products:
            raise ValueError

    except ValueError: 
        for product_data in newurl:
            product_data = dict()


            # Send an HTTP GET request to fetch the webpage content
            response = requests.get(newurl)
            kkas = uuid.uuid4().hex[:5].upper()
            product_data['no'] = kkas
            ps = product_data['no'] 

            if response.status_code == 200:
                # Parse the HTML content of the webpage
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all script tags in the HTML
                script_tags = soup.find_all('script')

                for script in script_tags:
                    script_content = script.get_text()

                    
                    if 'window.detailData' in script_content:
                        title = soup.find('h1').text.replace('"\"','')
                        Product.objects.create(name=title, link=newurl, product_no=ps)
                        # image data
                        productData_start = script_content.find('"product":') 
                        productData_end = script_content.find(',"seo":', productData_start)
                        product_datas = '{' + script_content[productData_start:productData_end].strip() + '}' 
                        # with open('output.json', 'w', encoding='utf-8') as file:
                        #     file.write( product_datas)
                        # print(product_datas)
                        try:
                            product_data = json.loads(product_datas)
                        except json.decoder.JSONDecodeError as e:
                            print("JSON Decode Error:", e)
                        Image_url = []
                        imgs = []
                        
                        for images in product_data['product']['mediaItems']:
                            try:
                                try:
                                    img = images['imageUrl']['big'].replace('_250x250.png','').replace('_250x250.jpg','').replace('_120x120.jpg','')
                                    imgs.append({'img':img,'cover':''})
                                except:
                                    img = images['videoUrl']['sd']['videoUrl'].replace('_250x250.png','').replace('_250x250.jpg','').replace('_120x120.jpg','')
                                    cover = images['videoCoverUrl'].replace('_250x250.png','').replace('_250x250.jpg','').replace('_120x120.jpg','')
                                    print(img)
                                    imgs.append({'img':img,'cover':cover})
                            except:
                                pass
                        for iimg in imgs:
                            if iimg not  in Image_url:
                                Image_url.append(iimg)
                        # You can print or process the data as needed
                        print(f'Image Url: {Image_url}')
                        for pic in Image_url:
                            print(pic)
                            ProductImage.objects.create(product_id=ps, image=pic['img'], image_cover = pic['cover'])
                        
                        # price data    
                        try:
                            # Look for the first occurrence of 'window.detailData' and extract JSON data
                            json_start = script_content.find('"productLadderPrices":') 
                            json_end = script_content.find('}]', json_start)
                            json_datas = '{' + script_content[json_start:json_end].strip() + '}]}' 
                            json_data = json.loads(json_datas)
                            # Print the JSON data
                            for price_info in json_data['productLadderPrices']:
                                dollar_price = price_info['dollarPrice']
                                format_price = price_info['formatPrice']
                                price_min = price_info['min']
                                price_max = price_info['max']
                                price = price_info['price']
                                # You can print or process the data as needed
                                print(f'Dollar Price: {dollar_price}')
                                if price_max == -1:
                                    print(f'Min order : {price_min} - Max order : =>')
                                    ProductPrice.objects.create(product_id=ps, price=price, m1 = price_min,  m2 = '=>')
                                else:
                                    print(f'Min order : {price_min} - Max order : {price_max}')
                                    ProductPrice.objects.create(product_id=ps, price=price, m1 = price_min,  m2 = price_max)
                                print(f'Price: {price}')

                        except:
                            skuData_start = script_content.find('"product":') 
                            skuData_end = script_content.find(',"seo":', productData_start)

                            sku_datas = '{' + script_content[skuData_start:skuData_end].strip() + '}' 
                            # print(product_datas)

                            
                            sku_data = json.loads(sku_datas)
                            price_max = sku_data['product']['price']['productRangePrices']['dollarPriceRangeHigh']
                            price_min = sku_data['product']['price']['productRangePrices']['dollarPriceRangeLow']
                            moq = sku_data['product']['moq']
                            print(f'Price : {price_min} -  {price_max}')
                            print(f'Min order : {moq} ')
                            ProductPrice.objects.create(product_id=ps, price=price_max, m1 = moq)


                        # Category
                        skuData_start = script_content.find('"seo":') 
                        skuData_end = script_content.find(',{"hrefObject":', productData_start)

                        sku_datas = '{' + script_content[skuData_start:skuData_end].strip() + ']}}}' 
                        sku_data = json.loads(sku_datas)
                        cata = sku_data['seo']['breadCrumb']['pathList'][0]['hrefObject']['name']
                        Catagorys.objects.create(product_id=ps, catagory=cata)
                   

                        # skudata
                        skuData_start = script_content.find('"product":') 
                        skuData_end = script_content.find(',"seo":', productData_start)

                        sku_datas = '{' + script_content[skuData_start:skuData_end].strip() + '}' 
                        # print(product_datas)

                        # with open('output.json', 'w', encoding='utf-8') as file:
                        #     file.write( sku_datas)
                        sku_data = json.loads(sku_datas)
                            
                        
                        
                        size = []
                        color = []
                        SKU = []
                        ls = []

                        try:
                            color_prices = {}

                            for key, value in sku_data['product']['sku']['skuInfoMap'].items():
                                color_id = int(key.split(';')[0].split(':')[1])
                              
                                # Find the color in values list based on id
                                color_info = next(
                                    (c for c in sku_data['product']['sku']['skuAttrs'][0]['values'] if c['id'] == color_id), None)
                             
                                if color_info:
                                    color_key = color_info['name']
                                    try:
                                        color_prices[color_key] = value['formatPrice']
                                        
                                        if not value['formatPrice']:
                                            raise ValueError
                                    except:
                                        print(f"Error: 'formatPrice' not found for key: {key}")
                                else:
                                    print(f"Color not found for key: {key}, color_id: {color_id}")

                            for SkuData in sku_data['product']['sku']['skuAttrs']:
                                sku_name = SkuData['name']
                                print(f'Sku Name:{sku_name}')
                                print(SkuData['values'])
                                if 'Size' in sku_name:
                                    size_attr = SkuData['values']
                                    print(size_attr)
                                    for i in size_attr:
                                        if i['type'] == 'TEXT':
                                            size.append(i['name'])
                                            print(size)
                                elif 'Color' in sku_name:
                                    color_attr = SkuData['values']
                                    for i in color_attr:
                                        if i['type'] == 'IMAGE':
                                            color.append({'name': i['name'], 'image': i['originImage']})
                                            skucolor.objects.create(product_id=ps, color=i['name'].replace('/',''), image=i['originImage'])
                                        else:
                                            color.append({'name': i['name']})
                                            skucolor.objects.create(product_id=ps, color=i['name'].replace('/',''))
                                else:
                                    size_attr = SkuData['values']
                                    for i in size_attr:
                                        if i['type'] == 'TEXT':
                                            SKU.append({'name': sku_name, 'Options': i['name']})
                                        if i['type'] == 'IMAGE':
                                            color.append({'name': i['name'], 'image': i['largeImage']})
                                            skucolor.objects.create(product_id=ps, color=i['name'].replace('/',''), image=i['largeImage'])
                            print(SKU)
                            print(SKU)
                            print(SKU)
                            for i in SKU:
                                if i['name'] not in ls:
                                    ls.append(i['name'])
                            if not color and not size and len(SKU) == 2:
                                color.append({'name': SKU[0]['Options']})
                                skucolor.objects.create(product_id=ps, color=SKU[0]['Options'].replace('/',''))

                                size.append(SKU[1]['Options'])
                            if not size:
                                for i in SKU:
                                    if len(ls) == 1:
                                        size.append(i['Options'])

                            if not size:
                                size.append('Quantity')
                                
                            if color_prices and color:
                                for color_name, price in color_prices.items():
                                        print(f"Color: {color_name}, Price: {price}")
                                        for x in color:
                                            if color_name != x['name']:
                                                print(x)
                                                skusize.objects.create(product_id=ps, size=color_name, color=x['name'], price=price)
                      
                            elif color_prices:
                            # Print the combined data
                                for color_name, price in color_prices.items():
                                    print(f"Color: {color_name}, Price: {price}")
                                    for sk in size:
                                        print(sk)
                                        skusize.objects.create(product_id=ps, size=sk, color = color_name, price=price)
                               

                            else:
                                for i in color:
                                    cl = i['name']
                                    for sk in size:
                                        skusize.objects.create(product_id=ps, size=sk, color = cl)

                            if SKU:
                                for i in SKU:
                                    sku.objects.create(product_id=ps, name=i['name'], option=i['Options'])
                            # Print other information (size, color, SKU)
                            if not color and not SKU and not color_prices and size:
                                if size == 'Quantity':
                                    skusize.objects.create(product_id=ps, size=size, color = None)
                                else:
                                    for i in size:
                                        skusize.objects.create(product_id=ps, size=i, color = None)
                                    

                        except Exception as e:
                            sk='Quantity'
                            skusize.objects.create(product_id=ps, size=sk)
                            print(f"Error: {e}")



                     
                        # # seller data
                        SellerData_start = script_content.find('"seller":') 
                        SellerData_end = script_content.find(',"seo":', productData_start)

                        Seller_datas = '{' + script_content[SellerData_start:SellerData_end].strip() + '}' 
                        # print(Seller_datas)

                        
                        Seller = []
                        Seller_data = json.loads(Seller_datas)
                        compnay_name = Seller_data['seller']['companyName']
                        compnay_country = Seller_data['seller']['companyRegisterCountry']
                        try:
                            compnay_ontimeDr = Seller_data['seller']['supplierOnTimeDeliveryRate']
                        except:
                            compnay_ontimeDr = 'None'
                        try:
                            compnay_rating = Seller_data['seller']['supplierRatingReviews']['averageStar']
                        except:
                            compnay_rating = 'None'

                        compnay_service_years = Seller_data['seller']['companyJoinYears']
                        Seller.append({'name': compnay_name, 
                                        'country': compnay_country,
                                        'On Time Delivery Rate': compnay_ontimeDr,
                                        'Seller Rating':compnay_rating,
                                        'Seller Years Of Service': compnay_service_years})
                        print(f'Seller Info:{Seller}')
                        for i in Seller:
                            SellerInfo.objects.create(product_id=ps,
                                                    seller= i['name'],
                                                    country=i['country'], 
                                                    year=i['Seller Years Of Service'],
                                                    )
                search_query.status = 'Completed'
                search_query.save()
                descriptions(ps, newurl)
                return
    


            
            
            
            
    
    return 