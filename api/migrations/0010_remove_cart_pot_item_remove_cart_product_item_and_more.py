# Generated by Django 4.0.1 on 2022-02-09 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_cart_pot_item_cart_product_item_delete_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='pot_item',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='product_item',
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pot')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_product', to='api.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_item',
            field=models.ManyToManyField(to='api.CartItem'),
        ),
    ]