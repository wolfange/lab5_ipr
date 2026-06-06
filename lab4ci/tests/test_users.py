import os
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sales_Aggregator.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Тесты для модели CustomUser"""

    def test_user_creation(self):
        """Тест создания пользователя"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_str_representation(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(str(user), 'testuser')


class RegisterViewTest(TestCase):
    """Тесты для представления регистрации"""

    def test_register_get(self):
        """Тест GET запроса на страницу регистрации"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_register_post_valid(self):
        """Тест POST запроса с валидными данными"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_post_invalid(self):
        """Тест POST запроса с невалидными данными"""
        data = {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'differentpass',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())


class LoginViewTest(TestCase):
    """Тесты для представления входа"""

    def setUp(self):
        """Создание тестового пользователя"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_login_get(self):
        """Тест GET запроса на страницу входа"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_login_post_valid(self):
        """Тест POST запроса с валидными данными"""
        data = {
            'username': 'testuser',
            'password': 'testpass123',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)

    def test_login_post_invalid(self):
        """Тест POST запроса с невалидными данными"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)


class LogoutViewTest(TestCase):
    """Тесты для представления выхода"""

    def setUp(self):
        """Создание и вход тестового пользователя"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_logout(self):
        """Тест выхода из системы"""
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.client.session.get('_auth_user_id'))