# Generated by Django 4.2.4 on 2024-08-19 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("crmpipeline", "0014_remove_activity_stage_id_activity_deal"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stage",
            name="activity",
        ),
    ]
