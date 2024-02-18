# Generated by Django 4.0.10 on 2024-02-18 01:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('telegram', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(choices=[('CONFERENCE', 'Конференция'), ('BREAKFAST', 'Коуч-завтрак'), ('GAME', 'Игра')], default='CONFERENCE', max_length=255, verbose_name='Продукт')),
                ('product_id', models.CharField(max_length=255, verbose_name='UUID продукта')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('status', models.CharField(choices=[('SUCCESS', 'Успех'), ('FAIL', 'Ошибка'), ('NEW', 'Новый')], default='NEW', max_length=255, verbose_name='Статус платежа')),
                ('data', models.JSONField(null=True, verbose_name='Данные платежа')),
                ('ticket', models.CharField(choices=[('SILVER', 'SILVER'), ('GOLD', 'GOLD'), ('PLATINUM', 'PLATINUM'), ('NONE', 'NONE')], default='NONE', max_length=255, verbose_name='Категория билета')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='telegram.botuser', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
    ]
