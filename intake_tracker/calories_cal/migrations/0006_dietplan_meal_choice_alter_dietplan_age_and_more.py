# Generated by Django 5.1.1 on 2024-10-25 15:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calories_cal", "0005_dietplan"),
    ]

    operations = [
        migrations.AddField(
            model_name="dietplan",
            name="meal_choice",
            field=models.CharField(
                choices=[
                    ("vegeterian", "vegeterian"),
                    ("non-vegeterian", "non-vegeterian"),
                    ("vegan", "vegan"),
                    ("vegeterian_nonvegeterian", "vegeterian_nonvegeterian"),
                ],
                default=django.utils.timezone.now,
                max_length=25,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="dietplan",
            name="age",
            field=models.IntegerField(default=28),
        ),
        migrations.AlterField(
            model_name="dietplan",
            name="height",
            field=models.FloatField(default=171),
        ),
        migrations.AlterField(
            model_name="dietplan",
            name="weight",
            field=models.FloatField(default=70),
        ),
    ]
