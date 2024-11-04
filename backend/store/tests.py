import threading
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
# from .forms import *

# required imports



import json

from urllib.parse import urlparse

import re
from django.http import request
import demoji




x = "https://www.amazon.com/dp/B0BSHH7RWK/"


def get_price_text(x, variant_id,  size, color, meterial):
    dp_index = x.find("/dp/") + 4  # Adding 4 to include the length of "dp/"

    # Extract the part before and after "dp/"
    before_dp = x[:dp_index]

    # Replace the value after "dp/" with your custom value

    modified_url = f"{before_dp}{variant_id}/?th=1&psc=1"

    
    print("Modified URL:", modified_url)
    try:
        response = requests.get(modified_url)
        response.raise_for_status()  # Raise an exception for bad responses
        html_content = response.text
    except requests.exceptions.RequestException as e:
        return {'url': url, 'status': str(e)}

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    


    main_image_element = soup.find(id= 'landingImage')

    if main_image_element:
        src_value = main_image_element.get('src').replace('._AC_UF894,1000_QL80_FMwebp_','')
        print(src_value)
    else:
        print("Element with id 'landingImage' not found.")

    
    print("Price call")
    try:
        target_div = soup.find(class_ = 'cardRoot bucket')
    
        # Extract the value associated with "displayString"
        if target_div:
            components_data = target_div.get('data-components')
            if components_data:
                display_string = components_data.split('"displayString":"')[1].split('"')[0]
                print(display_string)
                price_text = display_string
                if not price_text:
                    raise ValueError
            if not components_data:
                raise ValueError
        if not target_div:
            raise ValueError
    except:
        price_text = 'Stock Out'
    print(f"Product ID: {variant_id}, Meterial: {meterial}, Size: {size}, Color: {color}, Price: {price_text}")
    print(f"Product ID: {variant_id}, Size: {meterial} | {size}, Color: {color}, Price: {price_text}")
    # skusize.objects.create(product_id=kls, size=size, price= price_text)

    return 


 





