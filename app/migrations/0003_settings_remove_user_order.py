# Generated by Django 4.2 on 2023-05-13 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_user_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_ture', models.CharField(max_length=5)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='order',
        ),
    ]
