# Generated by Django 5.1.1 on 2024-11-25 16:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calories_cal", "0006_dietplan_meal_choice_alter_dietplan_age_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="caloriesintake",
            name="calories",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
