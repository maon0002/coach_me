# Generated by Django 4.2.3 on 2023-07-23 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinguserprofile',
            name='newsletter_subscription',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]