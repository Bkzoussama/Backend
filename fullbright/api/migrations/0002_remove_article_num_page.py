# Generated by Django 3.1.7 on 2022-03-19 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='num_page',
        ),
    ]
