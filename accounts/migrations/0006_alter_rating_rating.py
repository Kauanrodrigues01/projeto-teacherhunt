# Generated by Django 5.1.1 on 2024-09-20 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="rating",
            field=models.FloatField(),
        ),
    ]
