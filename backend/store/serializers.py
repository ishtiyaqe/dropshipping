from xml.dom import ValidationErr
from rest_framework import serializers
from store.models import *
from snipet.models import *
from order.models import *
# serializers.py
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(username=clean_data['username'], password=clean_data['password'])
		user_obj.username = clean_data['username']
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['username'], password=clean_data['password'])
		if not user:
			raise ValidationError({'error': 'User not found'}, code=status.HTTP_404_NOT_FOUND)
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'username')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class UserProSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = user_pro
        fields = ('first_name', 'last_name', 'phone', 'address')

class WalletSerializer(serializers.Serializer):
    def to_representation(self, instance):
        user_id = self.validated_data.get('user_id', None)

        approved_amount = self.validated_data.get('approved_amount', 0)
        cancel_amount = self.validated_data.get('cancel_amount', 0)
        wallet_balance = approved_amount - cancel_amount
        
        return {'wallet_balance': wallet_balance}

class UserProSerializers(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    first_name_initial = serializers.SerializerMethodField()

    class Meta:
        model = user_pro
        fields = ['full_name', 'first_name_initial', 'phone', 'address', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return f"{obj.full_name} "

    def get_first_name_initial(self, obj):
        return obj.full_name[0] if obj.full_name else ''
    
    

class ShipformedesSerializer(serializers.ModelSerializer):
    class Meta:
        model = shipformedes
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class descriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = description
        fields = '__all__'

class reviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = reviews
        fields = '__all__'

class shipformemesssagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = shipformemesssages
        fields = '__all__'

class shipformechargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = shipformecharge
        fields = '__all__'
        
        
class SiteIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Site_Identity
        fields = '__all__'
        
class HomeBanneerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home_Banneer
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Check if the 'image' field exists in the representation
        if 'image' in representation:
            # Prepend the base URL to the 'image' field
            representation['image'] = f'https://backend.ecargo.com.bd{representation["image"]}'
        
        return representation
        
class Hometop600pxBanneerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home_top600px_Banneer
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Check if the 'image' field exists in the representation
        if 'image' in representation:
            # Prepend the base URL to the 'image' field
            representation['image'] = f'https://backend.ecargo.com.bd{representation["image"]}'
        
        return representation
        
class Homemiddel502x202pxBanneerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home_middel502x202px_Banneer
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Check if the 'image' field exists in the representation
        if 'image' in representation:
            # Prepend the base URL to the 'image' field
            representation['image'] = f'https://backend.ecargo.com.bd{representation["image"]}'
        
        return representation
        
class Homemiddel680x180pxBanneerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home_middel680x180px_Banneer
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Check if the 'image' field exists in the representation
        if 'image' in representation:
            # Prepend the base URL to the 'image' field
            representation['image'] = f'https://backend.ecargo.com.bd{representation["image"]}'
        
        return representation
        
class Hom4databreadcumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home_4data_breadcum
        fields = '__all__'
        

class SubCatagorysListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCatagorysList
        fields = '__all__'

class CatagorysListSerializer(serializers.ModelSerializer):
    subcategories = SubCatagorysListSerializer(many=True, read_only=True)

    class Meta:
        model = CatagorysList
        fields = [ 'CategorName',]


class HomeslidingsellingtextBanneerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home_sliding_selling_text_Banneer
        fields = '__all__'
        
class CatagorysListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatagorysList
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Check if the 'image' field exists in the representation
        if 'image' in representation:
            # Prepend the base URL to the 'image' field
            representation['image'] = f'https://backend.ecargo.com.bd{representation["image"]}'
        
        return representation
        
class FooterWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterWidget
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Check if the 'image' field exists in the representation
        if 'logo' in representation:
            # Prepend the base URL to the 'image' field
            representation['image'] = f'https://backend.ecargo.com.bd{representation["logo"]}'
        
        return representation
        
class FooterLinksializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLinks
        fields = '__all__'
        
class FooterPaymentSuportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterPaymentSuportImage
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Check if the 'image' field exists in the representation
        if 'logo' in representation:
            # Prepend the base URL to the 'image' field
            representation['image'] = f'https://backend.ecargo.com.bd{representation["logo"]}'
        
        return representation
        
class SubCatagorysListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCatagorysList
        fields = '__all__'

class CatagorysListsSerializer(serializers.ModelSerializer):
    subcatagoryslist_set = SubCatagorysListSerializer(many=True, read_only=True)

    class Meta:
        model = CatagorysList
        fields = ['name', 'subcatagoryslist_set']
        
        
class HomebottomsitesBanneerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home_bottom_sites_Banneer
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Check if the 'image' field exists in the representation
        if 'image' in representation:
            # Prepend the base URL to the 'image' field
            representation['image'] = f'https://backend.ecargo.com.bd{representation["image"]}'
        
        return representation

class OrerPrductSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')  # Convert to human-readable representation
    product = ProductSerializer()
    class Meta:
        model = OrerPrduct
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = user_pro
        fields = ('full_name', 'phone', 'address')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"




class skucolorSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = skucolor
     
class skusizeSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = skusize
        fields = ('product','size')
     
class OrderProductSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = OrerPrduct
        fields = '__all__'
     
class REQOrderProductSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = req
        fields = '__all__'
     
class ReqOrderPartialPaymentSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = Req_Order_Partial_Payment
        fields = '__all__'
     

class ReqOrderSerializer(serializers.Serializer):
    permission_classes = [IsAuthenticated]
    reqo = serializers.SerializerMethodField()
    recount = serializers.IntegerField()
    unpaid = serializers.IntegerField()
    rq = serializers.IntegerField()
    totalamount = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    


    def get_reqo(self, obj):
        reqo = self.context['reqo']
        # Customize this based on your actual req model structure
        serialized_reqo = []

        # Assuming you have a list of req instances, you can iterate through them
        for req_obj in reqo:  # Replace 'req_objects' with your actual list of req instances
            serialized_reqo.append({
                'order_id': req_obj.order_id,
                'link': req_obj.link,
                'title': req_obj.title,
                'quantity': req_obj.quantity,
                'weight_charge': str(req_obj.weight_charge),
                'total_weight': str(req_obj.total_weight),
                'internal_shipping_charge': str(req_obj.internal_shipping_charge),
                'total_weight_charge': str(req_obj.total_weight_charge),
                'a_id': req_obj.a_id,
                'tracking': req_obj.tracking,
                'message': req_obj.message,
                'status': req_obj.status,
                'price': req_obj.price,
                't_m': req_obj.t_m,
                't_id': req_obj.t_id,
                'price_details': req_obj.price_details,
                'created_at': req_obj.created_at,
                'updated_at': req_obj.updated_at,
                'ps_status': req_obj.ps_status,
                # Add other fields here
            })

        return serialized_reqo


class ShippingSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]


    class Meta:
        model = Shipping
        fields = '__all__'


class SRequestDeliverySerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]


    class Meta:
        model = SRequest_Delivery
        fields = '__all__'


class ORequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ORequest_Delivery
        fields = '__all__'

class RRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RRequest_Delivery
        fields = '__all__'

class SRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SRequest_Delivery
        fields = '__all__'

class SticketSerializer(serializers.ModelSerializer):
    class Meta:
        model = sticket
        fields = '__all__'

class SmstSerializer(serializers.ModelSerializer):
    class Meta:
        model = smst
        fields = '__all__'

class walleatSerializer(serializers.ModelSerializer):
    class Meta:
        model = wallet
        fields = '__all__'

class FaqpageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq_page
        fields = '__all__'

class shippingrefundpageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping_refund_Pollicy_page
        fields = '__all__'

class aboustuspageSerializer(serializers.ModelSerializer):
    class Meta:
        model = aboustuspage
        fields = '__all__'

class PaymentnumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_numbers
        fields = '__all__'

class GoogleTagManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Google_Tag_Manager
        fields = '__all__'

class aboustuspageSerializer(serializers.ModelSerializer):
    class Meta:
        model = aboustuspage
        fields = '__all__'

class termsconditionpageSerializer(serializers.ModelSerializer):
    class Meta:
        model = terms_condition_page
        fields = '__all__'

class forbidenitempagenpageSerializer(serializers.ModelSerializer):
    class Meta:
        model = forbidenitempagen_page
        fields = '__all__'
        
class CombinedRequestSerializer(serializers.Serializer):
    o_requests = ORequestSerializer(many=True)
    r_requests = RRequestSerializer(many=True)
    s_requests = SRequestSerializer(many=True)
    total_requests = serializers.IntegerField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'o_requests': data['o_requests'],
            'r_requests': data['r_requests'],
            's_requests': data['s_requests'],
            'total_requests': data['total_requests']
        }

    
    
    
    
class payformeSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]


    class Meta:
        model = payforme
        fields = '__all__'

class RRequestDeliverySerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]


    class Meta:
        model = RRequest_Delivery
        fields = '__all__'

class PaysformePayNowReqSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]


    class Meta:
        model = payforme
        fields = ('p_total','t_m','t_id','t_img')

        
        
class PaymentOrderSerializer(serializers.Serializer):
    paymentorder = payformeSerializer(many=True)
    total_orders = serializers.IntegerField()
    unpaid_orders = serializers.IntegerField()
    partial_payment_received_orders = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=19, decimal_places=2, required=False)
        
        
class ShippingOrderSerializer(serializers.Serializer):
    shipping_orders = ShippingSerializer(many=True)
    total_orders = serializers.IntegerField()
    unpaid_orders = serializers.IntegerField()
    partial_payment_received_orders = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=19, decimal_places=2, required=False)

class Order_Partial_PaymentSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = Order_Partial_Payment
        fields = '__all__'

class ORequestDeliverySerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = ORequest_Delivery
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = orderss
        fields = '__all__'

class TotalOrderProductSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()

    def to_representation(self, instance):
        return {'total_orders': instance}