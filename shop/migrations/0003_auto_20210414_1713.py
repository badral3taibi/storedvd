# Generated by Django 3.1.7 on 2021-04-14 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210414_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', max_length=40, verbose_name='Nickname'),
        ),
        migrations.AddField(
            model_name='section',
            name='slug',
            field=models.SlugField(default='', max_length=40, verbose_name='Nickname'),
        ),
    ]
