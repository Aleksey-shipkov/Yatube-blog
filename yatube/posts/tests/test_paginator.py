from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from yatube.settings import PAGE_SIZE
from posts.models import Group, Post

User = get_user_model()

POST_NUMBERS = 12
SECOND_PAGE_POST_NUMBER = POST_NUMBERS - PAGE_SIZE


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Alex')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        for post in range(0, POST_NUMBERS):
            cls.post = Post.objects.create(
                author=cls.user,
                text=f'Тестовая пост {post}',
                group=cls.group
            )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorViewsTest.user)

    def test_first_page_contains_ten_records(self):
        object_dict_page_1 = {
            self.authorized_client.get(reverse(
                'posts:group_list', kwargs={'slug': 'test-slug'})): PAGE_SIZE,
            self.authorized_client.get(reverse('posts:index')): PAGE_SIZE,
            self.authorized_client.get(reverse(
                'posts:profile', kwargs={'username': 'Alex'})): PAGE_SIZE
        }
        for response, post_number in object_dict_page_1.items():
            with self.subTest(response=response):
                self.assertEqual(
                    len(response.context['page_obj']), post_number)

    def test_second_page_contains_two_records(self):
        object_dict_page_2 = {
            self.authorized_client.get(reverse(
                'posts:group_list', kwargs={'slug': 'test-slug'})
                + '?page=2'): 2,
            self.authorized_client.get(
                reverse('posts:index') + '?page=2'): SECOND_PAGE_POST_NUMBER,
            self.authorized_client.get(reverse(
                'posts:profile', kwargs={
                    'username': 'Alex'}) + '?page=2'): SECOND_PAGE_POST_NUMBER
        }
        for response, post_number in object_dict_page_2.items():
            with self.subTest(response=response):
                self.assertEqual(
                    len(response.context['page_obj']), post_number)
