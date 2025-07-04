# Generated by Django 5.2.3 on 2025-07-01 19:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orderServices", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="phone_number",
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must be exactly 10 digits.",
                        regex="^\\d{10}$",
                    )
                ],
                verbose_name="Customer Phone Number",
            ),
        ),
    ]
