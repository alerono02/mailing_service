# Generated by Django 4.2.7 on 2024-02-09 17:24

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=50, null=True),
        ),
    ]
