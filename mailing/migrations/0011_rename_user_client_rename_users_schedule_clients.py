# Generated by Django 5.0 on 2024-02-06 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0010_alter_schedule_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Client',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='users',
            new_name='clients',
        ),
    ]