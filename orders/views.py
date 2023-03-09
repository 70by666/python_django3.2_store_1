from django.views.generic import CreateView
from django.urls import reverse_lazy

from orders.forms import OrderForm

from common.views import CommonContextMixin


class OrderCreateView(CommonContextMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:create')
    title = 'Store - Оформление заказа'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)
