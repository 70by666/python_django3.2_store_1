from rest_framework.generics import ListCreateAPIView

from api.api_v1.serializers import ProductSerializer, ProductCreateSerializer
from products.models import Product


class ProductsListCreateAPIView(ListCreateAPIView):
    """
    GET Возвращает все продукты
    POST Cоздает новый продукт
    """
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        self.serializer_class = ProductSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = ProductCreateSerializer
        return self.create(request, *args, **kwargs)
