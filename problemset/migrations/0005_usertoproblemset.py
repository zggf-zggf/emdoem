# Generated by Django 4.1.6 on 2023-08-09 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problemset', '0004_problemset_featured'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserToProblemset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_visit', models.DateTimeField(null=True)),
                ('problemset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problemset.problemset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
