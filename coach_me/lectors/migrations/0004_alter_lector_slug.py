# Generated by Django 4.2.3 on 2023-07-31 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectors', '0003_alter_lector_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lector',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]