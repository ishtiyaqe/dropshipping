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
from store.models import *
from order.models import *
from accounts.models import *
from snipet.models import *
import uuid
from store.forms import *
from order.forms import *
import json
import chromedriver_binary
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import generics
from store.serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.core.serializers import serialize
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models  import *
from accounts.models  import *
from accounts.views  import *
from order.models  import *
from order.views  import *
from store.models  import *
import requests
import string
import nltk, json
import facebook
nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')
from nltk.tokenize import word_tokenize; from nltk.corpus import wordnet; from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker; spell = SpellChecker(); lemmatizer = WordNetLemmatizer()
from django.core.exceptions import ObjectDoesNotExist

import requests

import random
import time
import facebook


def get_wordnet_pos(word): return {'J': wordnet.ADJ, 'N': wordnet.NOUN, 'V': wordnet.VERB, 'R': wordnet.ADV}.get(nltk.pos_tag([word])[0][1][0].upper(), wordnet.NOUN)
def spell_check(text):
    corrected_words = []
    for word in word_tokenize(text):
        corrected_word = spell.correction(word)
        if corrected_word is not None:
            pos = get_wordnet_pos(word) or wordnet.NOUN
            corrected_words.append(lemmatizer.lemmatize(corrected_word, pos=pos))
    return ' '.join(corrected_words)

ADMIN_PAGE_ID = '106665319043371'
VERIFY_TOKEN = 'EAABZCL2kI5vIBAJQ7dyFn9X5PpMywnIuHedcf31RJZChDJnjZCzmzIx7EeWu7CvZCzhRCRjWBs25uSEn3pOrMcZBER77dtj2k4VbSwEDsXDgGM4kFWod8aZApgQw3FZCPmnAD8Tno0UTxMCGWwrsY7MgerYRMEMnyb3IxppLo1pNyd98gPMbHzA'
PAGE_ACCESS_TOKEN = 'EAABZCL2kI5vIBAJQ7dyFn9X5PpMywnIuHedcf31RJZChDJnjZCzmzIx7EeWu7CvZCzhRCRjWBs25uSEn3pOrMcZBER77dtj2k4VbSwEDsXDgGM4kFWod8aZApgQw3FZCPmnAD8Tno0UTxMCGWwrsY7MgerYRMEMnyb3IxppLo1pNyd98gPMbHzA'

API_URL = 'https://graph.facebook.com/me/conversations?fields=messages{message,from,to}&access_token=' + VERIFY_TOKEN


alibaba_patterns = [
    r'https?://www\.alibaba\.com/product-detail/[\w-]+\.html',
    r'https?://m\.alibaba\.com/product/[\w-]+\.html',
    r'https?://cn\.alibaba\.com/product/[\w-]+\.html',
    r'https?://wholesaler\.alibaba\.com/product-detail/[\w-]+\.html',
    r'https?://supplier\.alibaba\.com/product-detail/[\w-]+\.html',
    r'https?://best\.alibaba\.com/product/[\w-]+\.html',
    r'https?://app\.alibaba\.com/dynamiclink\?[\w-]+',
    r'https?://global\.alibaba\.com/products/[\w-]+\.html',
]

def extract_product_links(message_text):
    """
    Extracts Alibaba product links from a message.
    Returns a list of product links found in the message.
    """
    product_links = []
    for pattern in alibaba_patterns:
        matches = re.findall(pattern, message_text)
        if matches:
            product_links.extend(matches)

    output = ', '.join(product_links)
    print(output)
    return output

def handle_message(messaging_event):
    sender_id = messaging_event['sender']['id']
    message_data = messaging_event['message']
    if 'text' in message_data:
        message_text = message_data['text']
        corrected_text = spell_check(message_text)
        validate = URLValidator()
        
        if message_text == 'আমাদের সার্ভিস':
            user_data = get_user_data(sender_id)
            first_name = user_data['first_name']
            send_message(sender_id, f'Hi {first_name}, thank you for choosing our service.')
            # send_website_link(sender_id)

        elif message_text.startswith(('https://m.alibaba.com/product/' )):
            Product_information(messaging_event, message_text, sender_id)
        
            
        elif message_text.startswith(('https://' )):
            albaba = extract_product_links(message_text)
            print(albaba)
            if albaba:
                print('hi')
                Product_information(messaging_event, message_text, sender_id)
            else:
                send_message(sender_id, 'Not have APi')
        
            
        elif message_text == 'Order status':
            handle_order(messaging_event)
        
        elif message_text == 'Shop For Me Status':
            handle_req_order(messaging_event)
        
        elif message_text == 'Ship For Me Status':
            handle_SFM_order(messaging_event)
        
        elif message_text == 'Pay For Me Status':
            handle_PFM_order(messaging_event)
        
        elif message_text == 'Product information':
            send_message(sender_id, 'আমাকে প্রোডাক্টের লিংকটি দিন। \nউদাহরনঃ https://www.alibaba.com/product/Babyr_dress......')
        
        elif message_text.startswith(('https://ecargo.com.bd/' )):
            print('witt')

        # Single order number query
        elif message_text.startswith(('10000')):
            Order_Id(messaging_event, message_text, sender_id)
            
         # Single Shopping number query
        elif message_text.startswith(('9000000')):
            shopping_Id(messaging_event, message_text, sender_id)
        
        # Single Shipping number query
        elif message_text.startswith(('4000000')):
            shipping_Id(messaging_event, message_text, sender_id)
        
        # Single Payment number query
        elif message_text.startswith(('5000000')):
            payment_Id(messaging_event, message_text, sender_id)
            
        # check only phone in message
        elif message_text.startswith(('01')) and len(message_text) == 11:
            get_messages(sender_id, message_text)

        # Check only OTP in message
        elif message_text.isdigit() and len(message_text) == 4:
            check_OTP_only(messaging_event)
        
        # chekking in question dynamic models
        else:
            # check have in normal  text message
            query_result = AutoMessageQuestion.objects.filter(question__icontains=message_text).first()
            if not query_result:
                # Create a translation table to remove all punctuation and special characters
                translator = str.maketrans('', '', string.punctuation)

                # Remove all punctuation and special characters from the string
                cleaned_text = message_text.translate(translator)

                # Search for a matching question in the automessages database based on the cleaned text
                query_result = AutoMessageQuestion.objects.filter(question__icontains=cleaned_text).first()

            if query_result:
                response_text = query_result.q_id.answer
                send_message(sender_id, response_text)
                
            # check have in link button
            if not query_result:
                query_result = AutoLinkMessageQuestion.objects.filter(question__icontains=message_text).first()
                if not query_result:
                    # Create a translation table to remove all punctuation and special characters
                    translator = str.maketrans('', '', string.punctuation)

                    # Remove all punctuation and special characters from the string
                    cleaned_text = message_text.translate(translator)

                    # Search for a matching question in the automessages database based on the cleaned text
                    query_result = AutoLinkMessageQuestion.objects.filter(question__icontains=cleaned_text).first()
                if query_result:
                    api_url = 'https://graph.facebook.com/v16.0/103683522715299/messages'
                    print(query_result)
                    message_data = {
                        'recipient': {'id': sender_id},
                        'message': {
                            'attachment': {
                                'type': 'template',
                                'payload': {
                                    'template_type': 'generic',
                                    'elements': [{
                                        'title': query_result.q_id.title,
                                        'image_url': f'https://ecargo.com.bd/{query_result.q_id.imegs}',
                                        'subtitle': query_result.q_id.subtitle,
                                        'default_action': {
                                            'type': 'web_url',
                                            'url': query_result.q_id.link,
                                            'messenger_extensions': False,
                                            'webview_height_ratio': 'TALL'
                                        },
                                        'buttons': [
                                            {
                                                'type': 'web_url',
                                                'url': query_result.q_id.button_link,
                                                'title': query_result.q_id.button_name
                                            }
                                        ]
                                    }]
                                }
                            }
                        }
                    }
                    # Send the message data to the API URL
                    response = requests.post(api_url,params={'access_token': VERIFY_TOKEN}, json=message_data)
                    print(response.text)


            # check have in button message
            if not query_result:
                query_result = ButtonLinkMessageQuestion.objects.filter(question__icontains=message_text).first()
                if not query_result:
                    # Create a translation table to remove all punctuation and special characters
                    translator = str.maketrans('', '', string.punctuation)

                    # Remove all punctuation and special characters from the string
                    cleaned_text = message_text.translate(translator)

                    # Search for a matching question in the automessages database based on the cleaned text
                    query_result = ButtonLinkMessageQuestion.objects.filter(question__icontains=cleaned_text).first()
                if query_result:
                    api_url = 'https://graph.facebook.com/v16.0/103683522715299/messages'
                    print(query_result)
                    multi = AdditionalBtnLink.objects.filter(q_id=query_result.q_id)
                    if multi:
                        buttons = [
                            {
                                "type": "web_url",
                                "url": i.button_link,
                                "title": i.button_name
                            } for i in multi
                        ]
                    else:
                        buttons = []
                        
                    message_data = {
                        'recipient': {'id': sender_id},
                        "message": {
                            "attachment": {
                                "type": "template",
                                "payload": {
                                    "template_type": "button",
                                    "text": query_result.q_id.text,
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": query_result.q_id.button_link,
                                            "title": query_result.q_id.button_name
                                        }
                                    ] + buttons
                                }
                            }
                        }
                    }

                    # Send the message data to the API URL
                    response = requests.post(api_url,params={'access_token': VERIFY_TOKEN}, json=message_data)
                    print(response.text)

            if not query_result:
                response_text = "Sorry, I didn't understand that. How can I assist you today?"

                send_message(sender_id, response_text)
    else:
        response_text = "Sorry, I can only handle text messages at the moment."
        send_message(sender_id, response_text)

        return


