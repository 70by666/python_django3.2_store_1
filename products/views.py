from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from products.models import ProductCategory, Product, Basket


def index(request):
    context = {
        'title': 'Store',
    }    
    
    return render(request, 'products/index.html', context=context)


def products(request):
    context = {
        'title': 'Store - Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all()
    }   
    
    return render(request, 'products/products.html', context=context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)
    print(type(request.user), type(request.user.id))
    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        bsk = basket.first()
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
