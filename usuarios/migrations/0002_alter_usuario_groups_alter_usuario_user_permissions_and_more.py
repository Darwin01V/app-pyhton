# Generated by Django 5.0 on 2024-03-29 04:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(related_name='usuarios', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(related_name='usuarios', to='auth.permission'),
        ),
        migrations.CreateModel(
            name='Sesiones',
            fields=[
                ('rideID', models.AutoField(primary_key=True, serialize=False)),
                ('xml', models.TextField()),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]