# for single payment id query
def payment_Id(messaging_event, message_text, sender_id):
    user_data = check_user(messaging_event)
    if user_data is None:
        sender_id = messaging_event['sender']['id']
        response_text = "যে নাম্বারটি দিয়ে আপনি ওর্ডার প্লেস করেছেন আমাকে সে নাম্বারটা দিন। \n Ex:01XXXXXX"
        send_message(sender_id, response_text)
        # print("i2")
    elif user_data[0] == "Valid":
        phone = user_data[1]
        payments_id = payforme.objects.filter(phone=phone)
        num = None
        for order in payments_id:
            if int(message_text) == order.payment_id:
                num = message_text 
        if num is None:
            send_message(sender_id, 'This is not your Order Id. Please provide a correct Phone number or order number.')
        else:
            # print(f"11-digit number: {phone}")
            # print(Shipping_id)
            status_dict = {}
            for order in payments_id:
                if order.payment_id == int(num):
                    status_dict = order.status
            # send_message(sender_id, f'Order Id:  {num}. \nStatus: {status_dict}')
            api_url = 'https://graph.facebook.com/v16.0/103683522715299/messages'

            message_data = {
                'recipient': {'id': sender_id},
                "message":{
                    "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text":f'Payment Id:  {num}. \nStatus: {status_dict}',
                        "buttons":[
                        {
                            "type":"web_url",
                            "url":"https://ecargo.com.bd",
                            "title":"Visit Site"
                        },]
                        }
                    }
                }
            }
            # Send the message data to the API URL
            response = requests.post(api_url,params={'access_token': VERIFY_TOKEN}, json=message_data)
            print(response.text)


# for single Shipping id query
def shipping_Id(messaging_event, message_text, sender_id):
    user_data = check_user(messaging_event)
    if user_data is None:
        sender_id = messaging_event['sender']['id']
        response_text = "যে নাম্বারটি দিয়ে আপনি ওর্ডার প্লেস করেছেন আমাকে সে নাম্বারটা দিন। \n Ex:01XXXXXX"
        send_message(sender_id, response_text)
        # print("i2")
    elif user_data[0] == "Valid":
        phone = user_data[1]
        Shipping_id = Shipping.objects.filter(phone=phone)
        num = None
        for order in Shipping_id:
            if int(message_text) == order.shipping_id:
                num = message_text 
        if num is None:
            send_message(sender_id, 'This is not your Order Id. Please provide a correct Phone number or order number.')
        else:
            # print(f"11-digit number: {phone}")
            # print(Shipping_id)
            status_dict = {}
            for order in Shipping_id:
                if order.shipping_id == int(num):
                    status_dict = order.status
            # send_message(sender_id, f'Order Id:  {num}. \nStatus: {status_dict}')
            api_url = 'https://graph.facebook.com/v16.0/103683522715299/messages'

            message_data = {
                'recipient': {'id': sender_id},
                "message":{
                    "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text":f'Shipping Id:  {num}. \nStatus: {status_dict}',
                        "buttons":[
                        {
                            "type":"web_url",
                            "url":"https://ecargo.com.bd",
                            "title":"Visit Site"
                        },]
                        }
                    }
                }
            }
            # Send the message data to the API URL
            response = requests.post(api_url,params={'access_token': VERIFY_TOKEN}, json=message_data)
            print(response.text)

# for single Request order id query
def shopping_Id(messaging_event, message_text, sender_id):
    user_data = check_user(messaging_event)
    if user_data is None:
        sender_id = messaging_event['sender']['id']
        response_text = "যে নাম্বারটি দিয়ে আপনি ওর্ডার প্লেস করেছেন আমাকে সে নাম্বারটা দিন। \n Ex:01XXXXXX"
        send_message(sender_id, response_text)
        # print("i2")
    elif user_data[0] == "Valid":
        phone = user_data[1]
        Shopping = req.objects.filter(customer__mobile=phone)
        num = None
        for order in Shopping:
            if int(message_text) == order.order_id:
                num = message_text 
        if num is None:
            send_message(sender_id, 'This is not your Order Id. Please provide a correct Phone number or order number.')
        else:
            # print(f"11-digit number: {phone}")
            # print(Shopping)
            status_dict = {}
            for order in Shopping:
                if order.order_id == int(num):
                    status_dict = order.status
            # send_message(sender_id, f'Order Id:  {num}. \nStatus: {status_dict}')
            api_url = 'https://graph.facebook.com/v16.0/103683522715299/messages'

            message_data = {
                'recipient': {'id': sender_id},
                "message":{
                    "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text":f'Shopping Id:  {num}. \nStatus: {status_dict}',
                        "buttons":[
                        {
                            "type":"web_url",
                            "url":"https://ecargo.com.bd",
                            "title":"Visit Site"
                        },]
                        }
                    }
                }
            }
            # Send the message data to the API URL
            response = requests.post(api_url,params={'access_token': VERIFY_TOKEN}, json=message_data)
            print(response.text)


# for single order id query
def Order_Id(messaging_event, message_text, sender_id):
    user_data = check_user(messaging_event)
    if user_data is None:
        sender_id = messaging_event['sender']['id']
        response_text = "যে নাম্বারটি দিয়ে আপনি ওর্ডার প্লেস করেছেন আমাকে সে নাম্বারটা দিন। \n Ex:01XXXXXX"
        send_message(sender_id, response_text)
        # print("i2")
    elif user_data[0] == "Valid":
        phone = user_data[1]
        orders = OrerPrduct.objects.filter(orderi__phone=phone)
        num = None
        for order in orders:
            if int(message_text) == order.OrderP_id:
                num = message_text 
        if num is None:
            send_message(sender_id, 'This is not your Order Id. Please provide a correct Phone number or order number.')
        else:
            # print(f"11-digit number: {phone}")
            # print(orders)
            status_dict = {}
            for order in orders:
                if order.OrderP_id == int(num):
                    status_dict = order.status
            # send_message(sender_id, f'Order Id:  {num}. \nStatus: {status_dict}')
            api_url = 'https://graph.facebook.com/v16.0/103683522715299/messages'

            message_data = {
                'recipient': {'id': sender_id},
                "message":{
                    "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text":f'Order Id:  {num}. \nStatus: {status_dict}',
                        "buttons":[
                        {
                            "type":"web_url",
                            "url":"https://ecargo.com.bd",
                            "title":"Visit Site"
                        },]
                        }
                    }
                }
            }
            # Send the message data to the API URL
            response = requests.post(api_url,params={'access_token': VERIFY_TOKEN}, json=message_data)
            print(response.text)


