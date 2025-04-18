# Generated by Django 5.1.1 on 2024-10-09 14:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CaloriesIntake",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("protein", models.DateField(default=django.utils.timezone.now)),
                ("carbs", models.FloatField(default=0.0)),
                ("fats", models.FloatField(default=0.0)),
                ("fibers", models.FloatField(default=0.0)),
            ],
        ),
    ]
