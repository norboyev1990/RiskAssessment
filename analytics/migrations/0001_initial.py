# Generated by Django 3.0.9 on 2020-08-29 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('Status', models.IntegerField(primary_key=True, serialize=False)),
                ('Title', models.CharField(max_length=45, verbose_name='Класс')),
                ('Balance', models.FloatField(verbose_name='Всего задолженность')),
                ('Percent', models.FloatField(verbose_name='Доля, %')),
                ('Counts', models.IntegerField(verbose_name='Количество')),
                ('Reserve', models.FloatField(verbose_name='Резервы')),
                ('Needed', models.FloatField(verbose_name='Необход. резервы')),
            ],
        ),
    ]