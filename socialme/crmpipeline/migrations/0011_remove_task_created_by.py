# Generated by Django 4.2.4 on 2024-08-16 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("crmpipeline", "0010_remove_task_activity_activity_task_task_activity_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="created_by",
        ),
    ]
