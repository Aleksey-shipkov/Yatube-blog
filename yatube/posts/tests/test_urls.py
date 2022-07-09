from http.client import NOT_FOUND, OK
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, Client
from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, OK)


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
            id=3
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(TaskURLTests.user)
        cache.clear()

    def test_urls_uses_correct_template_guest(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/posts/3/': 'posts/post_detail.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_uses_correct_template_authorized(self):
        templates_url_names_authorized = {
            '/create/': 'posts/create_post.html',
            '/posts/3/edit/': 'posts/create_post.html',
            '/profile/auth/': 'posts/profile.html',
        }
        for address, template in templates_url_names_authorized.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_guest_user(self):
        url_names = [
            '/',
            '/group/test-slug/',
            '/posts/3/',
        ]
        for address in url_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, OK)

    def test_urls_authorized_user(self):
        url_names_authorized = [
            '/create/',
            '/posts/3/edit/',
            '/profile/auth/',
        ]
        for address in url_names_authorized:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, OK)

    def test_urls_unexisting_page(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, NOT_FOUND)

    def test_create_post_url_redirect_anonymous_on_user_login(self):
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/create/'))

    def test_post_edit_url_redirect_anonymous_on_user_login(self):
        response = self.guest_client.get('/posts/3/edit/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/posts/3/edit/'))

    def test_add_comment_url_redirect_anonymous_on_user_login(self):
        response = self.guest_client.get('/posts/3/comment/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/posts/3/comment/'))
