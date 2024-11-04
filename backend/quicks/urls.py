
from django.conf import settings
from django.urls import include, path
from django.contrib import admin
# from home import models
from store.views import *
from order.views import *
from django.views.static import serve 
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

urlpatterns = [
    path('load-more-data',load_more_data,name='load_more_data'),
    path('productdescription/<str:product_no>/', get_description, name='product-description'),
    path('getReview/<str:product_no>/', get_Review, name='getReview'),
    path('reqpays/<int:id>',reqpays,name='reqpays'),
    path('singleRRequest_Deliveryr/<int:id>',singleRRequest_Deliveryr,name='singleRRequest_Deliveryr'),
    path('singleSRequest_Deliveryr/<int:id>',singleSRequest_Deliveryr,name='singleSRequest_Deliveryr'),
    path('singleRRequest_Delivery/<int:id>',singleRRequest_Delivery,name='singleRRequest_Delivery'),
    path('shippays/<int:id>',shippays,name='shippays'),
    path('shipdpay/<int:id>',shipdpay,name='shipdpay'),
    path('reqpaynowreq/<int:id>',ReqPayNowReqAPIView.as_view(),name='reqpaynowreq'),
    path('ReqssPayView/<int:id>',ReqssPayView.as_view(),name='ReqssPayView'),
    path('PaysformePayNowReq/<int:id>',PaysformePayNowReqAPIView.as_view(),name='PaysformePayNowReq'),
    path('reqpay/<int:id>',reqpay,name='reqpay'),
    path('singleSRequest_Delivery/<int:id>',singleSRequest_Delivery,name='singleSRequest_Delivery'),
    path('ShippingOrderDeliveryRequest/<int:id>',ShippingOrderDeliveryRequestAPIView.as_view(),name='ShippingOrderDeliveryRequest'),
    path('reqpaynow/<int:id>',reqpaynow,name='reqpaynow'),
    path('rpayallp/',rpayallp,name='rpayallp'),
    path('rpayallreqp/',rpayallreqp,name='rpayallreqp'),
    path('frRequest_Deliveryr/',frRequest_Deliveryr,name='frRequest_Deliveryr'),
    path('rpayall/',rpayall,name='rpayall'),
    path('opayall/',opayall,name='opayall'),
    path('OORequest_Delivery/',OORequest_Delivery,name='OORequest_Delivery'),
    path('OrderDeliveryRequest/<int:id>',OrderDeliveryRequestAPIView.as_view(),name='OrderDeliveryRequest'),
    path('OOSRequest_Delivery/',OOSRequest_Delivery,name='OOSRequest_Delivery'),
    path('fsRequest_Deliveryr/',fsRequest_Deliveryr,name='fsRequest_Deliveryr'),
    path('OORRequest_Delivery/',OORRequest_Delivery,name='OORRequest_Delivery'),
    path('opayallreq/',opayallreq,name='opayallreq'),
    path('fRequest_Deliveryr/',fRequest_Deliveryr,name='fRequest_Deliveryr'),
    path('rpayallreq/',rpayallreq,name='rpayallreq'),
    path('paynowreq/<int:id>',paynowreq,name='paynowreq'),
    path('order-more-data',order_more_data,name='order_more_data'),
    path('', IndexView.as_view()),
    path('shop/',shop,name='shop'),
    path('delivery_req/',delivery_req,name='delivery_req'),
    path('faqs',faqs,name='faqs'),
    path('terms_condition',terms_condition,name='terms_condition'),
    path('forbidenitempagen',forbidenitempagen,name='forbidenitempagen'),
    path('Shipping_refund_Pollicy',Shipping_refund_Pollicy,name='Shipping_refund_Pollicy'),
    path('Privacy_Policy',Privacy_Policy,name='Privacy_Policy'),
    path('apparel_list',apparel_list,name='apparel_list'),
    path('apparel-list-more',apparel_list_more,name='apparel_list_more'),
    path('Shoes_Accessories',Shoes_Accessories,name='Shoes_Accessories'),
    path('Shoes_Accessoriesmore',Shoes_Accessoriesmore,name='Shoes_Accessoriesmore'),
    path('Vehicle_Accessories',Vehicle_Accessories_list,name='Vehicle_Accessories'),
    path('Vehicle_Accessories_list_more',Vehicle_Accessories_list_more,name='Vehicle_Accessories_list_more'),
    path('Fabric_Material',Fabric_Material,name='Fabric_Material'),
    path('Fabric_Material_more',Fabric_Material_more,name='Fabric_Material_more'),
    path('Sports_Entertainment_list',Sports_Entertainment_list,name='Sports_Entertainment_list'),
    path('Sports_Entertainment_list_more',Sports_Entertainment_list_more,name='Sports_Entertainment_list_more'),
    path('Tools_Hardware_list',Tools_Hardware_list,name='Tools_Hardware_list'),
    path('Tools_Hardware_list_more',Tools_Hardware_list_more,name='Tools_Hardware_list_more'),
    path('machinery_list',machinery_list,name='machinery_list'),
    path('machinery_list_more',machinery_list_more,name='machinery_list_more'),
    path('consumer_electronic',consumer_electronic,name='consumer_electronic'),
    path('consumer_electronic_more',consumer_electronic_more,name='consumer_electronic_more'),
    path('Luggage_Bags',Luggage_Bags,name='Luggage_Bags'),
    path('Luggage_Bags_more',Luggage_Bags_more,name='Luggage_Bags_more'),
    path('home_garden',home_garden,name='home_garden'),
    path('paysforme',paysforme,name='paysforme'),
    path('payment',payment,name='payment'),
    path('home_garden_more',home_garden_more,name='home_garden_more'),
    path('beauty_personal_care',beauty_personal_care,name='beauty_personal_care'),
    path('beauty_personal_care_more',beauty_personal_care_more,name='beauty_personal_care_more'),
    path("admin/", admin.site.urls),
    path("orders/", orderss,name='orders'),
    path("search/", search, name="search"),
    path("searchComplete/", searchComplete, name="searchComplete"),
    path("carts/", carts, name="carts"),
    path("checkout/", checkout, name="checkout"),
    path("shipping/", Shippingsk, name="shipping"),
    path("shipped/", shipped, name="shipped"),
    path("shippedpay/<int:id>", shippedpay, name="shippedpay"),
    path("paymentpay/<int:id>", paymentpay, name="paymentpay"),
    path("success/", success, name="success"),
    path("delivery/", delivery, name="delivery"),
    path("comeplete/", comeplete, name="comeplete"),
    path("partial-payments/", partial_payments, name="partial_payments"),
    path("ticket/", ticket, name="ticket"),
    path("ticketadmin/", ticketadmin, name="ticketadmin"),
    path("ticketadd/", ticketadd, name="ticketadd"),
    path("ticketdetails/<int:ticket_no>/<int:id>", ticketdetails, name="ticketdetails"),
    path("wallet/", walletall, name="wallet"),
    path("walletadd/", walletadd, name="walletadd"),
    path("about/", about, name="about"),
    path("reqorderd/<int:id>", reqorderd, name="reqorderd"),
    path("singleRequest_Delivery/<int:id>", singleRequest_Delivery, name="singleRequest_Delivery"),
    path("RequestOrderDeliveryr/<int:id>", RequestOrderDeliveryrAPIView.as_view(), name="RequestOrderDeliveryr"),
    path("Shippingpaynowreq/<int:id>", Shippingpaynowreq_api, name="Shippingpaynowreq"),
    path("reqpay/<int:id>", reqpay, name="reqpay"),
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    path("get_all_products/", get_all_products, name="get_all_products"),
    path("latest_get_all_products/", latest_get_all_products, name="latest_get_all_products"),
    path("carts_delete/<str:product_id>", carts_delete, name="carts_delete"),
    path('get_color/<str:product_id>/', get_color, name='get_color'),
    path('get_Sku/<str:product_id>/', get_Sku, name='get_Sku'),
    path('get_Sellerinfo/<str:product_id>/', get_Sellerinfo, name='get_Sellerinfo'),
    path("get_single_product_images/<str:id>/", get_single_product_images, name="get_single_product_images"),
    path('product/<str:name>/<str:product_no>/<int:id>',product_detail,name='product_detail'),
    path('products/<str:product_no>/<int:id>',productViewSet),
    # path('productdetails/<str:product_no>/<int:id>',ProductList.as_view()),
    path('', include('accounts.urls')),
    path('', include('charts.urls')),
    path('check_search_status/', check_search_status, name='check_search_status'),
    path('get_sizes_for_color/<str:product_id>/<str:color>/', get_sizes_for_color, name='get_sizes_for_color'),
    path('get_sizes/<str:product_id>/', get_sizes, name='get_sizes'),
    path('get_single_product/<str:product_id>/', get_single_product, name='get_single_product'),
    path('get_highest_lowest_prices/<str:product_id>/', get_highest_lowest_prices, name='get_highest_lowest_prices'),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('api/check-authentication/', CheckAuthenticationView.as_view(), name='check-authentication'),
    path('api/update-or-create-address/', AddressUpdateOrCreateView.as_view(), name='update-or-create-address'),
    path('api/register/', UserRegister.as_view(), name='register'),
	path('api/login/', UserLogin.as_view(), name='login'),
	path('api/logout/', UserLogout.as_view(), name='logout'),
	path('api/user/', UserView.as_view(), name='user'),
	path('api/terms_condition/', terms_condition_pageListView.as_view(), name='terms_condition'),
	path('api/Shipping_refund_Pollicy_page/', Shipping_refund_Pollicy_pageListView.as_view(), name='Shipping_refund_Pollicy_page'),
	path('api/aboustuspageList/', aboustuspageListView.as_view(), name='aboustuspageList'),
	path('api/Google_Tag_Manager/', Google_Tag_ManagerListView.as_view(), name='Google_Tag_Manager'),
	path('api/Payment_numbers/', Payment_numbersListView.as_view(), name='Payment_numbers'),
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path('api/user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/forbidenitempagen/', forbidenitempagen_pageListView.as_view(), name='api_forbidenitempagen'),
    path('api/Faqpage/', FaqpageListView.as_view(), name='Faqpage_api'),
    path('api/total-order-products/', TotalOrderProductView.as_view(), name='total-order-products'),
    path('api/TotalShipingCount/', TotalShipingCountView.as_view(), name='TotalShipingCount'),
    path('api/sticketCount/', sticketCountView.as_view(), name='sticketCount'),
    path('api/payforme/', payformeView.as_view(), name='payforme'),
    path('OrderPaymentPayNowReq/<int:id>', OrderPaymentPayNowReqAPIView.as_view(), name='OrderPaymentPayNowReq'),
    path('api/all-order-products/', AllOrderProductView.as_view(), name='all-order-products'),
    path('api/complete-order/', CompleteOrderView.as_view(), name='complete-order'),
    path('wallet/balance/', WalletBalanceView.as_view(), name='wallet-balance'),
    path('api/user_profiles/', UserProfileViews.as_view(), name='user-profiles'),
    path('api/shop/', ShopAPIView, name='shop-api'),
    path('api/paynow/<str:id>/', PayNowView.as_view(), name='paynow'),
    path('api/reqpaynow/<str:id>/', ReqPayNowView.as_view(), name='paynow'),
    path('api/shippingpaynow/<str:id>/', ShippingPayNowView.as_view(), name='shippingpaynow'),
    path('api/PayforMePayNow/<str:id>/', PayforMePayNowView.as_view(), name='PayforMePayNow'),
    path('api/paynowreq/<int:id>/', paynowreq_api, name='paynowreq_api'),
    path('api/rqo/', ReqAPIView.as_view(), name='api_rqo'),
    path('api/Shippingforme/', ShippingPostAPIView.as_view(), name='api_Shippingforme'),
    path('api/Paysforme/', PaysformePostAPIView.as_view(), name='api_Paysforme'),
    path('api/reqorder/', ReqOrderAPIView.as_view(), name='api_reqorder'),
    path('api/shipping/', ShippingAPIView.as_view(), name='api_shipping'),
    path('api/PaymentOrder/', PaymentOrderAPIView.as_view(), name='PaymentOrder'),
    path('api/ShippingOrder/', ShippingOrderAPIView.as_view(), name='ShippingOrder'),
    path('api/shipformedes/', shipformedes_list, name='shipformedes-list'),
    path('api/shipformecharge/', shipformecharge_list, name='shipformecharge-list'),
    path('api/shipformemesssages/', shipformemesssages_list, name='shipformemesssages-list'),
    path('api/order_partial_payment/create/', OrderPartialPaymentCreateAPIView.as_view(), name='order-partial-payment-create'),
    path('site-identity/', SiteIdentityListView.as_view(), name='site-identity-list'),
    path('home-banner/', Home_BanneerListView.as_view(), name='home-banner-list'),
    path('Home_top600px_Banneer/', Home_top600px_BanneerListView.as_view(), name='Home_top600px_Banneer'),
    path('Home_middel502x202px_Banneer/', Home_middel502x202px_BanneerListView.as_view(), name='Home_middel502x202px_Banneer'),
    path('Home_middel680x180px_Banneer/', Home_middel680x180px_BanneerListView.as_view(), name='Home_middel680x180px_Banneer'),
    path('Home_bottom_sites_Banneer/', Home_bottom_sites_BanneerListView.as_view(), name='Home_bottom_sites_Banneer'),
    path('Home_sliding_selling_text_Banneer/', Home_sliding_selling_text_BanneerListView.as_view(), name='Home_sliding_selling_text_Banneer'),
    path('CatagorysList/', CatagorysListView.as_view(), name='CatagorysList'),
    path('Home_4data_breadcum/', Home_4data_breadcumView.as_view(), name='Home_4data_breadcum'),
    path('FooterWidgets/', FooterWidgetsView.as_view(), name='FooterWidgets'),
    path('FooterLinks/', FooterLinkView.as_view(), name='FooterLinks'),
    path('FooterPaymentSuportImage/', FooterPaymentSuportImageView.as_view(), name='FooterPaymentSuportImage'),
    path('subcategories/', CatagorysListWithSubcategories, name='subcategory-list'),
    path('delivery-requests/', CombinedRequestListView.as_view(), name='delivery-requests-list'),
    path('TIketost/', TicketAPIView.as_view(), name='TIketost'),
    path('TicketSms/<int:ticket_id>', TicketSmsAPIView.as_view(), name='TicketSms'),
    path('edit_payment_brief/<int:obj_id>/', edit_payment_brief, name='edit_payment_brief'),
    path('edit_req_payment_brief/<int:obj_id>/', edit_req_payment_brief, name='edit_req_payment_brief'),
    path('edit_shipping_payment_brief/<int:obj_id>/', edit_shipping_payment_brief, name='edit_shipping_payment_brief'),
    path('edit_payforme_payment_brief/<int:obj_id>/', edit_payforme_payment_brief, name='edit_payforme_payment_brief'),
    
]


# Serve static and media files from development server
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index = 'admin/index.html'
admin.site.site_header = 'My project'                    # default: "Django Administration"
admin.site.index_title = 'Features area'                 # default: "Site administration"
admin.site.site_title = 'HTML title from adminsitration'