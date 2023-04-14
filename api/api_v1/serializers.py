from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('stripe_product_price_id',)


class ProductUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128, required=False)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)
    quantity = serializers.IntegerField(required=False)
    image = serializers.ImageField(required=False)
    
    class Meta:
        model = Product
        exclude = ('stripe_product_price_id',)
