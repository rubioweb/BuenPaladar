# Generated by Django 5.1.1 on 2024-10-28 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receta',
            name='visitas',
            field=models.IntegerField(default=0),
        ),
    ]
