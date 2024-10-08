# Generated by Django 4.2.4 on 2024-08-16 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crmpipeline", "0009_rename_stages_activity_stage_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="activity",
        ),
        migrations.AddField(
            model_name="activity",
            name="task",
            field=models.ManyToManyField(blank=True, to="crmpipeline.task"),
        ),
        migrations.AddField(
            model_name="task",
            name="activity_id",
            field=models.ManyToManyField(
                blank=True, related_name="activity", to="crmpipeline.activity"
            ),
        ),
    ]
