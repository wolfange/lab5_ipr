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

from discounts.models import Category, Favorite, Post, Vote

User = get_user_model()


class CategoryModelTest(TestCase):
    """Тесты для модели Category"""

    def test_category_creation(self):
        """Тест создания категории"""
        category = Category.objects.create(name='Еда')
        self.assertEqual(category.name, 'Еда')
        self.assertEqual(str(category), 'Еда')

    def test_category_unique_name(self):
        """Тест уникальности названия категории"""
        Category.objects.create(name='Еда')
        with self.assertRaises(Exception):
            Category.objects.create(name='Еда')


class PostModelTest(TestCase):
    """Тесты для модели Post"""

    def setUp(self):
        """Создание тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Еда')

    def test_post_creation(self):
        """Тест создания поста"""
        post = Post.objects.create(
            title='Тестовый пост',
            description='Описание тестового поста',
            place='Тестовое место',
            category=self.category,
            author=self.user
        )
        self.assertEqual(post.title, 'Тестовый пост')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.category, self.category)
        self.assertEqual(str(post), 'Тестовый пост')

    def test_post_rating_without_votes(self):
        """Тест рейтинга поста без голосов"""
        post = Post.objects.create(
            title='Тестовый пост',
            description='Описание',
            place='Место',
            category=self.category,
            author=self.user
        )
        self.assertEqual(post.rating, 0)

    def test_post_rating_with_votes(self):
        """Тест рейтинга поста с голосами"""
        post = Post.objects.create(
            title='Тестовый пост',
            description='Описание',
            place='Место',
            category=self.category,
            author=self.user
        )
        user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )
        
        Vote.objects.create(post=post, user=self.user, vote_type='up')
        Vote.objects.create(post=post, user=user2, vote_type='up')
        Vote.objects.create(post=post, user=User.objects.create_user(
            username='user3', password='testpass123'
        ), vote_type='down')
        
        self.assertEqual(post.rating, 1)


class VoteModelTest(TestCase):
    """Тесты для модели Vote"""

    def setUp(self):
        """Создание тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Еда')
        self.post = Post.objects.create(
            title='Тестовый пост',
            description='Описание',
            place='Место',
            category=self.category,
            author=self.user
        )

    def test_vote_creation(self):
        """Тест создания голоса"""
        vote = Vote.objects.create(
            post=self.post,
            user=self.user,
            vote_type='up'
        )
        self.assertEqual(vote.post, self.post)
        self.assertEqual(vote.user, self.user)
        self.assertEqual(vote.vote_type, 'up')

    def test_vote_unique_together(self):
        """Тест уникальности пары пользователь-пост"""
        Vote.objects.create(
            post=self.post,
            user=self.user,
            vote_type='up'
        )
        with self.assertRaises(Exception):
            Vote.objects.create(
                post=self.post,
                user=self.user,
                vote_type='down'
            )


class FavoriteModelTest(TestCase):
    """Тесты для модели Favorite"""

    def setUp(self):
        """Создание тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Еда')
        self.post = Post.objects.create(
            title='Тестовый пост',
            description='Описание',
            place='Место',
            category=self.category,
            author=self.user
        )

    def test_favorite_creation(self):
        """Тест создания избранного"""
        favorite = Favorite.objects.create(
            user=self.user,
            post=self.post
        )
        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.post, self.post)

    def test_favorite_unique_together(self):
        """Тест уникальности пары пользователь-пост в избранном"""
        Favorite.objects.create(
            user=self.user,
            post=self.post
        )
        with self.assertRaises(Exception):
            Favorite.objects.create(
                user=self.user,
                post=self.post
            )


class HomeViewTest(TestCase):
    """Тесты для представления главной страницы"""

    def setUp(self):
        """Создание тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Еда')
        self.post = Post.objects.create(
            title='Тестовый пост',
            description='Описание',
            place='Место',
            category=self.category,
            author=self.user
        )

    def test_home_view(self):
        """Тест главной страницы"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый пост')

    def test_home_view_with_category_filter(self):
        """Тест фильтрации по категории"""
        response = self.client.get(
            reverse('home') + f'?category={self.category.id}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый пост')

    def test_home_view_with_sort(self):
        """Тест сортировки"""
        response = self.client.get(reverse('home') + '?sort=rating')
        self.assertEqual(response.status_code, 200)


class CreatePostViewTest(TestCase):
    """Тесты для представления создания поста"""

    def setUp(self):
        """Создание тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Еда')
        self.client.login(username='testuser', password='testpass123')

    def test_create_post_get(self):
        """Тест GET запроса на страницу создания поста"""
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)

    def test_create_post_post_valid(self):
        """Тест POST запроса с валидными данными"""
        data = {
            'title': 'Новый пост',
            'description': 'Описание нового поста',
            'place': 'Новое место',
            'category': self.category.id,
        }
        response = self.client.post(reverse('create_post'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='Новый пост').exists())

    def test_create_post_requires_login(self):
        """Тест что создание поста требует авторизации"""
        self.client.logout()
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 302)


class VotePostViewTest(TestCase):
    """Тесты для представления голосования"""

    def setUp(self):
        """Создание тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Еда')
        self.post = Post.objects.create(
            title='Тестовый пост',
            description='Описание',
            place='Место',
            category=self.category,
            author=self.user
        )
        self.client.login(username='testuser', password='testpass123')

    def test_vote_post_up(self):
        """Тест голосования за пост"""
        response = self.client.post(
            reverse('vote_post', args=[self.post.id, 'up'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Vote.objects.filter(
                post=self.post,
                user=self.user,
                vote_type='up'
            ).exists()
        )

    def test_vote_post_requires_login(self):
        """Тест что голосование требует авторизации"""
        self.client.logout()
        response = self.client.post(
            reverse('vote_post', args=[self.post.id, 'up'])
        )
        self.assertEqual(response.status_code, 302)
