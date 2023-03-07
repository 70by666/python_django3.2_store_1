from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from users.models import User, EmailVerification
from users.forms import LoginForm, RegisterForm, ProfileForm
from products.models import Basket
from common.views import CommonContextMixin


class LoginView(CommonContextMixin, LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    title = 'Store - Авторизация'


class RegisterView(CommonContextMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Регистрация прошла успешно!'
    title = 'Store - Регистрация'


class ProfileView(CommonContextMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Store - Профиль'
    
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket'] = Basket.objects.filter(user=self.object)
        
        return context


class EmailVerificationView(CommonContextMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - Подтверждение электронной почты'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        emailverifications = EmailVerification.objects.filter(user=user,
                                                              code=code)
        if emailverifications.exists() and emailverifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