# for products data throw link
def Product_information(messaging_event, message_text, sender_id):
    try:
        product_data = None
        webPage = requests.get(message_text)
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
            q = message_text
            l = q.split(seperator)[0]
            newurl = l

        try:

            products = Product.objects.get(link__icontains=newurl)
            prices = ProductPrice.objects.filter(product_id=products.product_no)
            image_data = ProductImage.objects.filter(product_id=products.product_no)
            print(products)
            for j in prices:
                price = j.price
                if  j.m1 == None:
                    m1 = 1
                    print(j.m1)
                else:
                    m1=j.m1
                    print(m1)
                    break
            for i in image_data:
                imegs = i.image
            print(price)
            print(imegs)  
            api_url = 'https://graph.facebook.com/v16.0/103683522715299/messages'

            message_data = {
                'recipient': {'id': sender_id},
                'message': {
                    'attachment': {
                        'type': 'template',
                        'payload': {
                            'template_type': 'generic',
                            'elements': [{
                                'title': products.name[:40],
                                'image_url': imegs,
                                'subtitle': f'Price {price} \nMOQ : {m1}',
                                'default_action': {
                                    'type': 'web_url',
                                    'url': products.link,
                                    'messenger_extensions': False,
                                    'webview_height_ratio': 'TALL'
                                },
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': f'https://ecargo.com.bd/product/{products.name}/{products.product_no}/{products.id}',
                                        'title': 'Visit Now'
                                    }
                                ]
                            }]
                        }
                    }
                }
            }
            # Send the message data to the API URL
            response = requests.post(api_url,params={'access_token': VERIFY_TOKEN}, json=message_data)
            print(response.text)

            if not products:
                print("start job!!")
                

                raise ValueError

        except: 
            print('start ne job')
            for product_data in newurl:
                product_data = dict()
                


                # set chrome options
                chrome_options = Options()
                chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--log-level=3")
                chrome_options.add_argument("--mute-audio")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument('--disable-extensions')
                chrome_options.add_argument('--disable-gpu')

                # set desired capabilities
                capabilities = DesiredCapabilities.CHROME.copy()
                capabilities["pageLoadStrategy"] = "none"

                # create webdriver instance
                driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
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

                try:
                    ss = driver.find_element(By.CLASS_NAME,'view-more')
                    ss.click()
                    kk = driver.find_element(By.CLASS_NAME,'view-more')
                    kk.click()
                    ll = driver.find_element(By.CLASS_NAME,'view-more')
                    ll.click() 

                except:
                    pass

                kkas = uuid.uuid4().hex[:5].upper()
                product_data['no'] = kkas
                s = driver.find_element(By.XPATH, "//h1").text.replace("/"," ").replace("%"," ")
                product_data['title'] = s
                Product.objects.create(name=product_data['title'], link=newurl, product_no=product_data['no'])
        

                
                try:
                    cat = driver.find_element(By.XPATH, '//nav/ul/li[3]/a').text
                    Catagorys.objects.create(product_id=product_data['no'], catagory=cat)
                except:
                    pass
                #total Buyer
            
            
                try:
                    try:
                        s = soup.find('script', type='application/ld+json')
                        dt = json.loads(s.string)
                        AlibabaProdduct_Id=dt['@id']
                    except:
                        s = soup.find('script', type='application/ld+json')
                        dt = json.loads(s.string)

                        for entry in dt:
                            x = entry
                            AlibabaProdduct_Id=x['@id']
                    l = "https://www.alibaba.com/event/app/productExportOrderQuery/transactionOverview.htm?detailId="+AlibabaProdduct_Id
                    res = requests.get(l.format(1), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'})
                    k11 = BeautifulSoup(res.text, 'lxml')
                    kl =json.loads(k11.string)
                    kk=kl['data']
                    aaa=kk['totalBuyers']
                    total_buyer = str(aaa)

                    #seller info & country 
                    try:
                        sa = driver.find_element(By.CLASS_NAME, "company-card")
                        sas = sa.get_attribute("outerHTML")
                        sas11 = BeautifulSoup(sas, 'html.parser')
                        items = [item.get_text(strip=True) for item in sas11.find_all(class_="company-item")]
                        items.pop()
                        couun = sas11.find_all(class_="company-item")
                        country = couun
                        del country[:1]
                        del country[:1]
                        countryn = ''.join(str(item) for item in country)
                        ka = BeautifulSoup(countryn, 'html.parser')
                        con = ka.find(class_="company-country").text
                        year = ka.find(class_="company-year").text
                        print(year)
                        print(con)
                        SellerInfo.objects.create(product_id=product_data['no'],seller= items[0], country=con, brand=items[1], year=year,totalbuyer=total_buyer)
                    except:
                        sa = driver.find_element(By.CLASS_NAME, "widget-supplier-card")
                        sas = sa.get_attribute("outerHTML")
                        sas11 = BeautifulSoup(sas, 'html.parser')
                        items = sas11.find(class_="company-name-container").text
                        brands = sas11.find(class_="company-brand").text
                        country = sas11.find(class_="register-country").text
                        year = sas11.find(class_="join-year").text
                        print(country)
                        print(year)
                        SellerInfo.objects.create(product_id=product_data['no'],seller= items,country=country, brand=brands, year=year,totalbuyer=total_buyer)


                    
                except:
                    #seller info & country 
                    try:
                        sa = driver.find_element(By.CLASS_NAME, "company-card")
                        sas = sa.get_attribute("outerHTML")
                        sas11 = BeautifulSoup(sas, 'html.parser')
                        items = [item.get_text(strip=True) for item in sas11.find_all(class_="company-item")]
                        items.pop()
                        couun = sas11.find_all(class_="company-item")
                        country = couun
                        del country[:1]
                        del country[:1]
                        countryn = ''.join(str(item) for item in country)
                        ka = BeautifulSoup(countryn, 'html.parser')
                        con = ka.find(class_="company-country").text
                        year = ka.find(class_="company-year").text
                        
                        SellerInfo.objects.create(product_id=product_data['no'],seller= items[0], country=con, brand=items[1], year=year)
                    except:
                        sa = driver.find_element(By.CLASS_NAME, "widget-supplier-card")
                        sas = sa.get_attribute("outerHTML")
                        sas11 = BeautifulSoup(sas, 'html.parser')
                        items = sas11.find(class_="company-name-container").text
                        brands = sas11.find(class_="company-brand").text
                        country = sas11.find(class_="register-country").text
                        year = sas11.find(class_="join-year").text
                        
                        SellerInfo.objects.create(product_id=product_data['no'],seller= items,country=country, brand=brands, year=year)
                    
                # image
                try:
                    ims = driver.find_element(By.CLASS_NAME, 'main-list')
                except NoSuchElementException:
                    ims = driver.find_element(By.CLASS_NAME, 'thumb-list')

                import re  
                kobai = BeautifulSoup(ims.get_attribute("outerHTML"), 'html.parser')
                images = kobai.select('div.main-list img, div.thumb-list img, div.detail-next-slick-track img')

                new_lists = []
                for image in images:
                    src = image['src']
                    new_src = re.sub(r'(_\d+x\d+)?\.(jpg|png|jpeg)_[^.]*', r'\1', src)
                    new_lists.append(new_src)
                pattern = r'\.svg$'
                for data in new_lists[1:]:
                    if not re.search(pattern, data):
                        ProductImage.objects.create(product_id=product_data['no'], image=data)

                
                price = driver.find_element(By.CLASS_NAME, "product-price")
                price_code = price.get_attribute("outerHTML")
                kobai = BeautifulSoup(price_code, 'html.parser')


                # Pc froduct price
                try:
                    try:

                        items = kobai.findAll('div', attrs={'class': 'price-item'})
                        for item in items:
                            moq = item.find('div', attrs={'class': 'quality'}).text
                            m = moq.replace("boxes", "").replace("rolls", "").replace("units", "").replace("bag/bags", "").replace("square meters", "").replace("pairs", "").replace("piece/pieces", "").replace("sets", "").replace("pieces", "").replace("quarts", "").replace("-", "").replace("pair/pairs", "").replace("roll/rolls", "") .replace("unit/units", "")
                            mj, n = [i for i in m.split()]
                            xd = item.find('div', attrs={'class': 'price'}).text.replace('$', ' ')
                            s, r = [Decimal(i) for i in xd.split()]
                            x = s * 130
                            y = r * 130
                            saleprice = str(round(float(x)))
                            regularprice = str(round(float(y)))
                            ProductPrice.objects.create(product_id=product_data['no'], price=saleprice,saleprice=regularprice, m1 = mj,  m2 = n)
                            if not item:
                                raise ValueError
                            

                            

                    except ValueError:
                        items = kobai.find_all('div', attrs={'class': 'price-item'})
                        for item in items:
                            moq = item.find('div', attrs={'class': 'quality'}).text
                            m = moq.replace("boxes", "").replace("rolls", "").replace("sets", "").replace("bag/bags", "").replace("pairs", "").replace("square meters", "").replace("piece/pieces", "").replace("pieces", "").replace("quarts", "").replace("-", "").replace("unit/units", "").replace("pair/pairs", "").replace("roll/rolls", "") 
                            mj, n = [i  for i in m.split()]
                            xd = item.find('div', attrs={'class': 'price'}).text.replace('$', ' ')
                            x = Decimal(xd)  * 130
                            price = str(round(float(x)))
                            ProductPrice.objects.create(product_id=product_data['no'], price=price, m1 = mj, m2 = n)
                            


                    except:
                        for item in kobai:
                            moq = item.find('span', attrs={'class': 'moq'}).text
                            m = moq.replace("boxes", "").replace("rolls", "").replace("piece/", "").replace("bag/bags", "").replace("pairs", "").replace("square meters", "").replace("piece/pieces", "").replace("pieces", "").replace("pair/pairs", "").replace("unit/units", "").replace("sets", "").replace("-", "").replace("roll/rolls", "") .replace(">=", "").replace("sets/", "").replace("sets/Sets", "")
                            mj, n = [i for i in m.split()]
                            xd = item.find('span', attrs={'class': 'price'}).text.replace('$', ' ').replace('-', ' ')
                            a, b = [Decimal(i) for i in xd.split()]
                            x = a * 130
                            y = b * 130
                            proprice = str(round(float(x)))
                            price = str(round(float(y)))
                            ProductPrice.objects.create(product_id=product_data['no'], price=price,proprice=(price + "-" + proprice), m1 = mj, m2 = n)
                    else:
                        for item in kobai:
                            moq = item.find('span', attrs={'class': 'moq'}).text
                            m = moq.replace("boxes", "").replace("rolls", "").replace("piece/", "").replace("bag/bags", "").replace("pairs", "").replace("square meters", "").replace("piece/pieces", "").replace("pieces", "").replace("quarts", "").replace("sets", "").replace("-", "").replace("unit/units", "").replace("roll/rolls", "") .replace("set/", "").replace("sets/Sets", "").replace("pair/pairs", "")
                            xd = item.find('span', attrs={'class': 'price'}).text.replace('$', ' ').replace('-', ' ')
                            a, b = [Decimal(i) for i in xd.split()]
                            x = a * 130
                            y = b * 130
                            proprice = str(round(float(x)))
                            price = str(round(float(y)))
                            ProductPrice.objects.create(product_id=product_data['no'], price=price,proprice=(price + "-" + proprice),  m2 = m)
                    
                    # external single product price
                except:
                    try:
                        try:
                            for item in kobai:
                                moq = item.find('span', attrs={'class': 'moq'}).text
                                ks = item.find('span', attrs={'class': 'price'}).text
                                ls = ks.replace('$', '').replace("boxes", "").replace("bag/bags", "").replace("pairs", "").replace('-', '').replace(',', '') 
                                m = moq.replace("piece/", "").replace("rolls", "").replace("square meters", "").replace("piece/pieces", "").replace("pieces", "").replace("quarts", "").replace('set/sets', '') .replace("sets", "").replace("sets/", "").replace("sets/Sets", "").replace("-", "")
                                a, b = [d for d in m.split()]  
                        
                                x, ys = [d for d in ls.split()]  
                                l = Decimal(ys)
                                ya = l * 130
                                klsa = str(round(float(ya)))
                                ProductPrice.objects.create(product_id=product_data['no'], price=klsa,m1=a,m2=b)
                        
                        except:
                            for item in kobai:
                                moq = item.find('span', attrs={'class': 'moq'}).text
                                ks = item.find('span', attrs={'class': 'price'}).text
                                ls = ks.replace('$', '').replace("rolls", "").replace("boxes", "").replace("bag/bags", "").replace("pairs", "").replace('-', '').replace(',', '') 
                                m = moq.replace("piece/", "").replace("square meters", "").replace("piece/pieces", "").replace("pieces", "").replace("quarts", "").replace('set/sets', '') .replace("sets", "").replace("sets/", "").replace("sets/Sets", "").replace("-", "")
                
                                x, ys = [d for d in ls.split()]  
                                l = Decimal(ys)
                                ya = l * 130
                                klsa = str(round(float(ya)))
                                ProductPrice.objects.create(product_id=product_data['no'], price=klsa,m2=m)
                        else:
                            
                                
                                
                            for item in kobai:
                                moq = item.find('span', attrs={'class': 'promotion-moq'}).text
                                m = moq.replace("boxes", "").replace("rolls", "").replace("piece/", "").replace("bag/bags", "").replace("pairs", "").replace("piece/pieces", "").replace("square meters", "").replace("pieces", "").replace("quarts", "").replace("sets", "").replace("sets/", "").replace("sets/Sets", "").replace("unit/units", "").replace("roll/rolls", "") .replace("-", "").replace(">=", "").replace("pair/pairs", "")
                                
                                xd = item.find('strong', attrs={'class': 'normal'}).text.replace('$', '').replace('-', '').replace(',', '')
                                a = Decimal(xd)
                                x = a * 130
                                proprice = str(round(float(x)))
                                ProductPrice.objects.create(product_id=product_data['no'], price=proprice,m2=m)
                    except:
                        try:
                            items = kobai.findAll('div', attrs={'class': 'price-item'})
                            for item in items:
                                moq = item.find('div', attrs={'class': 'quality'}).text
                                m = moq.replace("boxes", "").replace("rolls", "").replace("units", "").replace("bag/bags", "").replace("square meters", "").replace("pairs", "").replace("piece/pieces", "").replace("sets", "").replace("pieces", "").replace("quarts", "").replace("-", "").replace("pair/pairs", "").replace("roll/rolls", "") .replace("unit/units", "")
                                mj, n = [i for i in m.split()]
                                xd = item.find('div', attrs={'class': 'price'}).text.replace('$', ' ').replace(',', '')
                                y = Decimal(xd) * 130
                                regularprice = str(round(float(y)))
                                ProductPrice.objects.create(product_id=product_data['no'], price=regularprice,m1=mj,m2=n)
                        except:
                            pass
                            
                try:
                    try:

                        items = kobai.findAll('div', attrs={'class': 'price-item'})
                        for item in items:
                            
                            moq = item.find('div', attrs={'class': 'quality'}).text
                            m = moq.replace("pieces", "").replace("rolls", "").replace("boxes", "").replace("pairs", "").replace("units", "").replace("sets", "").replace("piece/pieces", "").replace("-", "").replace("quarts", "")
                            mj, n, *others = [i for i in m.split()]
                            if len(others) >= 1:
                                mj, n, *_ = [i for i in m.split()]
                            xd = item.find('div', attrs={'class': 'price'}).text.replace('$', ' ')
                            s, r = [Decimal(i) for i in xd.split()]
                            x = s * 130
                            y = r * 130
                            saleprice = str(round(float(x)))
                            regularprice = str(round(float(y)))
                            ProductPrice.objects.create(product_id=product_data['no'], price=saleprice,saleprice=regularprice, m1 = mj,  m2 = n)
                            print("Sale Price1: " +saleprice + " Price: " + regularprice,"moq: " + mj + '-'+n)
                            if not saleprice:
                                print("value error 1")
                                raise ValueError


                    except ValueError:
                    
                        items = kobai.findAll('div', attrs={'class': 'price-item'})
                        for item in items:
                            moq = item.find('div', attrs={'class': 'quality'}).text
                            m = moq.replace("pieces", "").replace("rolls", "").replace("boxes", "").replace("pairs", "").replace("units", "").replace("sets", "").replace("piece/pieces", "").replace("-", "").replace("quarts", "")
                            mj, n, *others = [i for i in m.split()]
                            if len(others) >= 1:
                                mj, n, *_ = [i for i in m.split()]
                            xd = item.find('div', attrs={'class': 'price'}).text.replace('$', ' ')
                            y = Decimal(xd) * 130
                            regularprice = str(round(float(y)))
                            lookup_params = {'product_id': product_data['no'], 'm1': mj, 'm2': n}
                            # Try to retrieve the object from the database
                            product_price, created = ProductPrice.objects.get_or_create(defaults={'price': regularprice}, **lookup_params)

                            # If the object was not created, update its price
                            if not created:
                                product_price.price = regularprice
                                product_price.save()
                            print(" Price1: " + regularprice,"moq: " + mj + '-'+n)
                            if not regularprice:
                                print("value error 2")
                                raise ValueError
                    
                    except:
                        for item in kobai:
                            moq = item.find('span', attrs={'class': 'moq'}).text
                            m = moq.replace("boxes", "").replace("rolls", "").replace("piece/", "").replace("bag/bags", "").replace("pairs", "").replace("square meters", "").replace("piece/pieces", "").replace("pieces", "").replace("quarts", "").replace("sets", "").replace("-", "").replace("unit/units", "").replace("roll/rolls", "") .replace("set/", "").replace("sets/Sets", "").replace("pair/pairs", "")
                            xd = item.find('span', attrs={'class': 'price'}).text.replace('$', ' ').replace('-', ' ')
                            a, b = [Decimal(i) for i in xd.split()]
                            x = a * 130
                            y = b * 130
                            proprice = str(round(float(x)))
                            price = str(round(float(y)))
                            ProductPrice.objects.create(product_id=product_data['no'], price=price,proprice=(price + "-" + proprice),  m2 = m)

                    else:
                        items = kobai.findAll('div', attrs={'class': 'price-range'})
                        for item in items:
                            moq = item.find('span', attrs={'class': 'moq'}).text
                            m = moq.replace("pieces", "").replace("rolls", "").replace("piece/pieces", "").replace("boxes", "").replace("pairs", "").replace("units", "").replace("piece/", "").replace("piece/pieces", "").replace("sets", "").replace("quarts", "").replace("-", "").replace(">=", "")
                            mj, n, *others = [i for i in m.split()]
                            if len(others) >= 1:
                                mj, n, *_ = [i for i in m.split()]
                            xd = item.find('span', attrs={'class': 'price'}).text.replace('$', ' ').replace('-', ' ')
                            a, b = [Decimal(i) for i in xd.split()]
                            x = a * 130
                            y = b * 130
                            proprice = str(round(float(x)))
                            price = str(round(float(y)))
                            ProductPrice.objects.create(product_id=product_data['no'], price=price,proprice=(price + "-" + proprice),  m2 = m)
                            print("price: " + (price + " - " + proprice),"moq: " + (str(str(mj) + '-'+str(n))))
                            if not price:
                                print("value error 3")
                                raise ValueError
                # external single product price
                except ValueError:
                    try:
                        try:
                            for item in kobai:
                                moq = item.find('span', attrs={'class': 'moq'}).text
                                ks = item.find('span', attrs={'class': 'price'}).text
                                ls = ks.replace('$', '').replace("rolls", "").replace("boxes", "").replace('-', '').replace(',', '') 
                                m = moq.replace("pieces", "").replace("pairs", "").replace("piece/", "").replace("piece/pieces", "").replace('set/sets', '').replace("quarts", "") .replace("sets", "").replace("sets/", "").replace("sets/Sets", "").replace("-", "")
                                a, b = [d for d in m.split()]  
                        
                                x, ys = [d for d in ls.split()]  
                                l = Decimal(ys)
                                ya = l * 130
                                klsa = str(round(float(ya)))
                                ProductPrice.objects.create(product_id=product_data['no'], price=klsa,m1=a,m2=b)
                                print("price: " + klsa, klsa,"m1: " + a,"m2: " + b)
                        
                        except:
                            for item in kobai:
                                moq = item.find('span', attrs={'class': 'moq'}).text
                                ks = item.find('span', attrs={'class': 'promotion'}).text
                                ls = ks.replace('$', '').replace("boxes", "").replace('-', '').replace(',', '') 
                                m = moq.replace("pieces", "").replace("rolls", "").replace("pairs", "").replace("piece/", "").replace("piece/pieces", "").replace('set/sets', '').replace("quarts", "") .replace("sets", "").replace("sets/", "").replace("sets/Sets", "").replace("-", "")

                                x, ys = [d for d in ls.split()]  
                                l = Decimal(ys)
                                ya = l * 130
                                klsa = str(round(float(ya)))
                                ProductPrice.objects.create(product_id=product_data['no'], price=klsa,m2=m)
                                print("price: " + klsa,"m1: " +m)

                        else:
                            items = kobai.findAll('div', attrs={'class': 'price-item'})
                            for item in items:
                                
                                moq = item.find('div', attrs={'class': 'quality'}).text
                                m = moq.replace("pieces", "").replace("rolls", "").replace("boxes", "").replace("pairs", "").replace("units", "").replace("piece/pieces", "").replace("sets", "").replace("-", "").replace("quarts", "")
                                mj, n = [i for i in m.split()]
                                xd = item.find('div', attrs={'class': 'price'}).text.replace('$', ' ')
                                y = Decimal(xd) * 130
                                regularprice = str(round(float(y)))
                                ProductPrice.objects.create(product_id=product_data['no'], price=regularprice,m1=mj, m2=n)
                                print(" Price: " + regularprice,"moq: " + mj + '-'+n)
                            
                            
                            
                    except:
                        try:
                            for item in kobai:
                                moq = item.find('span', attrs={'class': 'promotion-moq'}).text
                                m = moq.replace("pieces", "").replace("rolls", "").replace("pairs", "").replace("boxes", "").replace("units", "").replace("piece/pieces", "").replace("piece/", "").replace("quarts", "").replace("sets", "").replace("sets/", "").replace("sets/Sets", "").replace("-", "").replace(">=", "")
                                
                                xd = item.find('strong', attrs={'class': 'normal'}).text.replace('$', '').replace('-', '').replace(',', '')
                                a = Decimal(xd)
                                x = a * 130
                                proprice = str(round(float(x)))
                                ProductPrice.objects.create(product_id=product_data['no'], price=proprice,m2=m)
                                print("price: " + proprice,"moq: " + m)
                                if not proprice:
                                        raise ValueError
                        except:
                            items = kobai.findAll('div', attrs={'class': 'price-item'})
                            for item in items:
                                
                                moq = item.find('div', attrs={'class': 'quality'}).text
                                m = moq.replace("pieces", "").replace("rolls", "").replace("pairs", "").replace("boxes", "").replace("units", "").replace("piece/pieces", "").replace("sets", "").replace("-", "").replace("quarts", "")
                                mj, n = [i for i in m.split()]
                                xd = item.find('div', attrs={'class': 'price'}).text.replace('$', ' ').replace(',', '')
                                print(xd)
                                y = Decimal(xd) * 130
                                regularprice = str(round(float(y)))
                                ProductPrice.objects.create(product_id=product_data['no'], price=regularprice,m1=mj,m2=n)
                                print(" Price: " + regularprice,"moq: " + mj + '-'+n)




                # pc  color  
                try:
                    color = driver.find_element(By.CLASS_NAME, "sku-body")
                except:
                    color = driver.find_element(By.CLASS_NAME, "sku-none")
                    
                color_code = color.get_attribute("outerHTML")
                color_kobai = BeautifulSoup(color_code, 'html.parser')

                images = color_kobai.select('img')
                image_link = [images['src'].replace("_100x100.jpg", "").replace("_.*#", "").replace("_50x50.jpg", "").replace("_100x100xz.jpg", "").replace("_100x100xz.png", "").replace("_50x50.png", "") for images in images]
                image_data = [images['title'] for images in images]

                if len(image_link) == len(image_data):
                    for i, j in zip(image_link, image_data):
                        skucolor.objects.create(product_id=product_data['no'], color=j, image=i)
                else:
                    kka = color_kobai.find_all('span', attrs={'class':'color'})
                    image_data = [kka['title'] for kka in kka]
                    
                    for i in image_data:
                        skucolor.objects.create(product_id=product_data['no'], color=i)

                # pc  size
                try:
                    try:
                        kall = driver.find_element(By.CLASS_NAME, "sku-body")
                        koil = kall.get_attribute("outerHTML")
                        kobi = BeautifulSoup(koil, 'html.parser')
                        kabil = kobi.find('span', attrs={'class':'txt'})
                        sizes = []
                        res = [val for val in kabil if val is not None]
                        if not res:
                            raise ValueError
                        else:
                            kab = [i.text for i in balo]
                            resk = [i for i in kab if i not in image_data]
                            for i in resk:
                                sizes = i.replace(" ", "_").replace(l)
                                skusize.objects.create(product_id=product_data['no'], size=sizes)
                    except ValueError:
                        kall = driver.find_element(By.CLASS_NAME, "sku-body")
                        koil = kall.get_attribute("outerHTML")
                        kobi = BeautifulSoup(koil, 'html.parser')
                        balo = kobi.find_all('span', attrs={'class':'txt'})
                        kab = [i.text for i in balo]
                        resk = [i for i in kab if i not in image_data]
                        for i in resk:
                            sizes = i.replace(" ", "_")
                            skusize.objects.create(product_id=product_data['no'], size=sizes)
                    except:
                        kall = driver.find_element(By.CLASS_NAME, "sku-body")
                        koil = kall.get_attribute("outerHTML")
                        kobi = BeautifulSoup(koil, 'html.parser')
                        balo = kobi.find_all('span', attrs={'class':'txt'})
                        kab = [i.text for i in balo]
                        resk = [i for i in kab if i not in image_data]
                        for i in resk:
                            sizes = i.replace(" ", "_")
                            skusize.objects.create(product_id=product_data['no'], size=sizes)
                # Empty Size
                except:
                    kall = driver.find_element(By.CLASS_NAME, "sku-none")
                    koil = kall.get_attribute("outerHTML")
                    kobi = BeautifulSoup(koil, 'html.parser')
                    balo = kobi.find_all('span', attrs={'class':'txt'})
                    if not balo:
                        sizes = "quantity"
                        skusize.objects.create(product_id=product_data['no'], size=sizes)

                finally:
                    if not sizes:
                        sizes = "quantity"
                        skusize.objects.create(product_id=product_data['no'], size=sizes)


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
                        ProductDes.objects.create(product_id=product_data['no'], shortdes=kas,fulldes=kad)
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
                                description.objects.create(product_id=product_data['no'],des = data_src)            
                except:
                    pass
                # reviews
                try:
                    reviewsk = driver.find_element(By.CLASS_NAME,'detail-next-loading-wrap')
                    rew = reviewsk.get_attribute('outerHTML')
                    ravi = BeautifulSoup(rew, 'html.parser')
                    review_items = ravi.find_all('div', class_='review-item')

                    for item in review_items:
                        buyer_name = item.find('div', class_='name').text
                        text_list = item.find('div', class_='country').text.split('\n')
                        country = [text for text in text_list if text.strip()][0]
                        review_time = item.find('div', class_='time').text
                        review_text = item.find('div', class_='content').text.strip()
                        reviews.objects.create(product_id=product_data['no'],Buyer_name = buyer_name,Country = country,Review_time = review_time,Review_text  = review_text )            
                except:
                    pass


                driver.close()
                products = Product.objects.get(link__icontains=newurl)
                prices = ProductPrice.objects.filter(product_id=products.product_no)
                image_data = ProductImage.objects.filter(product_id=products.product_no)
                print(products)
                for j in prices:
                    price = j.price
                    if  j.m1 == None:
                        m1 = 1
                        print(j.m1)
                    else:
                        m1=j.m1
                        print(m1)
                        break
                for i in image_data:
                    imegs = i.image
                print(price)
                print(imegs)  
                api_url = 'https://graph.facebook.com/v16.0/103683522715299/messages'

                message_data = {
                    'recipient': {'id': sender_id},
                    'message': {
                        'attachment': {
                            'type': 'template',
                            'payload': {
                                'template_type': 'generic',
                                'elements': [{
                                    'title': products.name[:40],
                                    'image_url': imegs,
                                    'subtitle': f'Price {price} \nMOQ : {m1}',
                                    'default_action': {
                                        'type': 'web_url',
                                        'url': products.link,
                                        'messenger_extensions': False,
                                        'webview_height_ratio': 'TALL'
                                    },
                                    'buttons': [
                                        {
                                            'type': 'web_url',
                                            'url': f'https://ecargo.com.bd/product/{products.name}/{products.product_no}/{products.id}',
                                            'title': 'Visit Now'
                                        }
                                    ]
                                }]
                            }
                        }
                    }
                }
                # Send the message data to the API URL
                response = requests.post(api_url,params={'access_token': VERIFY_TOKEN}, json=message_data)
                print(response.text)
    
        
    except:
        products = Product.objects.get(link__icontains=newurl)
        prices = ProductPrice.objects.filter(product_id=products.product_no)
        image_data = ProductImage.objects.filter(product_id=products.product_no)
        print(products)
        for j in prices:
            price = j.price
            if  j.m1 == None:
                m1 = 1
                print(j.m1)
            else:
                m1=j.m1
                print(m1)
                break
        for i in image_data:
            imegs = i.image
        print(price)
        print(imegs)    
        api_url = 'https://graph.facebook.com/v16.0/103683522715299/messages'

        message_data = {
            'recipient': {'id': sender_id},
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'generic',
                        'elements': [{
                            'title': products.name[:40],
                            'image_url': imegs,
                            'subtitle': f'Price {price} \nMOQ : {m1}',
                            'default_action': {
                                'type': 'web_url',
                                'url': products.link,
                                'messenger_extensions': False,
                                'webview_height_ratio': 'TALL'
                            },
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': f'https://ecargo.com.bd/product/{products.name}/{products.product_no}/{products.id}',
                                    'title': 'Visit Now'
                                }
                            ]
                        }]
                    }
                }
            }
        }
        # Send the message data to the API URL
        response = requests.post(api_url,params={'access_token': VERIFY_TOKEN}, json=message_data)
        print(response.text)


