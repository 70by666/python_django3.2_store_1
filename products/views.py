from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView

from products.models import ProductCategory, Product, Basket


class IndexView(TemplateView):
    template_name = 'products/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store'
        
        return context


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        
        return queryset.filter(category_id=category_id) if category_id else queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store - Каталог'
        context['categories'] = ProductCategory.objects.all()
        
        return context


@login_required
def basket_add(request, product_id):
    basket = Basket.objects.filter(user=request.user, product_id=product_id)
    if not basket.exists():
        Basket.objects.create(user=request.user, product_id=product_id, quantity=1)
    else:
        bsk = basket[0]
        bsk.quantity += 1
        bsk.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove_one_item(request, product_id):
    basket = Basket.objects.get(user=request.user, product_id=product_id)
    if basket.quantity == 1:
        basket.delete()
    else:
        basket.quantity -= 1
        basket.save()
        
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
