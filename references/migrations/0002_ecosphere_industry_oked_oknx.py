# Generated by Django 3.0.9 on 2020-10-13 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EcoSphere',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OKNX',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('sect', models.CharField(max_length=5)),
                ('ecosphere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oknx_sphere', to='references.EcoSphere')),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oknx_industry', to='references.Industry')),
            ],
        ),
        migrations.CreateModel(
            name='OKED',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('sect', models.CharField(max_length=1)),
                ('ecosphere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oked_sphere', to='references.EcoSphere')),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oked_industry', to='references.Industry')),
            ],
        ),
    ]