# for all Pay for me query
def handle_PFM_order(messaging_event):
    user_data = check_user(messaging_event)
    if user_data is None:
        sender_id = messaging_event['sender']['id']
        response_text = "যে নাম্বারটি দিয়ে আপনি ওর্ডার প্লেস করেছেন আমাকে সে নাম্বারটা দিন। \n Ex:01XXXXXX"
        send_message(sender_id, response_text)
        
        print("i2")
    elif user_data[0] == "Valid":
        phone = user_data[1]
        PFM_order = payforme.objects.filter(phone=phone)
        print(PFM_order)
        print(f"11-digit number: {phone}")
        if PFM_order:
            orders_dict = {}
            for req_obj in PFM_order:
                if req_obj.payment_id in orders_dict:
                    orders_dict[req_obj.id].append(req_obj.payment_id)
                else:
                    orders_dict[req_obj.id] = [req_obj.payment_id]
                print(orders_dict)
            order_numbers = list(set([order_num for order_nums in orders_dict.values() for order_num in order_nums]))
            response_texts = []
            for order_num in order_numbers:
                count = 0
                statuses = []
                print(orders_dict.items())
                for order_id, order_nums in orders_dict.items():
                    if order_num in order_nums:
                        count += 1
                        order = payforme.objects.get(id=order_id)
                        statuses.append(order.status)
                if count > 0:
                    status_str = ", ".join(list(set(statuses)))
                    response_text = f"\nPay For Me Payment Number: {order_num}\nStatus: {status_str}"
                    response_texts.append(response_text)
            extra = "\n\n কোন নির্দিষ্ট অর্ডার সম্পর্কে জানতে শুদু অর্ডার নাম্বারটি দিন।\nউদাহরনঃ 5000###"
            response_texts.append(extra)
            if response_texts:
                sender_id = messaging_event['sender']['id']
                send_message(sender_id, "\n".join(response_texts))
                
            else:
                sender_id = messaging_event['sender']['id']
                response_text = "No Request orders found with this phone number."
                send_message(sender_id, response_text)
        else:
            sender_id = messaging_event['sender']['id']
            response_text = "কোন ওর্ডার নেই আপনার এই নাম্বারের অধীনে।"
            send_message(sender_id, response_text)
        
    return HttpResponse(status=200)


