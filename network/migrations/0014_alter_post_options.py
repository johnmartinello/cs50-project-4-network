# Generated by Django 4.1.5 on 2023-03-20 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0013_remove_user_followed_users_user_follower_users'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-timestamp']},
        ),
    ]
