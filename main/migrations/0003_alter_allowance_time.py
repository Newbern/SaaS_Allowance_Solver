# Generated by Django 5.1.2 on 2025-03-08 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_allowance_time_alter_expense_spending'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allowance',
            name='time',
            field=models.CharField(choices=[('weekly', 'Weekly'), ('biweekly', 'Biweekly'), ('monthly', 'Monthly')], default='biweekly', max_length=10),
        ),
    ]
