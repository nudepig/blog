# Generated by Django 3.0.3 on 2020-04-09 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_auto_20200409_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
