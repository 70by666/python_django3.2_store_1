from django.urls import path

from products.views import (ProductsListView, basket_add, basket_remove,
                            basket_remove_one_item)

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('basket/add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('basket/remove_one_item/<int:product_id>/', basket_remove_one_item, name='basket_remove_one_item'),
]
