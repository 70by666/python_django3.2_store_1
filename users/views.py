from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DetailView, TemplateView,
                                  UpdateView)

from common.views import CommonContextMixin, ReverseProfileMixin
from users.forms import LoginForm, ProfileForm, RegisterForm
from users.models import EmailVerification, User


class LoginView(ReverseProfileMixin, CommonContextMixin, LoginView):
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


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'{self.object.id} - {self.object}'
        
        return context


class ProfileEditView(ReverseProfileMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """
    Контроллер редактирования прфоиля
    """
    template_name = 'users/profile_edit.html'    
    form_class = ProfileForm
    model = User
    success_message = 'Профиль изменен!'

    def get_object(self, queryset=None):
        return self.request.user


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
