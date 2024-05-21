# Generated by Django 5.0.4 on 2024-05-15 23:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('domain_id', models.AutoField(primary_key=True, serialize=False)),
                ('domain_name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EtfProduct',
            fields=[
                ('etf_product_id', models.AutoField(primary_key=True, serialize=False)),
                ('etf_product_name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ETF.domain')),
            ],
        ),
        migrations.CreateModel(
            name='EtfPrice',
            fields=[
                ('etf_price_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('transaction_date', models.DateTimeField()),
                ('closing_price', models.IntegerField()),
                ('trading_volume', models.IntegerField()),
                ('change', models.FloatField()),
                ('etf_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ETF.etfproduct')),
            ],
        ),
        migrations.CreateModel(
            name='EtfMajorCompany',
            fields=[
                ('etf_major_company_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_name', models.CharField(max_length=100)),
                ('etf_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ETF.etfproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('industry_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('industry_name', models.CharField(max_length=255, unique=True)),
                ('domains', models.ManyToManyField(related_name='industries', to='ETF.domain')),
            ],
        ),
        migrations.AddConstraint(
            model_name='etfprice',
            constraint=models.UniqueConstraint(fields=('etf_product', 'transaction_date'), name='unique_etf_product_transaction_date'),
        ),
        migrations.AddConstraint(
            model_name='etfmajorcompany',
            constraint=models.UniqueConstraint(fields=('etf_product', 'company_name'), name='unique_etf_product_company_name'),
        ),
    ]