# for all Shipping for me query
def handle_SFM_order(messaging_event):
    user_data = check_user(messaging_event)
    if user_data is None:
        sender_id = messaging_event['sender']['id']
        response_text = "যে নাম্বারটি দিয়ে আপনি ওর্ডার প্লেস করেছেন আমাকে সে নাম্বারটা দিন। \n Ex:01XXXXXX"
        send_message(sender_id, response_text)
        
        print("i2")
    elif user_data[0] == "Valid":
        phone = user_data[1]
        SFM_order = Shipping.objects.filter(phone=phone)
        print(SFM_order)
        print(f"11-digit number: {phone}")
        if SFM_order:
            orders_dict = {}
            for req_obj in SFM_order:
                if req_obj.shipping_id in orders_dict:
                    orders_dict[req_obj.id].append(req_obj.shipping_id)
                else:
                    orders_dict[req_obj.id] = [req_obj.shipping_id]
                print(orders_dict)
            order_numbers = list(set([order_num for order_nums in orders_dict.values() for order_num in order_nums]))
            response_texts = []
            for order_num in order_numbers:
                count = 0
                statuses = []
                print(orders_dict.items())
                for order_id, order_nums in orders_dict.items():
                    if order_num in order_nums:
                        count += 1
                        order = Shipping.objects.get(id=order_id)
                        statuses.append(order.status)
                if count > 0:
                    status_str = ", ".join(list(set(statuses)))
                    response_text = f"\nShipping For Me Shippig Number: {order_num}\nStatus: {status_str}"
                    response_texts.append(response_text)

            extra = "\n\n কোন নির্দিষ্ট অর্ডার সম্পর্কে জানতে শুদু অর্ডার নাম্বারটি দিন।\nউদাহরনঃ 4000###"
            response_texts.append(extra)
            if response_texts:
                sender_id = messaging_event['sender']['id']
                send_message(sender_id, "\n".join(response_texts))
                
            else:
                sender_id = messaging_event['sender']['id']
                response_text = "No Request orders found with this phone number."
                send_message(sender_id, response_text)
        else:
            sender_id = messaging_event['sender']['id']
            response_text = "কোন ওর্ডার নেই আপনার এই নাম্বারের অধীনে।"
            send_message(sender_id, response_text)
        
    return HttpResponse(status=200)


