# Generated by Django 5.1.1 on 2024-10-07 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_favoriteteacher"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="name",
            field=models.CharField(max_length=60, unique=True),
        ),
    ]
