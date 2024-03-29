# Generated by Django 3.1.7 on 2022-06-26 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20220626_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicite',
            name='famille',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.famille'),
        ),
        migrations.AddField(
            model_name='publicite',
            name='marche',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.marche'),
        ),
        migrations.AddField(
            model_name='publicite',
            name='secteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.secteur'),
        ),
        migrations.AddField(
            model_name='publicite',
            name='segment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.segment'),
        ),
        migrations.AlterField(
            model_name='programme',
            name='fin',
            field=models.TimeField(default='20:27:43'),
        ),
        migrations.AlterField(
            model_name='programmeradio',
            name='fin',
            field=models.TimeField(default='20:27:43'),
        ),
        migrations.AlterField(
            model_name='publicite',
            name='fin',
            field=models.TimeField(default='20:27:43'),
        ),
        migrations.AlterField(
            model_name='publiciteradio',
            name='fin',
            field=models.TimeField(default='20:27:43'),
        ),
    ]
