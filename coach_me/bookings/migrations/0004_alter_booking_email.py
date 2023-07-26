# Generated by Django 4.2.3 on 2023-07-24 07:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookings', '0003_rename_employee_booking_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bookings', to=settings.AUTH_USER_MODEL),
        ),
    ]