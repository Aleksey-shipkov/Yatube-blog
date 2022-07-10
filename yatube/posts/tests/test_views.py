import shutil
import tempfile
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django import forms
from posts.models import Group, Post, Follow

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Alex')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.group2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='test-slug2',
            description='Тестовое описание 2',
        )

        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
            id=3,
            group=cls.group,
            image=cls.uploaded
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostPagesTests.user)
        cache.clear()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def post_show_correct_context(
            self, first_object):
        post_text = first_object.text
        post_group = first_object.group.slug
        post_author = first_object.author.username
        post_pk = first_object.pk
        post_image = first_object.image
        self.assertEqual(post_text, self.post.text)
        self.assertEqual(post_group, self.post.group.slug)
        self.assertEqual(post_author, self.post.author.username)
        self.assertEqual(post_pk, self.post.pk)
        self.assertEqual(post_image, self.post.image)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list', kwargs={'slug': 'test-slug'}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile', kwargs={'username': 'Alex'}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail', kwargs={'post_id': 3}
            ): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:post_edit', kwargs={'post_id': 3}
            ): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertIn(PostPagesTests.post, response.context['page_obj'])

    def test_group_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': 'test-slug'})
        )
        first_object = response.context.get('page_obj')[0]
        self.post_show_correct_context(first_object)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': 'Alex'})
        )
        first_object = response.context.get('page_obj')[0]
        self.post_show_correct_context(first_object)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id})
        )
        first_object = response.context.get('post')
        self.post_show_correct_context(first_object)

    def test_create_posts_page_show_correct_context(self):
        """Шаблон create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_posts_edit_page_show_correct_context(self):
        """Шаблон редактирования поста сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_in_wrong_group_context(self):
        """Проверка попадания поста в другую группу."""
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': 'test-slug2'})
        )
        first_object = response.context['page_obj']
        self.assertNotIn(self.post, first_object)


class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Alex')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост'
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_cache_index(self):
        """Тест кэширования страницы index.html"""
        first_state = self.authorized_client.get(reverse('posts:index'))
        post = Post.objects.get(pk=1)
        post.text = 'Измененный текст поста'
        post.save()
        second_state = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(first_state.content, second_state.content)
        cache.clear()
        third_state = self.authorized_client.get(reverse('posts:index'))
        self.assertNotEqual(first_state.content, third_state.content)


class Followtests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Alex')
        cls.user2 = User.objects.create_user(username='Petya')
        cls.user3 = User.objects.create_user(username='Vasya')
        cls.post = Post.objects.create(
            author=cls.user2,
            text='Тестовая пост'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        cache.clear()

    def test_follow_authorized_user(self):
        """Тестирование подписки на автора"""
        self.authorized_client.get(reverse(
            'posts:profile_follow', kwargs={'username': self.post.author}))
        author_following = Follow.objects.filter(
            user=self.user, author=self.post.author
        )
        self.assertTrue(author_following.exists())

    def test_unfollow_authorized_user(self):
        """Тестирование отписки от автора"""
        self.authorized_client.get(reverse(
            'posts:profile_follow', kwargs={'username': self.post.author}))
        self.authorized_client.get(reverse(
            'posts:profile_unfollow', kwargs={'username': self.post.author}))
        author_following = Follow.objects.filter(
            user=self.user, author=self.post.author
        )
        self.assertFalse(author_following.exists())

    def test_followed_post_right_user(self):
        """Проверка попадания поста на страницу подписки на авторов."""
        self.authorized_client.get(reverse(
            'posts:profile_follow', kwargs={'username': self.post.author}))
        response = self.authorized_client.get(reverse(
            'posts:follow_index')
        )
        follow_page = response.context['page_obj']
        self.assertIn(self.post, follow_page)

    def test_followed_post_wrong_user(self):
        """Проверка попадания поста на страницу подписки на авторов."""
        self.authorized_client.get(reverse(
            'posts:profile_follow', kwargs={'username': self.post.author}))
        self.authorized_client.force_login(self.user3)
        response = self.authorized_client.get(reverse(
            'posts:follow_index')
        )
        follow_page = response.context['page_obj']
        self.assertNotIn(self.post, follow_page)
