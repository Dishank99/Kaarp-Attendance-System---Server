# Generated by Django 3.1.2 on 2021-01-27 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210127_1924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kaarpuser',
            old_name='date_joined',
            new_name='datetime_of_request',
        ),
        migrations.AddField(
            model_name='kaarpuser',
            name='datetime_of_activation',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
