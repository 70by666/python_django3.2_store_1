from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

from users.views import LoginView, RegisterView, ProfileView, EmailVerificationView


app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', login_required(ProfileView.as_view()), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='emailverification'),
]
