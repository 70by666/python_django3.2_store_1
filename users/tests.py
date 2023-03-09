from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class RegisterViewTest(TestCase):
    def setUp(self):
        self.path = reverse('users:register')
        self.data = {
            'first_name': 123, 'last_name': 123, 'username': 666,
            'email': '666@666.666', 'password1': 'testpassword', 
            'password2': 'testpassword'
        }
        self.username = self.data['username']
    
    def test_user_register_get(self):
        response = self.client.get(self.path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_register_post_success(self):
        self.assertFalse(User.objects.filter(username=self.username).exists())
        
        response = self.client.post(self.path, self.data)
        
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=self.username).exists())
        
        emailverify = EmailVerification.objects.filter(user__username=self.username)
        self.assertTrue(emailverify.exists())
        self.assertEqual(
            emailverify.first().expiration.date(),
            (now() + timedelta(hours=24)).date()
        )
        
    def test_user_register_post_error(self):
        User.objects.create(username=self.username)
        response = self.client.post(self.path, self.data)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, 
            'Пользователь с таким именем уже существует.',
            html=True
        )
