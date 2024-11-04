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

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework.settings import api_settings
from rest_framework.test import APIClient
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
from .views import *
from selenium.common.exceptions import (NoSuchElementException, TimeoutException, ElementNotInteractableException)
# import chromedriver_binary
from selenium.webdriver.common.action_chains import ActionChains
import re
# import chromedriver_binary
from .models import *
from snipet.models import *
from django.http import request
import demoji
import threading
from playwright.async_api import async_playwright
from PIL import Image
import pytesseract
import asyncio
from asgiref.sync import sync_to_async


@sync_to_async
def create_product(title, link, product_no):
    Product.objects.create(name=title, link=link, product_no=product_no)

@sync_to_async
def create_review(kls, text_without_emoji, rev_date, rating,text_without_emoji_rev ):
    reviews.objects.create(product_id=kls,Buyer_name = text_without_emoji,Review_time = rev_date,Review_rating=rating,Review_text  = text_without_emoji_rev )

@sync_to_async
def create_Seller(kls):
    SellerInfo.objects.create(product_id=kls,seller= 'Amazon.com',country='USA')

@sync_to_async
def create_product_image(product_no, link_href):
    ProductImage.objects.create(product_id=product_no, image=link_href)

@sync_to_async
def create_description(kls, link_href):
    description.objects.create(product_id=kls,des = link_href)

# @sync_to_async
# def create_sku_color(kls, color,src_value):
#     skucolor.objects.create(product_id=kls, color=color.replace('/', ''), image=src_value)

@sync_to_async
def create_sku_size(kls, color,p, price_text):
    if color:
        color = color.replace('/', ' or ')
    skusize.objects.create(product_id=kls, color=color, size=p, price=price_text)

@sync_to_async
def create_Sku_filter(kls, color, src_value):
    if color:
        color = color.replace('/', ' or ')
    p = skucolor.objects.filter(product_id=kls, color=color)
    if not p:
        skucolor.objects.create(product_id=kls, color=color, image=src_value)
    pt = ProductImage.objects.filter(product_id=kls)
    if not pt:
        if src_value:
            ProductImage.objects.create(product_id=kls, image=src_value)
    return 



# Function to decode CAPTCHA image
@sync_to_async
# def decode_captcha(image_url):
#     if not image_url.startswith('http'):
#         image_url = 'https:' + image_url
#     # Download the image
#     with open('captcha_image.jpg', 'wb') as f:
#         response = requests.get(image_url)
#         f.write(response.content)
#     pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
#     # Open and process the image
#     captcha_image = Image.open('captcha_image.jpg')
#     captcha_text = pytesseract.image_to_string(captcha_image)
#     captcha_text = captcha_text.upper().replace(" ", "")
#     return captcha_text
def decode_captcha(image_url):
    # Download the image
    with open('captcha_image.jpg', 'wb') as f:
        response = requests.get(image_url)
        f.write(response.content)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Open and process the image
    captcha_image = Image.open('captcha_image.jpg')
    captcha_text = pytesseract.image_to_string(captcha_image)
    return captcha_text

# proxy_list = [
#     '120.26.0.11:8880',
#     '45.76.196.51:80',
#     '188.165.213.106:80',
#     '102.132.50.49:8080',
# ]

