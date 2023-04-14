from django.urls import path

from api.api_v1.views import ProductsListCreateAPIView

app_name = 'api_v1'

urlpatterns = [
    path('products/', ProductsListCreateAPIView.as_view()),
]
