from rest_framework import generics

from api.api_v1.serializers import ProductSerializer
from products.models import Product


class ProductsListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
