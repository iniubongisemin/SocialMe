# Generated by Django 4.2.4 on 2024-08-20 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crmpipeline", "0022_remove_pipeline_stages_stage_pipeline"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stage",
            name="pipeline",
        ),
        migrations.AddField(
            model_name="pipeline",
            name="stages",
            field=models.ManyToManyField(blank=True, to="crmpipeline.stage"),
        ),
    ]