async def amazon_api(x):
    print('threading start')
    try:
        # Attempt to retrieve an existing record with the same query
        search_query = await sync_to_async(SearchQuery.objects.get)(query=x)
        return JsonResponse({'url': x, 'status': 'Searching'})
    except SearchQuery.DoesNotExist:
        # If no existing record is found, create a new one
        search_query = SearchQuery(query=x, status='Searching')
        await sync_to_async(search_query.save)()
        print('Data created')
    except IntegrityError as e:
        return JsonResponse({'url': x, 'status': str(e)})
    # for proxy in proxy_list:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        try:
            screenshot_counter = 1
            while True:
                response = await page.goto(x)
                time.sleep(.3)
                if response.status == 200:
                    html_content = await page.content()
                    screenshot_filename = f'screenshot_load_{screenshot_counter}.png'
                    await page.screenshot(path=screenshot_filename)
                    captcha_image_url_element = await page.query_selector('img')
                    captcha_image_url = await captcha_image_url_element.get_attribute('src')
                    captcha_text = await decode_captcha(captcha_image_url)
                    print("Decoded CAPTCHA:", captcha_text)
                    
                    # Fill input box with CAPTCHA text
                    await page.fill('#captchacharacters', captcha_text)
                    
                    screenshot_filename = f'screenshot_{screenshot_counter}.png'
                    await page.screenshot(path=screenshot_filename)
                    screenshot_counter += 1 
                    
                    # Submit the form
                    await page.click('button[type="submit"]')
                    # await page.wait_for_navigation()
                    # Check if CAPTCHA is still present
                    if await page.query_selector('#captchacharacters'):
                        continue  # Continue solving CAPTCHA if it's still present
                    else:
                        print("No more CAPTCHA found. Exiting loop.")
                        break  # Exit loop if no more CAPTCHA found
                else:
                    print(f"Request failed with status code {response.status}")
                    break  # Exit loop if request fails
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:

            # time.sleep(3)
            
            
           
            await page.wait_for_load_state()
            html_content = await page.content()
    # Use BeautifulSoup to parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Continue with the rest of your code for scraping and processing
            product_data = dict()
            kkas = uuid.uuid4().hex[:5].upper()
            product_data['no'] = kkas
            kls = product_data['no']
            # Example: Extracting the title
            title_element = soup.find(id='title') or soup.find(id='truncatedTitle')
            if title_element:
                titlel = title_element.text.replace("/", " ").replace("%", " ").replace(" \ ", " ").replace(" | ", " ")
                import re
                title =  titlel
            else:
                title = "Title not found"
            print(title)
            product_data['title'] = title
            
            q = x
            l = q
            newurl = l
            await create_product(product_data['title'], newurl, product_data['no'])
            await create_Seller(kls)
            
            
            # Example: Extracting images
            images = soup.find(id='lookbook_content_div') or soup.find(id='image-block') or soup.find(id='altImages')

            if images:
                img_tags = images.find_all('img')
                for img in img_tags:
                    if 'gif' not in img.get('src') and '360_icon' not in img.get('src') and 'PKdp-play-icon-overlay_' not in img.get('src'):
                        link_href = img.get('src').replace('._AC_UF894,1000_QL80_FMwebp_','').replace('_AC_SR38,50_.','').replace('._AC_US40_','').replace('._AC_US100_','').replace('._SX342_SY445_','').replace('._AC_SY300_SX300_','').replace('L.__AC_SX300_SY300_QL70_ML2_','').replace('._SS40_','').replace('._SX342_SY445_','').replace('._SX38_SY50_CR,0,0,38,50_','').replace('._SX300_SY300_QL70_ML2_','')
                        # Process the image link as needed
                        print(link_href)
                        await create_product_image(product_data['no'], link_href)
            script_tags = soup.find_all('script')
            price = False
            for script in script_tags:
                script_content = script.get_text()
                if 'twister-js-init-dpx-data' in script_content:
                    price = True
                    productData_start = script_content.find('"dimensionValuesDisplayData" : {') 
                    productData_end = script_content.find('};', productData_start)
                    product_datas = '{' + script_content[productData_start:productData_end].strip() + '}' 
                    # print(product_datas)
                
                    try:
                        product_data = json.loads(product_datas)
                    except json.decoder.JSONDecodeError as e:
                        print("JSON Decode Error:", e)
                    size_color_info = {}
                    # try:
                    ks = []
                    for keys in product_data["dimensionsDisplay"]:
                        print(keys)
                        ks.append(keys)
                    
                    
                    meterial = ''
                    color = ''
                    for product_id, values in product_data["dimensionValuesDisplayData"].items():
                        print(len(values))
                        if len(values) == 2:
                            try:
                                try:
                                    color = values[ks.index('Color')]
                                except:
                                    color = values[ks.index('Material')]
                            except:
                                color = values[ks.index('Style')]
                                
                            if ks[0] == 'Color':
                                # If it is, skip to the next iteration (go next)
                                size = values[ks.index(ks[1])]
                            elif ks[0] == 'Material':
                                # If it is, skip to the next iteration (go next)
                                size = values[ks.index(ks[1])]
                            elif ks[0] == 'Style':
                                # If it is, skip to the next iteration (go next)
                                size = values[ks.index(ks[1])]
                            else:
                                size = values[ks.index(ks[0])]

                            size_color_info[product_id] = {"size": size, "color": color, "material": meterial}
                        
                        elif len(values) == 3:
                            # Assuming the third element is material
                        
                            if ks[0] == 'Color':
                                # If it is, skip to the next iteration (go next)
                                color = values[ks.index('Color')]
                                material = values[ks.index(ks[1])]
                                size = values[ks.index(ks[2])]
                            elif ks[1] == 'Color':
                                material = values[ks.index(ks[0])]
                                color = values[ks.index('Color')]
                                size = values[ks.index(ks[2])]
                            elif ks[2] == 'Color':
                                material = values[ks.index(ks[0])]
                                size = values[ks.index(ks[1])]
                                color = values[ks.index('Color')]
                            size_color_info[product_id] = {"size": size, "color": color, "material": material}
                        
                        elif len(values) == 4:
                            # Assuming the third element is material
                            print(values)
                            if ks[0] == 'Color':
                                # If it is, skip to the next iteration (go next)
                                color = values[ks.index('Color')]
                                material = None
                                size = values[ks.index(ks[3])] + ' | ' +values[ks.index(ks[1])] + " | "  +values[ks.index(ks[2])]
                            elif ks[1] == 'Color':
                                material = None
                                color = values[ks.index('Color')]
                                size = values[ks.index(ks[2])] +' | ' + values[ks.index(ks[0])] + " | "  +values[ks.index(ks[3])]
                            elif ks[2] == 'Color':
                                material = None
                                size = values[ks.index(ks[1])] + ' | ' + values[ks.index(ks[0])] + " | "  +values[ks.index(ks[3])]
                                color = values[ks.index('Color')]
                            size_color_info[product_id] = {"size": size, "color": color, "material": material}
                        
                        elif len(values) == 1:
                            size = values[0]
                            size_color_info[product_id] = {"size": size, "color": color, "meterial": meterial}
                        else:
                            len(values)
                        # print(size_color_info)
                        
                    
            


                    # Iterate through dimensionValuesDisplayData
                    for product_id, info in size_color_info.items():
                        # print(f"Product ID: {product_id}, Size: {info['size']}, Color: {info['color']}")
                        size = info['size'] if 'size' in info else None
                        color = info['color'] if 'color' in info else None
                        meterial = info['meterial'] if 'meterial' in info else None
                        # thread = threading.Thread(target=get_price_text, args=(x,kls,browser,page,  product_id,  size, color, meterial))

                        # # Start the thread
                        # thread.start()
                        # thread.join()
                        if "https://www.amazon.com/dp/" in x:
                            dp_index = x.find("/dp/") + 4  # Adding 4 to include the length of "dp/"

                            # Extract the part before and after "dp/"
                            before_dp = x[:dp_index]

                            # Replace the value after "dp/" with your custom value
                        else:
                            before_dp = "https://www.amazon.com/dp/"
                            
                        modified_url = f"{before_dp}{product_id}/?th=1&psc=1"

                        
                        print("Modified URL:", modified_url)
                        # await page.evaluate(f'window.location.href = "{modified_url}"')
                        await page.goto(modified_url)
                        html_content = await page.content()
                        # Use BeautifulSoup to parse the HTML content
                        soups = BeautifulSoup(html_content, 'html.parser')
                        
                        


                        main_image_element = soups.find(id= 'landingImage')

                        if main_image_element:
                            src_value = main_image_element.get('src').replace('._AC_UF894,1000_QL80_FMwebp_','').replace('._AC_US40_','').replace('._AC_US100_','').replace('._SX342_SY445_','').replace('._AC_SY300_SX300_','').replace('L.__AC_SX300_SY300_QL70_ML2_','').replace('._SS40_','').replace('._SX342_SY445_','').replace('._SX38_SY50_CR,0,0,38,50_','').replace('._SX300_SY300_QL70_ML2_','')
                            print(src_value)
                        else:
                            print("Element with id 'landingImage' not found.")
                            try:
                                main_image_elements = soups.find(id= 'imgTagWrapperId')
                                data_a_hires = main_image_elements.get('data-a-hires')
                                if main_image_elements:
                                    src_value = data_a_hires.get('src').replace('._AC_UF894,1000_QL80_FMwebp_','').replace('._AC_US40_','').replace('._AC_US100_','').replace('._SX342_SY445_','').replace('._AC_SY300_SX300_','').replace('L.__AC_SX300_SY300_QL70_ML2_','').replace('._SS40_','').replace('._SX342_SY445_','').replace('._SX38_SY50_CR,0,0,38,50_','').replace('._SX300_SY300_QL70_ML2_','')
                                    print(src_value)
                            except:
                                main_image_element = soup.find(id='unrolledImgNo0')
                                if main_image_element:
                                    # Extract the src attribute value from the img tag
                                    main_image_src = main_image_element.find('img')['src']
                                    if main_image_src:
                                        src_value = main_image_src.replace('._AC_UF894,1000_QL80_FMwebp_','').replace('._AC_US40_','').replace('._AC_US100_','').replace('._SX342_SY445_','').replace('._AC_SY300_SX300_','').replace('L.__AC_SX300_SY300_QL70_ML2_','').replace('._SS40_','').replace('._SX342_SY445_','').replace('._SX38_SY50_CR,0,0,38,50_','').replace('._SX300_SY300_QL70_ML2_','')
                                    print("Main image src:", main_image_src)
                                else:
                                    print("Main image element not found.")
                                # pass
                        
                        print("Price call")
                        try:
                            try:
                                target_div = soups.find(class_ = 'cardRoot bucket')
                            
                                # Extract the value associated with "displayString"
                                if target_div:
                                    components_data = target_div.get('data-components')
                                    if components_data:
                                        display_string = components_data.split('"displayString":"')[1].split('"')[0]
                                        print(display_string)
                                        price_text = display_string.replace('$','')
                                        if not price_text:
                                            raise ValueError
                                    if not components_data:
                                        raise ValueError
                                if not target_div:
                                    raise ValueError
                            except:
                                target_div = soups.find(id = 'corePrice_feature_div')
                            
                                # Extract the value associated with "displayString"
                                if target_div:
                                    components_data = target_div.find(class_='a-offscreen')
                                    if components_data:
                                        display_string = components_data.text.replace('$', '')
                                        if display_string.replace('.', '', 1).isdigit():
                                            print(display_string)
                                            price_text = float(display_string)
                                        if not price_text:
                                            raise ValueError
                                    if not components_data:
                                        raise ValueError
                                if not target_div:
                                    raise ValueError
                        except:
                            try:
                                price_elements = soup.find(class_='reinventPricePriceToPayMargin priceToPay')
                                if price_elements:
                                    price_element = price_elements.find(class_='a-offscreen')
                                    price_text = price_element.text.replace('$', '')
                                    if price_text.replace('.', '', 1).isdigit():
                                        # If the text represents a number, convert and print the number
                                        price_number = float(price_text)
                                        price_text = price_number
                                        print(f"Size: Quantity, Price: {price_number}")
                                if not price_elements:
                                    raise ValueError                
                            except:
                                price_elements = soup.find(id='tp_price_block_total_price_ww')
                                if price_elements:
                                    price_element = price_elements.find(class_='a-offscreen')
                                    price_text = price_element.text.replace('$', '')
                                    if price_text.replace('.', '', 1).isdigit():
                                        # If the text represents a number, convert and print the number
                                        price_number = float(price_text)
                                        price_text = price_number
                                        print(f"Size: Quantity, Price: {price_number}")
                        print(f"Product ID: {product_id}, Meterial: {meterial}, Size: {size}, Color: {color}, Price: {price_text}")
                        print(f"Product ID: {product_id}, Size: {meterial} | {size}, Color: {color}, Price: {price_text}")
                        # skusize.objects.create(product_id=kls, size=size, price= price_text)
                        await create_Sku_filter(kls, color, src_value)
                       

                        if meterial:
                            p = meterial + '|' + size
                        else:
                            p = size

                        await create_sku_size(kls, color,p, price_text)
                    
                    
                        if price == False:
                            price_element = soups.find(class_='a-offscreen')

                            if price_element:
                                price_text = price_element.text.replace('$', '')
                                
                                if price_text.replace('.', '', 1).isdigit():
                                    # If the text represents a number, convert and print the number
                                    price_number = float(price_text)
                                    p='Quantity'
                                    await create_sku_size(kls, color,p, price_number)
                                    print(f"Size: Quantity, Price: {price_number}")

                                else:
                                    # Find the script tag containing "dimensionValuesDisplayData"

                                    # If the text is not a number, print the text
                                    print("Text:", price_text)
                        
                        
                search_query.status = 'Completed'
                await sync_to_async(search_query.save)()
            
            if price == False:
                price_element = soup.find(class_='a-offscreen')
                p='Quantity'
                color=None
                if price_element:
                    price_text = price_element.text.replace('$', '')
                    
                    if price_text.replace('.', '', 1).isdigit():
                        # If the text represents a number, convert and print the number
                        price_number = float(price_text)
                        await create_sku_size(kls, color,p, price_number)
                        print(f"Size: Quantity, Price: {price_number}")

                    else:
                        # Find the script tag containing "dimensionValuesDisplayData"
                        price_elements = soup.find(class_='reinventPricePriceToPayMargin priceToPay')
                        if price_element:
                            price_element = price_elements.find(class_='a-offscreen')
                            price_text = price_element.text.replace('$', '')
                            if price_text.replace('.', '', 1).isdigit():
                                # If the text represents a number, convert and print the number
                                price_number = float(price_text)
                                await create_sku_size(kls, color,p, price_number)
                                print(f"Size: Quantity, Price: {price_number}")
                            else:
                                # If the text is not a number, print the text
                                print("Text:", price_text)
                                price_text = 'Stock Out'                    
                                await create_sku_size(kls, color,p, price_text)
                        else:
                            price_text = 'Stock Out'                    
                            await create_sku_size(kls, color,p, price_text)
                    search_query.status = 'Completed'
                    await sync_to_async(search_query.save)()
            # Continue with the rest of your code...
            descriptiom = soup.find(id='aplus_feature_div')
            if descriptiom:
                img_tags = descriptiom.find_all('img')
                for img in img_tags:
                    if 'gif' not in img.get('src'):
                        link_href = img.get('src').replace('._SS40_','')
                        # Process the image link as needed
                        print(f'Description Image: {link_href}')
                        await create_description(kls, link_href)

            review = soup.find(id='cm-cr-dp-review-list')
            reviewsl = review.find_all(attrs={'data-hook': 'review'})
            for i in reviewsl:
                customer_name = i.find(class_='a-profile-name').get_text()
                text_without_emoji = demoji.replace(customer_name, "")
                rating = i.find(class_='a-icon-alt').text
                rev_date = i.find(class_='review-date').text
                rev_text =  i.find(class_='reviewText').text
                text_without_emoji_rev = demoji.replace(rev_text, "")
                print(f'Customer Name: {text_without_emoji}, rating: {rating}, Review Date: {rev_date}, Review Text: {text_without_emoji_rev}')
                await  create_review(kls, text_without_emoji, rev_date, rating,text_without_emoji_rev )

            await browser.close()
    # Example: Creating Product object
    # Replace the following line with the appropriate logic for your project
    # Product.objects.create(name=title, link=x, product_no=search_query.query)

    # Return the response
    return { 'status': 'Success'}

