# Generated by Django 4.2.3 on 2023-07-28 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0001_initial'),
        ('lectors', '0002_lector_user'),
        ('bookings', '0007_alter_booking_options_alter_booking_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='trainings.training'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='lector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lectors.lector'),
        ),
        migrations.DeleteModel(
            name='Lector',
        ),
        migrations.DeleteModel(
            name='Training',
        ),
    ]