# for all Shop for me query
def handle_req_order(messaging_event):
    user_data = check_user(messaging_event)
    if user_data is None:
        sender_id = messaging_event['sender']['id']
        response_text = "যে নাম্বারটি দিয়ে আপনি ওর্ডার প্লেস করেছেন আমাকে সে নাম্বারটা দিন। \n Ex:01XXXXXX"
        send_message(sender_id, response_text)
        
        print("i2")
    elif user_data[0] == "Valid":
        phone = user_data[1]
        req_order = req.objects.filter(customer__mobile=phone)
        print(req_order)
        print(f"11-digit number: {phone}")
        if req_order:
            orders_dict = {}
            for req_obj in req_order:
                if req_obj.order_id in orders_dict:
                    orders_dict[req_obj.id].append(req_obj.order_id)
                else:
                    orders_dict[req_obj.id] = [req_obj.order_id]
                print(orders_dict)
            order_numbers = list(set([order_num for order_nums in orders_dict.values() for order_num in order_nums]))
            response_texts = []
            for order_num in order_numbers:
                count = 0
                statuses = []
                print(orders_dict.items())
                for order_id, order_nums in orders_dict.items():
                    if order_num in order_nums:
                        count += 1
                        order = req.objects.get(id=order_id)
                        statuses.append(order.status)
                if count > 0:
                    status_str = ", ".join(list(set(statuses)))
                    response_text = f"\nShop For Me Status Shopping Number: {order_num}\nStatus: {status_str}"
                    response_texts.append(response_text)
            extra = "\n\n কোন নির্দিষ্ট অর্ডার সম্পর্কে জানতে শুদু অর্ডার নাম্বারটি দিন।\nউদাহরনঃ 9000###"
            response_texts.append(extra)
            if response_texts:
                sender_id = messaging_event['sender']['id']
                send_message(sender_id, "\n".join(response_texts))
                
            else:
                sender_id = messaging_event['sender']['id']
                response_text = "No Request orders found with this phone number."
                send_message(sender_id, response_text)
        else:
            sender_id = messaging_event['sender']['id']
            response_text = "কোন ওর্ডার নেই আপনার এই নাম্বারের অধীনে।"
            send_message(sender_id, response_text)
        
    return HttpResponse(status=200)

