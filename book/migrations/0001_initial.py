# Generated by Django 2.2.5 on 2019-09-29 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('phone_numbers', models.CharField(max_length=16)),
                ('id', models.AutoField(default=1, primary_key=True, serialize=False)),
            ],
        ),
    ]
