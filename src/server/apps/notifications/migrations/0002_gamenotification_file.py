# Generated by Django 4.0.10 on 2024-02-07 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamenotification',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='notifications', verbose_name='Файл'),
        ),
    ]