# for all Orders query
def handle_order(messaging_event):
    user_data = check_user(messaging_event)
    if user_data is None:
        sender_id = messaging_event['sender']['id']
        response_text = "যে নাম্বারটি দিয়ে আপনি ওর্ডার প্লেস করেছেন আমাকে সে নাম্বারটা দিন। \n Ex:01XXXXXX"
        send_message(sender_id, response_text)
        
        print("i2")
    elif user_data[0] == "Valid":
        phone = user_data[1]
        orders = OrerPrduct.objects.filter(orderi__phone=phone)
        print(f"11-digit number: {phone}")
        if orders:
            orders_dict = {}
            for i in orders:
                if i.orderi in orders_dict:
                    orders_dict[i.orderi].append(i.OrderP_id)
                else:
                    orders_dict[i.orderi] = [i.OrderP_id]
            order_numbers = list(set([order_num for order_nums in orders_dict.values() for order_num in order_nums]))
            response_texts = []
            for order_num in order_numbers:
                count = 0
                statuses = []
                for order, order_nums in orders_dict.items():
                    if order_num in order_nums:
                        count += 1
                        statuses.append(order.status)
                if count > 0:
                    status_str = ", ".join(list(set(statuses)))
                    response_text = f"\nOrder Number: {order_num}\nStatus: {status_str}"
                    response_texts.append(response_text)
                
            extra = "\n\n কোন নির্দিষ্ট অর্ডার সম্পর্কে জানতে শুদু অর্ডার নাম্বারটি দিন।\nউদাহরনঃ 1000###"
            response_texts.append(extra)
            if response_texts:
                sender_id = messaging_event['sender']['id']
                send_message(sender_id, "\n".join(response_texts))
                
            else:
                sender_id = messaging_event['sender']['id']
                response_text = "No orders found with this phone number."
                send_message(sender_id, response_text)
        else:
            sender_id = messaging_event['sender']['id']
            response_text = "কোন ওর্ডার নেই আপনার এই নাম্বারের অধীনে।"
            send_message(sender_id, response_text)
        
    return HttpResponse(status=200)

    
  
# validate user for database
def get_user_data(user_id):
    # Get user data from the Facebook Graph API
    user_data_url = f"https://graph.facebook.com/{user_id}?fields=first_name,last_name,profile_pic&access_token={PAGE_ACCESS_TOKEN}"
    response = requests.get(user_data_url)
    user_data = json.loads(response.content)
    return user_data


# send generik message
def send_message(recipient_id, response_text):
    # Set the API endpoint URL and access token
    # print("Reciver ID: " + recipient_id)
    api_url = 'https://graph.facebook.com/v16.0/me/messages'
    access_token = 'EAABZCL2kI5vIBAJQ7dyFn9X5PpMywnIuHedcf31RJZChDJnjZCzmzIx7EeWu7CvZCzhRCRjWBs25uSEn3pOrMcZBER77dtj2k4VbSwEDsXDgGM4kFWod8aZApgQw3FZCPmnAD8Tno0UTxMCGWwrsY7MgerYRMEMnyb3IxppLo1pNyd98gPMbHzA'

    # Send typing indicator
    dat = {
        'recipient': json.dumps({'id': recipient_id}),
        'sender_action': 'typing_on',
        'messaging_type': 'RESPONSE',
        'access_token': access_token,
    }
    response = requests.post(api_url, params=dat)
    # print(response.text)

    multi = Extra_quick_replays.objects.all()
    if multi:
        extra_quciks = [
            {
                "content_type": "text",
                "title": i.name,
                "payload": i.name
            } for i in multi
        ]
    else:
        extra_quciks = []
    # Set up the Quick Replies template
    quick_replies = [
        {
            "content_type": "text",
            "title": "Product information",
            "payload": "PRODUCT_INFO"
        },
        {
            "content_type": "text",
            "title": "Order status",
            "payload": "ORDER_STATUS"
        },
        {
            "content_type": "text",
            "title": "Shop For Me Status",
            "payload": "req_status"
        },
        {
            "content_type": "text",
            "title": "Ship For Me Status",
            "payload": "SFM_status"
        },
        {
            "content_type": "text",
            "title": "Pay For Me Status",
            "payload": "PFM_status"
        },
    ] + extra_quciks
    # Add the quick reply to the message payload
    message = {
        "text": response_text,
        "quick_replies": quick_replies
    }

    # Send the message to the user
    data = {
        'recipient': json.dumps({'id': recipient_id}),
        'message': json.dumps(message),
        'messaging_type': 'RESPONSE',
        'access_token': access_token,
    }
    response = requests.post(api_url, params=data)
    if response.status_code != 200:
        pass


