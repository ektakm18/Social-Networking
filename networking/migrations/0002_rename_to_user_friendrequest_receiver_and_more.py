# Generated by Django 5.0.6 on 2024-06-17 08:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networking', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendrequest',
            old_name='to_user',
            new_name='receiver',
        ),
        migrations.RenameField(
            model_name='friendrequest',
            old_name='from_user',
            new_name='sender',
        ),
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together={('sender', 'receiver')},
        ),
    ]
