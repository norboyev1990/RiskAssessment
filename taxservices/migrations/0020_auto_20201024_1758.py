# Generated by Django 3.0.9 on 2020-10-24 12:58

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('taxservices', '0019_physicalperson'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_no', models.CharField(max_length=3)),
                ('sum_begin_period', models.IntegerField()),
                ('sum_end_period', models.IntegerField()),
            ],
            options={
                'managed': False,
            },
            managers=[
                ('services', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='BaseNDS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ns10_code', models.IntegerField()),
                ('ns11_code', models.IntegerField()),
                ('tin', models.CharField(max_length=9)),
                ('company_name', models.CharField(max_length=9)),
                ('nds', models.FloatField()),
                ('ndsupr', models.FloatField()),
            ],
            options={
                'managed': False,
            },
            managers=[
                ('services', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Dividend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ns10_code', models.IntegerField()),
                ('ns11_code', models.IntegerField()),
                ('tin', models.CharField(max_length=9)),
                ('fio', models.CharField(max_length=100)),
                ('company_tin', models.CharField(max_length=9)),
                ('company_name', models.CharField(max_length=100)),
                ('adress', models.CharField(max_length=100)),
                ('vid_d', models.CharField(max_length=50)),
                ('summa1', models.FloatField()),
                ('summa2', models.FloatField()),
                ('summa3', models.FloatField()),
            ],
            options={
                'managed': False,
            },
            managers=[
                ('services', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ns10_code', models.IntegerField()),
                ('ns11_code', models.IntegerField()),
                ('tin', models.CharField(max_length=9)),
                ('fio', models.CharField(max_length=100)),
                ('company_tin', models.CharField(max_length=9)),
                ('doxod1', models.FloatField()),
                ('doxod2', models.FloatField()),
            ],
            options={
                'managed': False,
            },
            managers=[
                ('services', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_no', models.CharField(max_length=3)),
                ('sum_old_period_doxod', models.IntegerField()),
                ('sum_old_period_rasxod', models.IntegerField()),
                ('sum_period_doxod', models.IntegerField()),
                ('sum_period_rasxod', models.IntegerField()),
            ],
            options={
                'managed': False,
            },
            managers=[
                ('services', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Founder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ns10_code', models.IntegerField()),
                ('ns11_code', models.IntegerField()),
                ('tin', models.CharField(max_length=9)),
                ('fio', models.CharField(max_length=100)),
                ('dolya', models.CharField(max_length=9)),
                ('company_tin', models.CharField(max_length=9)),
                ('company_name', models.CharField(max_length=100)),
                ('adress', models.CharField(max_length=100)),
            ],
            options={
                'managed': False,
            },
            managers=[
                ('services', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Leased',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ns10_code', models.IntegerField()),
                ('ns11_code', models.IntegerField()),
                ('tin', models.CharField(max_length=9)),
                ('name', models.CharField(max_length=100)),
                ('obj_code', models.CharField(max_length=100)),
                ('obj_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('rentSum', models.FloatField()),
                ('rentArea', models.FloatField()),
                ('beginDate', models.CharField(max_length=10)),
                ('endDate', models.CharField(max_length=10)),
            ],
            options={
                'managed': False,
            },
            managers=[
                ('services', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ns10_code', models.IntegerField()),
                ('ns11_code', models.IntegerField()),
                ('tin', models.CharField(max_length=9)),
                ('name', models.CharField(max_length=100)),
                ('obj_code', models.CharField(max_length=100)),
                ('obj_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('percentage', models.IntegerField()),
                ('inv_cost', models.IntegerField()),
                ('total_area', models.FloatField()),
                ('land_area', models.FloatField()),
                ('land_extra_area', models.FloatField()),
            ],
            options={
                'managed': False,
            },
            managers=[
                ('services', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ReportENP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ns10_code', models.IntegerField()),
                ('ns11_code', models.IntegerField()),
                ('tin', models.CharField(max_length=9)),
                ('company_name', models.CharField(max_length=9)),
                ('enp101', models.FloatField()),
                ('enp102', models.FloatField()),
                ('prib10', models.FloatField()),
            ],
            options={
                'managed': False,
            },
            managers=[
                ('services', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tin', models.CharField(max_length=9)),
                ('name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('period', models.IntegerField()),
                ('pinfl', models.CharField(max_length=9)),
                ('ns10_code', models.IntegerField()),
                ('ns11_code', models.IntegerField()),
                ('company_name', models.CharField(max_length=100)),
                ('company_tin', models.CharField(max_length=100)),
                ('salary', models.IntegerField()),
                ('salary_tax_sum', models.IntegerField()),
                ('inps_sum', models.IntegerField()),
                ('prop_income', models.IntegerField()),
                ('other_income', models.IntegerField()),
                ('series_passport', models.CharField(max_length=2)),
                ('number_passport', models.CharField(max_length=7)),
            ],
            options={
                'managed': False,
            },
            managers=[
                ('services', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TaxDebt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ns10_code', models.IntegerField()),
                ('ns11_code', models.IntegerField()),
                ('tin', models.CharField(max_length=9)),
                ('company_name', models.CharField(max_length=100)),
                ('ned_date', models.CharField(max_length=20)),
                ('na2_code', models.IntegerField()),
                ('ned_summa', models.FloatField()),
            ],
            options={
                'managed': False,
            },
            managers=[
                ('services', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='juridicalperson',
            managers=[
                ('services', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='juridicalperson',
            name='slug',
            field=models.CharField(default='X', max_length=11),
        ),
        migrations.AddField(
            model_name='physicalperson',
            name='slug',
            field=models.CharField(default='X', max_length=11),
        ),
    ]