def amazon_api(x, request):
    
    try:
        # Use requests to fetch the HTML content
        response = requests.get(x)
        response.raise_for_status()  # Raise an exception for bad responses
        html_content = response.text
    except requests.exceptions.RequestException as e:
        return {'url': x, 'status': str(e)}

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Continue with the rest of your code for scraping and processing
    product_data = dict()
    kkas =10001
    product_data['no'] = kkas
    kls = product_data['no']
    # Example: Extracting the title
    title_element = soup.find('h1') or soup.find(id='truncatedTitle')
    if title_element:
        titlel = title_element.text.replace("/", " ").replace("%", " ").replace(" \ ", " ").replace(" | ", " ")
        import re
        title = re.sub(r'\s+', ' ', titlel) 
    else:
        title = "Title not found"
    print(title)
    product_data['title'] = title
    seperator = '?'
    q = x
    l = q.split(seperator)[0]
    newurl = l
    # Product.objects.create(name=product_data['title'], link=newurl, product_no=product_data['no'])
    
    # SellerInfo.objects.create(product_id=kls,seller= 'Amazon.com',country='USA')
    
    # Example: Extracting images
    images = soup.find(id='lookbook_content_div') or soup.find(id='image-block') or soup.find(id='altImages')

    if images:
        img_tags = images.find_all('img')
        for img in img_tags:
            if 'gif' not in img.get('src'):
                link_href = img.get('src').replace('._SS40_','')
                # Process the image link as needed
                print(link_href)
                # ProductImage.objects.create(product_id=product_data['no'], image=link_href)
  
    # price_element = soup.find(class_='a-offscreen')

    # if price_element:
    #     price_text = price_element.text.replace('$', '')
        
    #     if price_text.replace('.', '', 1).isdigit():
    #         # If the text represents a number, convert and print the number
    #         price_number = float(price_text)
    #         print("Price:", price_number)
    #     else:
    #         # Find the script tag containing "dimensionValuesDisplayData"

    #         # If the text is not a number, print the text
    #         print("Text:", price_text)
    script_tags = soup.find_all('script')
    price = False
    for script in script_tags:
        script_content = script.get_text()
        if 'twister-js-init-dpx-data' in script_content:
            price = True
            productData_start = script_content.find('"dimensionValuesDisplayData" : {') 
            productData_end = script_content.find('};', productData_start)
            product_datas = '{' + script_content[productData_start:productData_end].strip() + '}' 
            print(product_datas)
        
            try:
                product_data = json.loads(product_datas)
            except json.decoder.JSONDecodeError as e:
                print("JSON Decode Error:", e)
            size_color_info = {}
            try:
                ks = []
                for keys in product_data["dimensionsDisplay"]:
                    print(keys)
                    ks.append(keys)
                
                
                for product_id, values in product_data["dimensionValuesDisplayData"].items():
                    print(len(values))
                    if len(values) == 2:
                        meterial = ''
                        color = values[ks.index('color')]
                        if ks[0] == 'color':
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
                    elif len(values) == 1:
                        meterial = ''
                        color = ''
                        size = values[0]
                        size_color_info[product_id] = {"size": size, "color": color, "meterial": meterial}
                    else:
                        len(values)
                    size_color_info[product_id] = {"size": size, "color": color, "material": material}
                    print(size_color_info)
                    
                            
                        
            except:
                ks = []
                ps = []
                for keys, values in product_data["variationDisplayLabels"].items():
                    print(keys)
                    ks.append(keys)
                    ps.append(keys)
                
                
                for product_id, values in product_data["dimensionValuesDisplayData"].items():
                    print(len(values))
                    if len(values) == 2:
                        meterial = ''
                        color = values[ks.index('color_name')]
                        if ks[0] == 'color_name':
                            # If it is, skip to the next iteration (go next)
                            size = values[ks.index(ks[1])]
                        else:
                            size = values[ks.index(ks[0])]

                        size_color_info[product_id] = {"size": size, "color": color, "material": meterial}
                    
                    elif len(values) == 3:
                        # Assuming the third element is material
                    
                        if ks[0] == 'color_name':
                            # If it is, skip to the next iteration (go next)
                            color = values[ks.index('color_name')]
                            material = values[ks.index(ks[1])]
                            size = values[ks.index(ks[2])]
                        elif ks[1] == 'color_name':
                            material = values[ks.index(ks[0])]
                            color = values[ks.index('color_name')]
                            size = values[ks.index(ks[2])]
                        elif ks[2] == 'color_name':
                            material = values[ks.index(ks[0])]
                            size = values[ks.index(ks[1])]
                    elif len(values) == 1:
                        meterial = ''
                        color = ''
                        size = values[0]
                        size_color_info[product_id] = {"size": size, "color": color, "meterial": meterial}
                    else:
                        len(values)
                    size_color_info[product_id] = {"size": size, "color": color, "material": material}
                    print(size_color_info)
                    

                
                    # meterial = ''
                    # color = ''
                    # size = values[0]
                    # size_color_info[product_id] = {"size": size, "color": color, "meterial": meterial}

            
            # navigate to the URL
            

            # Iterate through dimensionValuesDisplayData
            for product_id, info in size_color_info.items():
                # print(f"Product ID: {product_id}, Size: {info['size']}, Color: {info['color']}")
                size = info['size']
                color = info['color']
                meterial = info['material']
                thread = threading.Thread(target=get_price_text, args=(x, product_id,  size, color, meterial))

                # Start the thread
                thread.start()
                # thread.join()
    if price == False:
        price_element = soup.find(class_='a-offscreen')

        if price_element:
            price_text = price_element.text.replace('$', '')
            
            if price_text.replace('.', '', 1).isdigit():
                # If the text represents a number, convert and print the number
                price_number = float(price_text)
                print(f"Size: Quantity, Price: {price_number}")

            else:
                # Find the script tag containing "dimensionValuesDisplayData"

                # If the text is not a number, print the text
                print("Text:", price_text)
    # else:
    #     print("Price element not found.")

        # skusize.objects.create(product_id=product_data['no'], size="Stock Out", price= "")

    # Return the response
    return { 'status': 'Success'}



amazon_api(x, request)


