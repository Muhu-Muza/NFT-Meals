# Generated by Django 4.2.3 on 2023-07-31 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lunch_Menu', '0003_alter_fooditem_foodtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='foodType',
            field=models.CharField(choices=[('food', 'Food'), ('sauces', 'Sauces'), ('drinks', 'Drinks')], default='Matooke', max_length=100),
        ),
    ]