# Generated by Django 4.2.3 on 2024-09-07 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teachers", "0003_subject_teacher_subjects"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teacher",
            name="subjects",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="teachers", to="teachers.subject"
            ),
        ),
    ]
