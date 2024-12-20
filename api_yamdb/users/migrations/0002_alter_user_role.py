# Generated by Django 3.2 on 2024-06-21 03:39

from django.db import migrations, models
import users.enums


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[(users.enums.UserRoles['user'], 'Пользователь'), (users.enums.UserRoles['moderator'], 'Модератор'), (users.enums.UserRoles['admin'], 'Администратор')], default='user', max_length=20, verbose_name='Роль пользователя'),
        ),
    ]
