# Generated by Django 4.2.4 on 2023-08-10 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sign',
            field=models.CharField(default='这人很懒，什么也没留下', max_length=100),
        ),
    ]
