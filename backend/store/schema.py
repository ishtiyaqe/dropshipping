# schema.py
import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from .models import Product, ProductImage, ProductDes, skucolor, skusize, Catagorys

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filter_fields = {
            'product_no': ['exact', 'icontains', 'istartswith'],
            'name': ['exact', 'icontains', 'istartswith'],
            'link': ['exact', 'icontains', 'istartswith'],
            'price': ['exact'],
        }
        interfaces = (relay.Node,)

class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage
        filter_fields = {
            'product__id': ['exact'],
            'image': ['exact'],
            'caption': ['exact', 'icontains'],
        }
        interfaces = (relay.Node,)


class ProductDesType(DjangoObjectType):
    class Meta:
        model = ProductDes
        filter_fields = {
            'product__id': ['exact'],
            'shortdes': ['exact', 'icontains'],
            'fulldes': ['exact', 'icontains'],
        }
        interfaces = (relay.Node,)


class SkuColorType(DjangoObjectType):
    class Meta:
        model = skucolor
        filter_fields = {
            'product__id': ['exact'],
            'color': ['exact', 'icontains'],
        }
        interfaces = (relay.Node,)


class SkuSizeType(DjangoObjectType):
    class Meta:
        model = skusize
        filter_fields = {
            'product__id': ['exact'],
            'color': ['exact', 'icontains'],
            'size': ['exact', 'icontains'],
        }
        interfaces = (relay.Node,)


class CategoryType(DjangoObjectType):
    class Meta:
        model = Catagorys
        filter_fields = {
            'product__id': ['exact'],
            'catagory': ['exact', 'icontains'],
        }
        interfaces = (relay.Node,)


# Define a query class
class Query(graphene.ObjectType):
    all_products = DjangoFilterConnectionField(ProductType)
    all_product_images = DjangoFilterConnectionField(ProductImageType)
    all_product_descriptions = DjangoFilterConnectionField(ProductDesType)
    all_sku_colors = DjangoFilterConnectionField(SkuColorType)
    all_sku_sizes = DjangoFilterConnectionField(SkuSizeType)
    all_categories = DjangoFilterConnectionField(CategoryType)

    # You can also define custom queries if needed
    product_by_id = graphene.Field(ProductType, id=graphene.Int())

    def resolve_product_by_id(self, info, id):
        return Product.objects.get(pk=id)

# Define your GraphQL schema
schema = graphene.Schema(query=Query)
