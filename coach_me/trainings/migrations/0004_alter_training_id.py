# Generated by Django 4.2.3 on 2023-08-05 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0003_alter_training_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]