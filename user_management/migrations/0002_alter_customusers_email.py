# Generated by Django 5.0.6 on 2024-07-02 07:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusers',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator(message='Invalid email format.')], verbose_name='email'),
        ),
    ]