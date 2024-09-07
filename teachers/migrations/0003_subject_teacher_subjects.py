# Generated by Django 4.2.3 on 2024-09-07 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teachers", "0002_teacher_profile_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subject",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name="teacher",
            name="subjects",
            field=models.ManyToManyField(
                related_name="teachers", to="teachers.subject"
            ),
        ),
    ]
