from django.urls import path

from api.api_v1.views import ProductsListAPIView

app_name = 'api_v1'

urlpatterns = [
    path('products/list', ProductsListAPIView.as_view(), name='index'),
]
