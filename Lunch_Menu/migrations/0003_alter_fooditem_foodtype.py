# Generated by Django 4.2.1 on 2023-07-31 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lunch_Menu', '0002_fooditem_foodtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='foodType',
            field=models.CharField(choices=[('food', 'Food'), ('sauces', 'Sauces'), ('drinks', 'Drinks')], max_length=100),
        ),
    ]