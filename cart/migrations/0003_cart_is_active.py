# Generated by Django 5.1.3 on 2025-03-14 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_alter_cartitem_cart"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
