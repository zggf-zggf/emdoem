# Generated by Django 4.1.6 on 2023-08-01 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_problem_source'),
        ('notifications', '0004_newsolutionnotification'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewProblemNotification',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notifications.notification')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.solution')),
            ],
            bases=('notifications.notification',),
        ),
    ]
