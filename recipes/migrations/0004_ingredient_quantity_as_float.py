# Generated by Django 3.2 on 2021-08-28 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_ingredient_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='quantity_as_float',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
