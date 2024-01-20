from datetime import datetime

from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    email = models.EmailField(verbose_name='Почта')
    comment = models.TextField(verbose_name='коментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель')

    def __str__(self):
        return f'{self.email} {self.last_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Newsletter(models.Model):
    STATUS_TYPES = [
        ('start', 'Запущена'),
        ('finish', 'Завершена'),
        ('created', 'Создана')
    ]

    PERIOD_TYPES = [
        ('once_a_day', 'Раз в день'),
        ('once_a_week', 'Раз в неделю'),
        ('once_a_month', 'Раз в месяц')
    ]

    time = models.DateTimeField(default=datetime.now(), verbose_name='Время рассылки')
    period = models.CharField(max_length=20, choices=PERIOD_TYPES, default='once_a_day', verbose_name='период')
    status = models.CharField(max_length=20, choices=STATUS_TYPES, default='created', verbose_name='статус')
    to_client = models.ForeignKey(Client, to_field=Client.email, on_delete=models.CASCADE, verbose_name='кому '
                                                                                                        'отправлять')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель')

    def __str__(self):
        return f'{self.owner} {self.time} {self.time}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    head = models.CharField(max_length=150, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, verbose_name='расслыка')

    def __str__(self):
        return f'{self.head}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


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
