# Generated by Django 4.1.6 on 2023-07-08 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_problem_problem_statement_alter_content_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='content',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='content',
        ),
        migrations.DeleteModel(
            name='Content',
        ),
    ]
