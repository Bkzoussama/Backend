# Generated by Django 3.1.7 on 2022-06-13 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20220613_1915'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jourradio',
            old_name='chaine',
            new_name='radio',
        ),
        migrations.AlterField(
            model_name='programme',
            name='fin',
            field=models.TimeField(default='19:29:58'),
        ),
        migrations.AlterField(
            model_name='programmeradio',
            name='fin',
            field=models.TimeField(default='19:29:58'),
        ),
        migrations.AlterField(
            model_name='publicite',
            name='fin',
            field=models.TimeField(default='19:29:58'),
        ),
        migrations.AlterField(
            model_name='publiciteradio',
            name='fin',
            field=models.TimeField(default='19:29:58'),
        ),
    ]
