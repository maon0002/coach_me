# Generated by Django 4.2.3 on 2023-07-31 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0002_training_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='slug',
            field=models.SlugField(blank=True, max_length=254, unique=True),
        ),
    ]
