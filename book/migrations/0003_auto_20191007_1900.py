# Generated by Django 2.2.5 on 2019-10-07 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20191002_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='phone_numbers',
            field=models.CharField(max_length=200),
        ),
    ]
