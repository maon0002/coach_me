# Generated by Django 4.2.3 on 2023-08-04 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectors', '0005_alter_lector_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lector',
            name='slug',
            field=models.SlugField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
