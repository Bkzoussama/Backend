# Generated by Django 3.1.7 on 2022-06-06 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_remove_publicite_fin'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicite',
            name='fin',
            field=models.TimeField(default='15:12:52'),
        ),
    ]