
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=100, default='', verbose_name='заголовок')
    slug = models.CharField(max_length=100, default='', verbose_name='slug')
    post_content = models.TextField(**NULLABLE, verbose_name='содержимое')
    image = models.ImageField(upload_to='posts/', verbose_name='изображение', **NULLABLE)
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    publication_sign = models.BooleanField(default=True, verbose_name='признак публикации')
    count_of_views = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель')

    def __str__(self):
        return f'Название поста: {self.title}, Дата создания: {self.date_of_create} Автор: {self.owner}'

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
