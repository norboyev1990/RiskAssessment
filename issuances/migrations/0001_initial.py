# Generated by Django 3.0.9 on 2020-08-11 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TITLE', models.CharField(max_length=255)),
                ('ISSUE_YEAR', models.IntegerField()),
                ('ISSUE_MONTH', models.IntegerField()),
                ('DATE_CREATE', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CODE_REGION', models.CharField(max_length=3)),
                ('MFO', models.CharField(max_length=5)),
                ('NAME_CLIENT', models.CharField(max_length=255)),
                ('CREDIT_SCHET', models.CharField(max_length=20)),
                ('BALANS_SCHET', models.CharField(max_length=20)),
                ('PROCENT_CREDIT', models.FloatField()),
                ('PROCENT_PROSR', models.FloatField()),
                ('SUMMA_DOGOVOR', models.FloatField()),
                ('SUMMA_FACT', models.FloatField()),
                ('DATE_VIDACHI', models.DateField()),
                ('DATE_POGASH', models.DateField()),
                ('SEL_CREDITA', models.CharField(max_length=255)),
                ('OTRASL_CLIENTA', models.CharField(max_length=255)),
                ('VID_CREDITA', models.CharField(max_length=255)),
                ('ISTOCHNIK_CREDITA', models.CharField(max_length=255)),
                ('SCHET_KORRESPONDENT', models.CharField(max_length=5)),
                ('NAME_KORRESPONDENT', models.CharField(max_length=255)),
                ('DATE_PERVOY_VYBOR', models.DateField()),
                ('ISSUANCE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issuance', to='issuances.List')),
            ],
        ),
    ]
