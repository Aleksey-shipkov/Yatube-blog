from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост'
        )

    def test_post_model_have_correct_object_names(self):
        """Проверяем, что у модели корректно работает __str__."""
        post = PostModelTest.post
        self.assertEqual(str(post), post.text)

    def test_post_verbose_name(self):
        post = self.post
        fields_verboses = {
            'text': 'Текст',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа'
        }
        for field, value in fields_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, value)

    def test_post_help_text(self):
        post = self.post
        fields_help_text = {
            'text': 'Пожалуйста, напишите текст поста',
            'pub_date': 'Введите дату публикации',
            'author': 'Пожалуйста, укажите автора',
            'group': 'Пожалуйста, укажите группу'
        }
        for field, value in fields_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, value)


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_group_model_have_correct_object_names(self):
        """Проверяем, что у модели корректно работает __str__."""
        group = GroupModelTest.group
        self.assertEqual(str(group), group.title)

    def test_group_verbose_name(self):
        group = self.group
        fields_verboses = {
            'title': 'Название',
            'description': 'Описание'
        }
        for field, value in fields_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, value)

    def test_groupt_help_text(self):
        group = self.group
        fields_help_text = {
            'title': 'Пожалуйста, добавьте название',
            'description': 'Пожалуйста, добавьте описание'
        }
        for field, value in fields_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text, value)
