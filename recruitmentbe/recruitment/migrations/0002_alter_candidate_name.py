# Generated by Django 5.0.4 on 2024-04-05 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
