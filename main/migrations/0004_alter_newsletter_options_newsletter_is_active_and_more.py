# Generated by Django 4.2.7 on 2024-01-21 15:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_client_email_alter_newsletter_period_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'permissions': [('set_is_active', 'Can active newsletter')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
        migrations.AddField(
            model_name='newsletter',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активная рассылка'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 21, 20, 8, 43, 398329), verbose_name='Время рассылки'),
        ),
    ]
