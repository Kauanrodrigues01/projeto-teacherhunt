# Generated by Django 5.1.1 on 2024-09-14 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classroom", "0003_alter_classroom_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classroom",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Scheduled"),
                    ("accepted", "Completed"),
                    ("cancelled", "Cancelled"),
                ],
                default="scheduled",
                max_length=20,
            ),
        ),
    ]
