# Generated by Django 4.1.6 on 2023-08-05 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_remove_solution_voters'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
