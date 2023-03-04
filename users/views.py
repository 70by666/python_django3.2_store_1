from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView

from users.models import User
from users.forms import LoginForm, RegisterForm, ProfileForm
from products.models import Basket


class LoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm


# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('users:profile', args=(request.user.id,)))
#     else:
#         form = LoginForm()
        
#     context = {'form': form}
    
#     return render(request, 'users/login.html', context)


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store - Регистрация'
        
        return context
    

# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Регистрация прошла успешно!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegisterForm()
        
#     context = {'form': form}
    
#     return render(request, 'users/register.html', context)


class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store - Профиль'
        context['basket'] = Basket.objects.filter(user=self.object)
        
        return context
    
    
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(instance=request.user, 
#                                data=request.POST, 
#                                files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = ProfileForm(instance=request.user)
    
#     context = {
#         'title': 'Store - Профиль', 
#         'form': form,
#         'basket': Basket.objects.filter(user=request.user),
#     }
    
#     return render(request, 'users/profile.html', context)


# def logout(request):
#     auth.logout(request)
    
#     return HttpResponseRedirect(reverse('index'))
