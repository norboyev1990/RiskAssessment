# Generated by Django 3.0.9 on 2020-08-10 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CODE', models.CharField(db_index=True, max_length=3)),
                ('NAME', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RateDate', models.DateField()),
                ('RateValue', models.FloatField()),
                ('Currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency', to='references.Currency')),
            ],
        ),
    ]