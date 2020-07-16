# Generated by Django 3.0.8 on 2020-07-14 07:42

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('deleted', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('title', models.CharField(max_length=250)),
                ('is_done', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Todo',
                'verbose_name_plural': 'Todo',
            },
        ),
    ]