# Generated by Django 5.0 on 2023-12-30 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_alter_mailinglog_options_alter_schedule_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
    ]
