# Generated by Django 4.1.6 on 2023-07-19 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_comment_upvote_counter_commentvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertoproblem',
            name='began_surrendering',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usertoproblem',
            name='surrender_end_time',
            field=models.DateTimeField(null=True),
        ),
    ]
