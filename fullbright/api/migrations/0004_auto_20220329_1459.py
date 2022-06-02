# Generated by Django 3.1.7 on 2022-03-29 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_article_num_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jour',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='pub',
            name='langue',
            field=models.CharField(choices=[('fr', 'fr'), ('ar', 'ar'), ('AF', 'arabe + francais')], max_length=20),
        ),
        migrations.AlterField(
            model_name='publicite',
            name='language',
            field=models.CharField(choices=[('AR', 'arabe'), ('FR', 'francais'), ('AF', 'arabe + francais')], default='', max_length=2),
        ),
    ]
