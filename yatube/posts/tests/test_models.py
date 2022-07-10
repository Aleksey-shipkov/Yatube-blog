from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post, Comment, Follow

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


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост'
        )
        cls.comment = Comment.objects.create(
            post=cls.post, text="Тестовый комментарий", author=cls.user
        )

    def test_comment_model_have_correct_object_names(self):
        """Проверяем, что у модели корректно работает __str__."""
        comment = self.comment
        self.assertEqual(str(comment), comment.text)

    def test_comment_verbose_name(self):
        comment = self.comment
        fields_verboses = {
            'post': 'Пост',
            'author': 'Автор',
            'text': 'Текст комментария',
            'created': 'Дата и время',
        }
        for field, value in fields_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).verbose_name, value)

    def test_comment_help_text(self):
        comment = self.comment
        fields_help_text = {
            'text': 'Пожалуйста, напишите комментарий',
        }
        for field, value in fields_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).help_text, value)


class FollowModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.user2 = User.objects.create_user(username='auth2')
        cls.post = Post.objects.create(
            author=cls.user2,
            text='Тестовая пост'
        )
        cls.follow = Follow.objects.create(user=cls.user, author=cls.user2)

    def test_follow_model_have_correct_object_names(self):
        """Проверяем, что у модели корректно работает __str__."""

        # self.assertEqual(str(group), group.title)
        self.assertEqual(
            str(self.follow),
            f'{self.user.username} подписан на {self.post.author.username}'
        )

    def test_follow_verbose_name(self):
        follow = Follow.objects.get(user=self.user, author=self.user2)
        fields_verboses = {
            'user': 'Подписчик',
            'author': 'Автор',
        }
        for field, value in fields_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    follow._meta.get_field(field).verbose_name, value)

    def test_follow_help_text(self):
        follow = Follow.objects.get(user=self.user, author=self.user2)
        fields_help_text = {
            'user': 'Указать подписчика',
            'author': 'Подписаться на автора',
        }
        for field, value in fields_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    follow._meta.get_field(field).help_text, value)
