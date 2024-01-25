from datetime import datetime

from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    email = models.EmailField(verbose_name='Почта', unique=True)
    comment = models.TextField(verbose_name='коментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель')

    def __str__(self):
        return f'Почта: {self.email} Фамилия: {self.last_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Newsletter(models.Model):
    # newsletter_list = Newsletter.objects.all()
    STATUS_TYPES = [
        ('start', 'Запущена'),
        ('finish', 'Завершена'),
        ('created', 'Создана')
    ]

    PERIOD_TYPES = [
        ('no', 'Нет'),
        ('once_a_day', 'Раз в день'),
        ('once_a_week', 'Раз в неделю'),
        ('once_a_month', 'Раз в месяц')
    ]

    head = models.CharField(max_length=150, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    time = models.DateTimeField(default=datetime.now(), verbose_name='Время рассылки')
    period = models.CharField(max_length=20, choices=PERIOD_TYPES, default='no', verbose_name='период')
    status = models.CharField(max_length=20, choices=STATUS_TYPES, default='created', verbose_name='статус')
    to_client = models.ForeignKey(Client, to_field='email', on_delete=models.CASCADE, verbose_name='кому '
                                                                                                   'отправлять')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель')
    is_active = models.BooleanField(default=True, verbose_name='активная рассылка')

    def __str__(self):
        return f'Создатель: {self.owner} {self.time} {self.to_client}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            (
                "set_is_active",
                "Can active newsletter"
            )
        ]


class Logs(models.Model):
    STATUS_ATTEMPT_TYPES = [
        ('make', 'Совершена'),
        ('dont_make', 'Не совершена'),
    ]

    date = models.DateTimeField(verbose_name='Время и дата последней попытки', auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_ATTEMPT_TYPES, default='Не совершена',
                              verbose_name='Статус')
    response = models.CharField(max_length=100, verbose_name='Ответ сервера', )
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, verbose_name='рассылка')

    def __str__(self):
        return f'{self.status}, {self.response}, {self.date}'

    class Meta:
        verbose_name = 'Логи'
        verbose_name_plural = 'Логи'
