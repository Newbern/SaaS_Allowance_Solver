# Generated by Django 5.1.2 on 2025-03-08 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_allowance_schedules'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allowance',
            name='schedules',
            field=models.CharField(blank=True, choices=[('Weekly', 'Weekly'), ('Biweekly', 'Biweekly'), ('Monthly', 'Monthly')], default='Biweekly', max_length=10),
        ),
    ]
