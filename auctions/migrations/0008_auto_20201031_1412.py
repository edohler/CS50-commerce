# Generated by Django 3.1.1 on 2020-10-31 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20201031_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='categorie',
            field=models.CharField(choices=[('Hobby', 'Hobby'), ('Fashion', 'Fashion'), ('Electronics', 'Electronics'), ('Home', 'Home')], max_length=20),
        ),
    ]
