# Generated by Django 4.0.1 on 2022-02-09 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_pot_cartitem_pot_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_item',
            field=models.ManyToManyField(related_name='cart_item', to='api.CartItem'),
        ),
    ]