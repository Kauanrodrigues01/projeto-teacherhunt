# Generated by Django 4.2.3 on 2024-09-08 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0002_classroom"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="groups",
        ),
        migrations.RemoveField(
            model_name="student",
            name="user_permissions",
        ),
        migrations.DeleteModel(
            name="Classroom",
        ),
        migrations.DeleteModel(
            name="Student",
        ),
    ]
