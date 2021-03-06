# Generated by Django 3.1.2 on 2021-01-28 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_of_creation', models.DateTimeField(auto_now_add=True)),
                ('datetime_of_updation', models.DateTimeField(auto_now=True)),
                ('location_latitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('location_longitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('location_timestamp', models.PositiveIntegerField()),
                ('location_string', models.CharField(blank=True, max_length=150, null=True)),
                ('is_present', models.BooleanField(default=False)),
                ('validity_data', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
