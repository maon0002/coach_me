# Generated by Django 4.2.3 on 2023-07-30 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_alter_bookinguserprofile_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinguserprofile',
            name='phone',
            field=models.CharField(blank=True, default=None, max_length=12, null=True),
        ),
    ]
