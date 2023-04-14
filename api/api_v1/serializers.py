from rest_framework.serializers import ModelSerializer, ImageField

from products.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(ModelSerializer):
    image = ImageField(required=False)
    
    class Meta:
        model = Product
        exclude = ('stripe_product_price_id',)
