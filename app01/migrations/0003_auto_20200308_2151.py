# Generated by Django 3.0.3 on 2020-03-08 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20200302_1350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='tel',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='avatars/default.png', upload_to='avatars/', verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='phone',
            field=models.CharField(max_length=11, null=True, unique=True),
        ),
    ]
