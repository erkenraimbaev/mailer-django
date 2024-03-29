# Generated by Django 4.2.7 on 2024-01-21 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100, verbose_name='заголовок')),
                ('slug', models.CharField(default='', max_length=100, verbose_name='slug')),
                ('post_content', models.TextField(blank=True, null=True, verbose_name='содержимое')),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='изображение')),
                ('date_of_create', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('publication_sign', models.BooleanField(default=True, verbose_name='признак публикации')),
                ('count_of_views', models.PositiveIntegerField(default=0, verbose_name='количество просмотров')),
            ],
            options={
                'verbose_name': 'пост',
                'verbose_name_plural': 'посты',
            },
        ),
    ]
