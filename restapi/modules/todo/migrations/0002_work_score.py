# Generated by Django 3.0.8 on 2020-07-14 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi_todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
