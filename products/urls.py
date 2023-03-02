from django.urls import path

from products.views import products, basket_add, basket_remove, basket_remove_one_item


app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:category_id>/', products, name='category'),
    path('page/<int:page_num>', products, name='paginator'),
    path('basket/add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('basket/remove_one_item/<int:product_id>/', basket_remove_one_item, name='basket_remove_one_item'),
]
