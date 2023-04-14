from django.urls import include, path
from rest_framework import routers

from api.api_v1.views import ProductsViewSet, UsersViewSet

app_name = 'api_v1'

router = routers.DefaultRouter()
router.register('products', ProductsViewSet, basename='products')
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
