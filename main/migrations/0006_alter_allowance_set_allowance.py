# Generated by Django 5.1.2 on 2025-03-08 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_allowance_schedules'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allowance',
            name='set_allowance',
            field=models.DecimalField(blank=True, decimal_places=2, default=models.DecimalField(decimal_places=2, max_digits=10), max_digits=10, null=True),
        ),
    ]
