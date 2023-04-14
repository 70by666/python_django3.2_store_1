from rest_framework.viewsets import ModelViewSet

from api.api_v1.serializers import ProductSerializer
from products.models import Product


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
