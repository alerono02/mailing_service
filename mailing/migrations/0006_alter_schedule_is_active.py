# Generated by Django 5.0 on 2024-01-13 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0005_schedule_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активна'),
        ),
    ]
