# Generated by Django 5.1.3 on 2024-11-28 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0005_alter_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('desc', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=20)),
                ('completion_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
