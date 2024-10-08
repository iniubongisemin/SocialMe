# Generated by Django 4.2.4 on 2024-08-15 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crmpipeline", "0006_remove_activity_stage_stage_activity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("COMPLETED", "COMPLETED"),
                    ("CANCELLED", "CANCELLED"),
                    ("ONGOING", "ONGOING"),
                    ("RESCHEDULE", "RESCHEDULE"),
                ],
                default="ONGOING",
                max_length=100,
                null=True,
            ),
        ),
    ]
