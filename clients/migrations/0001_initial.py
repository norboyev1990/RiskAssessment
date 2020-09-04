# Generated by Django 3.0.9 on 2020-08-29 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('ClientID', models.IntegerField(primary_key=True, serialize=False)),
                ('ClientName', models.CharField(max_length=255, verbose_name='Наименование')),
                ('ClientType', models.CharField(max_length=255, verbose_name='Тип клиента')),
                ('Subject', models.CharField(max_length=2)),
                ('Passport', models.CharField(max_length=255)),
                ('CountLoans', models.IntegerField(verbose_name='Кол-во кред-ов')),
                ('TotalLoans', models.DecimalField(decimal_places=0, max_digits=20, verbose_name='Всего задолжен')),
                ('Address', models.CharField(max_length=255)),
                ('Status', models.IntegerField(verbose_name='Класс качества')),
                ('Reserve', models.FloatField(verbose_name='Резервы')),
                ('OstatokReserve', models.FloatField(verbose_name='Необход. резервы')),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DatePogash', models.DateField(verbose_name='Дата погашения')),
                ('PrognozPogash', models.FloatField(verbose_name='Прогноз погашения')),
                ('OstatokPercent', models.FloatField(verbose_name='Остаток нач. процент')),
                ('CurrencyName', models.CharField(max_length=10, verbose_name='Валюта')),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Credits',
            fields=[
                ('CodeContract', models.IntegerField(primary_key=True, serialize=False, verbose_name='Код договора')),
                ('DateContract', models.DateField(verbose_name='Дата договора')),
                ('DateClosed', models.DateField(verbose_name='Дата закрытия')),
                ('SummaContract', models.FloatField(verbose_name='Сумма кредита')),
                ('CreditPercent', models.FloatField(verbose_name='Процент кредита')),
                ('BalanceCredit', models.FloatField(verbose_name='Остаток кредита')),
                ('TypeCredit', models.CharField(max_length=255, verbose_name='Вид кредита')),
                ('PurposeCredit', models.CharField(max_length=255, verbose_name='Цель кредита')),
                ('SummaOverdue', models.FloatField(verbose_name='Просроченная сумма')),
                ('DaysOverdue', models.IntegerField(verbose_name='Просроченные дни')),
                ('DaysOverduePercent', models.IntegerField(verbose_name='Дни проср. проценты')),
                ('SummaPeresm', models.FloatField(verbose_name='Остаток пересм.')),
                ('SummaSudeb', models.FloatField(verbose_name='Остаток судеб.')),
                ('SummaVneb', models.FloatField(verbose_name='Остаток вне баланс.')),
                ('UniqueCode', models.CharField(max_length=10)),
                ('OstatokReserve', models.FloatField(verbose_name='Остаток резерв')),
                ('Reserve', models.FloatField(verbose_name='Необход. резерв')),
                ('NachPercent', models.FloatField(verbose_name='Нач. процент')),
            ],
            options={
                'managed': False,
            },
        ),
    ]
