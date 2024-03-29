# Generated by Django 5.0 on 2024-01-18 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0008_alter_schedule_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='time',
            field=models.TimeField(verbose_name='время начала'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='users',
            field=models.ManyToManyField(to='mailing.user', verbose_name='Пользователи'),
        ),
    ]
