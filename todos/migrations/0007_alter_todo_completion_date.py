# Generated by Django 5.1.3 on 2024-11-29 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0006_todo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
