import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.utils.timezone import now, localtime
from order.models import *
from django.http import JsonResponse
from apiclient.discovery import build
# from oauth2client.service_account import ServiceAccountCredentials



@csrf_exempt
def reqo_report(request):
    status_data = {}
    for choice in req.STATUS:
        count = req.objects.filter(status=choice[0]).count()
        status_data[choice[0]] = count
    return JsonResponse(status_data)

@csrf_exempt
def shipping_report(request):
    status_data = {}
    for choice in Shipping.STATUS:
        count = Shipping.objects.filter(status=choice[0]).count()
        status_data[choice[0]] = count
    return JsonResponse(status_data)



@csrf_exempt
def recent_orders(request):
    orders = OrerPrduct.objects.order_by('-created_at')[:20]
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'user': order.user.username,
            'product': order.product.name[:10],
            'quantity': order.quantity,
            'price': order.price,
            'status': order.status,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'data': data})

@csrf_exempt
def recent_req_orders(request):
    orders = req.objects.order_by('-created_at')[:20]
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'user': order.user.username,
            'link': order.link,
            'quantity': order.quantity,
            'price': order.price,
            'status': order.status,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'data': data})

@csrf_exempt
def recent_shipping_orders(request):
    orders = Shipping.objects.order_by('-created_at')[:20]
    data = []
    for order in orders:
        data.append({
            'user': order.user.username,
            'shipping_id': order.shipping_id,
            'quantity': order.quantity,
            'note': order.note,
            'tracking': order.tracking,
            'total_weight': order.total_weight,
            'weight_charge': order.weight_charge,
            'total_weight_charge': order.total_weight_charge,
            'internal_shipping_charge': order.internal_shipping_charge,
            's_total': order.s_total,
            'status': order.status,
            'country': order.country,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'data': data})

@csrf_exempt
def recent_orders_delivery(request):
    orders = ORequest_Delivery.objects.order_by('-created_at')[:20]
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'user': order.user.username,
            'orderi_id': order.orderi_id,
            'Name': order.Name,
            'Address': order.Address,
            'Phone': order.Phone,
            'status': order.status,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'data': data})

@csrf_exempt
def recent_req_orders_delivery(request):
    orders = RRequest_Delivery.objects.order_by('-created_at')[:20]
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'user': order.user.username,
            'orderi_id': order.orderi_id,
            'Name': order.Name,
            'Address': order.Address,
            'Phone': order.Phone,
            'status': order.status,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'data': data})

@csrf_exempt
def shipping_orders_delivery(request):
    orders = SRequest_Delivery.objects.order_by('-created_at')[:20]
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'user': order.user.username,
            'orderi_id': order.orderi_id,
            'Name': order.Name,
            'Address': order.Address,
            'Phone': order.Phone,
            'status': order.status,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'data': data})

@csrf_exempt
def req_partial_payment(request):
    orders = Req_Order_Partial_Payment.objects.order_by('-created_at')[:20]
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'user': order.user.username,
            'orderi_id': order.orderi_id,
            'p_status': order.p_status,
            'Amount': order.Amount,
            't_m': order.t_m,
            't_id': order.t_id,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'data': data})

@csrf_exempt
def order_partial_payment(request):
    orders = Order_Partial_Payment.objects.order_by('-created_at')[:20]
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'user': order.user.username,
            'orderi_id': order.orderi_id,
            'p_status': order.p_status,
            'Amount': order.Amount,
            't_m': order.t_m,
            't_id': order.t_id,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'data': data})



def order_partial_payment_table(request):
    # Get all the partial payments
    partial_payments = Order_Partial_Payment.objects.all()
    # Create a list to store the serialized data
    data = []
    # Loop through each partial payment and serialize the data
    for partial_payment in partial_payments:
        data.append({
            'id': partial_payment.id,
            'user': partial_payment.user.username,
            'order_id': partial_payment.orderi.OrderP_id,
            'status': partial_payment.p_status,
            'amount': str(partial_payment.Amount),
            'transaction_method': partial_payment.t_m,
            'transaction_id': partial_payment.t_id,
            'transaction_image': partial_payment.t_img.url if partial_payment.t_img else '/static/images/eargo_icon.png',
            'created_at': partial_payment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': partial_payment.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        })
    # Return the serialized data as a JSON response
    return JsonResponse({'data': data})

def analytics_data(request):
    # Set up the Google Analytics Reporting API client
    credentials = ServiceAccountCredentials.Credentials.from_service_account_file('C:/Users/Nobel/projects/8/quicks/ecargo-380620-d0d4ae417062.json')
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    
    # Set up the Google Analytics Reporting API request
    response = analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': '358238426', # Replace with your Google Analytics View ID
                    'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:sessions'}],
                    'dimensions': [{'name': 'ga:date'}]
                }
            ]
        }
    ).execute()

    # Process the response data and return it as a JSON response
    data = []
    for row in response['reports'][0]['data']['rows']:
        data.append({
            'date': row['dimensions'][0],
            'sessions': int(row['metrics'][0]['values'][0])
        })
    return JsonResponse(data, safe=False)