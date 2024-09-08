# Generated by Django 4.2.3 on 2024-09-08 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("teachers", "0007_alter_teacher_subjects"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teacher",
            name="groups",
            field=models.ManyToManyField(
                blank=True, related_name="teacher_groups", to="auth.group"
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="subjects",
            field=models.ManyToManyField(
                blank=True, related_name="teachers", to="teachers.subject"
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True, related_name="teacher_permissions", to="auth.permission"
            ),
        ),
    ]
