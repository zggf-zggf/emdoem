# Generated by Django 4.1.6 on 2023-08-05 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='is_visible',
            field=models.BooleanField(default=False),
        ),
    ]
