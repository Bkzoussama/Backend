# Generated by Django 3.1.7 on 2022-06-07 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20220606_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='fin',
            field=models.TimeField(default='18:54:50'),
        ),
        migrations.AlterField(
            model_name='publicite',
            name='fin',
            field=models.TimeField(default='18:54:50'),
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=100, unique=True)),
                ('NomAnnonceur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.annonceur')),
            ],
        ),
        migrations.CreateModel(
            name='Secteur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=100, unique=True)),
                ('NomAnnonceur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.annonceur')),
            ],
        ),
        migrations.CreateModel(
            name='Marche',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=100, unique=True)),
                ('NomAnnonceur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.annonceur')),
            ],
        ),
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=100, unique=True)),
                ('NomAnnonceur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.annonceur')),
            ],
        ),
    ]