# handle post back
def handle_postback(messaging_event):
    sender_id = messaging_event['sender']['id']
    send_message(sender_id, f'Hi , thank you for choosing our service.')

    # # Handle payload
    # if message_text == 'আমাদের_সার্ভিস':
    #     user_data = get_user_data(sender_id)
    #     first_name = user_data['first_name']
    #     # send_website_link(sender_id)
    # elif message_text == 'ORDER_STATUS':
    #     send_message(sender_id, 'Your order status is...', {'content_type': 'text', 'title': 'Back', 'payload': 'BACK'})
   

@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        # Handle webhook verification
        mode = request.GET.get('hub.mode')
        challenge = request.GET.get('hub.challenge')
        verify_token = request.GET.get('hub.verify_token')
        if mode == 'subscribe' and verify_token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse(status=403)
    elif request.method == 'POST':
        # Handle incoming messages and postbacks
        data = json.loads(request.body.decode('utf-8'))
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):
                    # check page message or user message
                    # page Id here
                    processed_messages = set()
                    if messaging_event['sender']['id'] == '103683522715299':
                        pass
                    else:
                        if messaging_event['message']['mid'] not in processed_messages:
                            processed_messages.add(messaging_event['message']['mid'])
                            handle_message(messaging_event)
                        else:
                            print(f"Message with ID {messaging_event['message']['mid']} has already been processed.")
                elif messaging_event.get('postback'):
                    handle_postback(messaging_event)
              
        return HttpResponse(status=200)

    else:
        return HttpResponse(status=405)


# get user all message
def get_all_msg(message_id, sender_id):
    url = f"https://graph.facebook.com/v16.0/{message_id}/messages"
    params = {
        "access_token": VERIFY_TOKEN,
        "pretty": "0",
        "fields": "message,id,from",
    }

    all_data = []

    first_eleven_digit_number = None
    first_four_digit_number = None

    while url and not (first_eleven_digit_number and first_four_digit_number):
        response = requests.get(url, params=params)
        json_data = response.json()
        all_data.extend(json_data["data"])

        for conversation in all_data:
            if conversation['from']['id'] == sender_id:
                match = re.search(r'\b\d{11}\b', conversation['message'])
                if match:
                    first_eleven_digit_number = match.group()
                    if first_four_digit_number:
                        url = None
                        break

                match = re.search(r'\b\d{4}\b', conversation['message'])
                if match:
                    first_four_digit_number = match.group()
                    if first_eleven_digit_number:
                        url = None
                        break

        if "paging" in json_data and "next" in json_data["paging"]:
            url = json_data["paging"]["next"]
        else:
            url = None
        
    return all_data



# Check user
def check_user(messaging_event):
    urls = f'https://graph.facebook.com/me?fields=conversations{{id}}&access_token={VERIFY_TOKEN}'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(urls, headers=headers)
    message_id = response.json()['conversations']['data'][0]['id']
    sender_id = messaging_event['sender']['id']
    all_data = get_all_msg(message_id, sender_id)
    datamsg = []
    first_eleven_digit_number = None
    first_four_digit_number = None
    first_two_messages = []
    for conversation in all_data:
        if conversation['from']['id'] == sender_id:
            # print(conversation['message'])
            datamsg.append(conversation['message'])
            if not first_eleven_digit_number:
                match = re.search(r'\b\d{11}\b', conversation['message'])
                if match:
                    first_eleven_digit_number = match.group()
            if not first_four_digit_number:
                match = re.search(r'\b\d{4}\b', conversation['message'])
                if match:
                    first_four_digit_number = match.group()
    response_text = "Please wait, let me check your data."
    send_message(sender_id, response_text)

    if first_eleven_digit_number and first_four_digit_number:
        check_phone = Profile.objects.filter(mobile=first_eleven_digit_number).first()
        check_otp = Profile.objects.filter(otp=first_four_digit_number).first()
        if check_phone and check_otp:
            valid_data = ("Valid", first_eleven_digit_number)
            return valid_data
        else:
            main_text = "Verification failed.\nPhone number or OTP do not match. Please provide correct data."
            print('No match found')
            # Call send_message only once
            send_message(sender_id, main_text)
        
 
    return None


# check user only for OTP check first time
def check_OTP_only(messaging_event):
    urls = f'https://graph.facebook.com/me?fields=conversations{{id}}&access_token={VERIFY_TOKEN}'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(urls, headers=headers)
    message_id = response.json()['conversations']['data'][0]['id']
    sender_id = messaging_event['sender']['id']
    all_data = get_all_msg(message_id, sender_id)
    datamsg = []
    first_eleven_digit_number = None
    first_four_digit_number = None
    first_two_messages = []
    for conversation in all_data:
        if conversation['from']['id'] == sender_id:
            # print(conversation['message'])
            datamsg.append(conversation['message'])
            if not first_eleven_digit_number:
                match = re.search(r'\b\d{11}\b', conversation['message'])
                if match:
                    first_eleven_digit_number = match.group()
            if not first_four_digit_number:
                match = re.search(r'\b\d{4}\b', conversation['message'])
                if match:
                    first_four_digit_number = match.group()
            if len(first_two_messages) < 2:
                first_two_messages.append(conversation['message'])
            if first_eleven_digit_number and first_four_digit_number and first_two_messages:
                break
    last_msg = None
    prev_msg = None
    if first_two_messages:
        last_msg = first_two_messages[0]
        prev_msg = first_two_messages[1]

    print(last_msg, prev_msg)
    if prev_msg.startswith(('01')) and len(prev_msg) == 11:
        response_text = "Please wait, let me check your data."
        send_message(sender_id, response_text)

        if first_eleven_digit_number and first_four_digit_number:
            check_phone = Profile.objects.filter(mobile=first_eleven_digit_number).first()
            check_otp = Profile.objects.filter(otp=first_four_digit_number).first()
            if check_phone and check_otp:
                main_text = "Verification successful.\n\nChoose an option below to get your data."
                send_message(sender_id, main_text)
                valid_data = ("Valid", first_eleven_digit_number)
                # Move send_message call outside the loop
                print('founr daga')
                return valid_data
            else:
                main_text = "Verification failed.\nPhone number or OTP do not match. Please provide correct data."
                print('No match found')
                # Call send_message only once
                send_message(sender_id, main_text)
        
    else:
        pass
    return None


def get_messages(sender_id, message_text):
    url = f'https://graph.facebook.com/me?fields=conversations{{messages{{message,id,from}}}}&access_token={VERIFY_TOKEN}'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    data = response.json()['conversations']['data']
    previous_message = None
    latest_message = None
    for conversation in data:
        messages = conversation['messages']['data']
        for i in range(len(messages)-1, -1, -1):
            message = messages[i]
            if 'from' in message and message['from']['id'] == sender_id:
                if 'message' in message:
                    if latest_message is None:
                        latest_message = message_text
                    elif previous_message is None and 'Order status' in message['message']:
                        previous_message = message['message']
                        break
    
    # check user alreeady exits and do further
    user = Profile.objects.filter(mobile = latest_message).first()
    
    # if user not exit create new one
    if user is None:
        user = User(username = latest_message )
        user.save()
        otp = str(random.randint(1000 , 9999))
        kalaa = User.objects.get(username = latest_message)
        profile = Profile(user = kalaa , mobile=latest_message , otp = otp) 
        profile.save()
        send_otp(latest_message, otp)
        send_message(sender_id, 'Do not find any user under this nuumber. Creating New User.')
        response_text = "Provide Us 4 digit OTP. We Send Your Phone number your provide"
        send_message(sender_id, response_text)
      
    else:
        #  Elase user exit then do this work
        otp = str(random.randint(1000 , 9999))
        user.otp = otp
        user.save()
        send_otp(latest_message , otp)                
        response_text = "Provide Us 4 digit OTP. We Send Your Phone number your provide."
        send_message(sender_id, response_text)

    print(previous_message, latest_message)
 


def check_otp(message_text, sender_id, messaging_event):
    user_data = check_user(messaging_event)
    

