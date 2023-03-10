from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from common.views import CommonContextMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(CommonContextMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CancelTemplateView(CommonContextMixin, TemplateView):
    template_name = 'orders/cancel.html'


class OrderListView(CommonContextMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = ('-id')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'Заказ №{self.object.id}'
        
        return context
    

class OrderCreateView(CommonContextMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:create')
    title = 'Store - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)
        
        basket = Basket.objects.filter(user=self.request.user)   
        checkout_session = stripe.checkout.Session.create(
            line_items=basket.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url=f'{settings.DOMAIN_NAME}{reverse("orders:success")}',
            cancel_url=f'{settings.DOMAIN_NAME}{reverse("orders:cancel")}',
        )
        
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)
    
    def form_valid(self, form):
        form.instance.initiator = self.request.user
        
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
