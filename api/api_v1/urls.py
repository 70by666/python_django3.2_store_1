from django.urls import path, include
from rest_framework import routers

from api.api_v1.views import ProductsViewSet 

app_name = 'api_v1'

router = routers.SimpleRouter()
router.register('products', ProductsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
