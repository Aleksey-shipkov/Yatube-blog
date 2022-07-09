import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Group, Post, Comment

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsCreateTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Alex')
        cls.group = Group.objects.create(
            title='Тестовая группа 2',
            slug='test-slug2',
            description='Тестовое описание 2',
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create_forms(self):
        post_count = Post.objects.count()

        form_data = {
            'text': 'Тестовый пост пост',
            'group': self.group.pk,
            'image': self.uploaded,
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'), data=form_data, follow=True)
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'Alex'}))
        self.assertTrue(
            Post.objects.filter(
                group=self.group.pk,
                text='Тестовый пост пост',
                image='posts/small.gif'
            ).exists())

    def test_post_edit_forms(self):
        """Проверка формы редактирования записи в БД>."""
        small_gif2 = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded2 = SimpleUploadedFile(
            name='small2.gif',
            content=small_gif2,
            content_type='image/gif'
        )

        post = Post.objects.create(
            author=self.user,
            text='Тестовая пост1',
            group=self.group,
            image=self.uploaded,
        )
        posts_count = Post.objects.count()
        form_data = {
            'group': self.group.pk,
            'text': 'Измененные текста на пост пост текст',
            'image': uploaded2
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post.id}),
            data=form_data,
            follow=True,)
        print(post.image)
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': post.id}))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                group=self.group.pk,
                text='Измененные текста на пост пост текст',
                image='posts/small2.gif',
            ).exists())

    def test_add_comment_form_authorized(self):
        post = Post.objects.create(
            author=self.user,
            text='Тестовая пост1',
            group=self.group,
        )
        form = {'text': 'Тестовый комментарий'}
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': post.id}),
            data=form,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': post.id}))
        self.assertTrue(Comment.objects.filter(
            post=post,
            text='Тестовый комментарий',
        ).exists())
