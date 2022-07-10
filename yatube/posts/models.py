from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='Название',
        help_text='Пожалуйста, добавьте название')
    slug = models.SlugField(unique=True)
    description = models.TextField(
        verbose_name='Описание',
        help_text='Пожалуйста, добавьте описание')

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст',
        help_text='Пожалуйста, напишите текст поста')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Введите дату публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts', verbose_name='Автор',
        help_text='Пожалуйста, укажите автора'
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts', verbose_name='Группа',
        help_text='Пожалуйста, укажите группу'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True,
        null=True,
        related_name='comments', verbose_name='Пост'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments', verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Пожалуйста, напишите комментарий')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время')

    def __str__(self) -> str:
        return self.text[:30]


class Follow(models.Model):
    user = models.ForeignKey(
        User, related_name='follower', on_delete=models.CASCADE, blank=True,
        null=True, verbose_name='Подписчик', help_text='Указать подписчика')
    author = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE, blank=True,
        null=True, verbose_name='Автор', help_text='Подписаться на автора')

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'), name='unique_following'))

    def __str__(self) -> str:
        return f'{self.user.username} подписан на {self.author.username}'
