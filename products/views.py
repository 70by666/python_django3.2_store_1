from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from products.models import ProductCategory, Product, Basket


class IndexView(TemplateView):
    template_name = 'products/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Store'
        
        return context


def products(request, category_id=None, page_num=1):
    products = Product.objects.filter(category=category_id) if category_id else Product.objects.all()
    paginator = Paginator(object_list=products, per_page=3)
    products_paginator = paginator.page(page_num)
    context = {
        'title': 'Store - Каталог', 
        'categories': ProductCategory.objects.all(),
        'products': products_paginator,
    }
    
    return render(request, 'products/products.html', context=context)


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
