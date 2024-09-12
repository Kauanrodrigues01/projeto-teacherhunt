# Generated by Django 4.2.3 on 2024-09-12 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_teacher_profile_image"),
        ("classroom", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="classroom",
            unique_together={("teacher", "student", "start_time")},
        ),
        migrations.AddField(
            model_name="classroom",
            name="description_about_class",
            field=models.TextField(blank=True, null=True),
        ),
    ]