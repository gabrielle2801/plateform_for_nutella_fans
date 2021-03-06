# Generated by Django 3.2 on 2021-09-16 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nutriscore', models.CharField(max_length=1, null=True)),
                ('nova', models.IntegerField(null=True)),
                ('url', models.URLField()),
                ('barcode', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(null=True)),
                ('picture', models.URLField(null=True)),
                ('fat_100g', models.FloatField(null=True)),
                ('fat_level', models.CharField(max_length=50, null=True)),
                ('salt_100g', models.FloatField(null=True)),
                ('salt_level', models.CharField(max_length=50, null=True)),
                ('saturated_fat_100g', models.FloatField(null=True)),
                ('saturated_fat_level', models.CharField(max_length=50, null=True)),
                ('sugars_100g', models.FloatField(null=True)),
                ('sugars_level', models.CharField(max_length=50, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.brand')),
                ('categories', models.ManyToManyField(to='product.Category')),
                ('stores', models.ManyToManyField(to='product.Store')),
            ],
        ),
    ]
