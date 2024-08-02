# Generated by Django 4.2.4 on 2024-08-01 14:33

import crmpipeline.models
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0002_company_saleslead_team_alter_useraccount_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Activity",
            fields=[
                ("title", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("COMPLETED", "COMPLETED"),
                            ("CANCELLED", "CANCELLED"),
                            ("ONGOING", "ONGOING"),
                            ("RESCHEDULE", "RESCHEDULE"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Deal",
            fields=[
                (
                    "unique_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("deal_title", models.CharField(blank=True, max_length=100, null=True)),
                ("description", models.TextField(max_length=300, null=True)),
                (
                    "trail",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.JSONField(), default=[], size=None
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        blank=True,
                        choices=[("HOT", "HOT"), ("WARM", "WARM"), ("COLD", "COLD")],
                        default="HOT",
                        max_length=100,
                        null=True,
                    ),
                ),
                ("industry", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "deal_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("WON", "WON"),
                            ("LOST", "LOST"),
                            ("ONGOING", "ONGOING"),
                        ],
                        default="HOT",
                        max_length=100,
                        null=True,
                    ),
                ),
                ("contact_person", models.CharField(max_length=100)),
                ("value", models.CharField(max_length=100)),
                (
                    "product",
                    models.CharField(
                        choices=[
                            ("STOCKS_INVENTORY", "STOCKS_INVENTORY"),
                            ("SALES", "SALES"),
                            ("SPEND_MANAGEMENT", "SPEND_MANAGEMENT"),
                            ("HR_MANAGEMENT", "HR_MANAGEMENT"),
                        ],
                        max_length=100,
                    ),
                ),
                ("start_date", models.DateTimeField(auto_now_add=True)),
                ("expected_close_date", models.DateTimeField(auto_now_add=True)),
                ("phone_num", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
            ],
            options={
                "verbose_name": "DEAL",
                "verbose_name_plural": "DEAL",
            },
        ),
        migrations.CreateModel(
            name="DealProgression",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("email", models.EmailField(max_length=254)),
                (
                    "trail",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.JSONField(), default=[], size=None
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("COMPLETED", "COMPLETED"),
                            ("CANCELLED", "CANCELLED"),
                            ("ONGOING", "ONGOING"),
                            ("RESCHEDULE", "RESCHEDULE"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("unique_id", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
            ],
            options={
                "verbose_name": "DEAL PROGRESSION",
                "verbose_name_plural": "DEAL PROGRESSIONS",
            },
        ),
        migrations.CreateModel(
            name="DealRequirement",
            fields=[
                (
                    "custom_fields",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.JSONField(), blank=True, null=True, size=None
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
            ],
            options={
                "verbose_name": "DEAL REQUIREMENT",
                "verbose_name_plural": "DEAL REQUIREMENTS",
            },
        ),
        migrations.CreateModel(
            name="EmaiLog",
            fields=[
                ("subject", models.CharField(blank=True, max_length=255, null=True)),
                ("message", models.TextField(blank=True, null=True)),
                ("recipient", models.EmailField(max_length=254)),
                ("sender", models.EmailField(max_length=254)),
                (
                    "status",
                    models.CharField(
                        choices=[("success", "Success"), ("failure", "Failure")],
                        default="failure",
                        max_length=20,
                    ),
                ),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
            ],
            options={
                "verbose_name": "Email Log",
                "verbose_name_plural": "Email Logs",
            },
        ),
        migrations.CreateModel(
            name="HeadOfSales",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.CharField(max_length=100)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LeadsDataUpload",
            fields=[
                (
                    "leads_file",
                    models.FileField(blank=True, null=True, upload_to="leads_file"),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
            ],
            options={
                "verbose_name": "LEADS DATA UPLOAD",
                "verbose_name_plural": "LEADS DATA UPLOADS",
            },
        ),
        migrations.CreateModel(
            name="Pipeline",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "pipeline_type",
                    models.CharField(
                        choices=[("DEFAULT", "DEFAULT"), ("CUSTOM", "CUSTOM")],
                        default="DEFAULT",
                        max_length=100,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Report",
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
            ],
        ),
        migrations.CreateModel(
            name="Stage",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("order", models.IntegerField(default=0)),
                (
                    "email_subject",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("email_body", models.TextField(blank=True, null=True)),
                ("email_text", models.TextField(blank=True, null=True)),
                ("email_notifications_enabled", models.BooleanField(default=True)),
                ("merchant_count", models.IntegerField(blank=True, null=True)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                (
                    "pipeline",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crmpipeline.pipeline",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "task_id",
                    models.CharField(
                        default=crmpipeline.models.generate_random_task_id,
                        editable=False,
                        max_length=20,
                        unique=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("COMPLETED", "COMPLETED"),
                            ("CANCELLED", "CANCELLED"),
                            ("ONGOING", "ONGOING"),
                            ("RESCHEDULE", "RESCHEDULE"),
                        ],
                        default="uncompleted",
                        max_length=100,
                    ),
                ),
                ("trail", models.JSONField(blank=True, default=dict)),
                ("deadline", models.DateTimeField(blank=True, null=True)),
                ("deadline_reminder", models.BooleanField(default=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                (
                    "activity",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crmpipeline.activity",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "current_stage",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="todos",
                        to="crmpipeline.stage",
                    ),
                ),
                (
                    "deal",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crmpipeline.deal",
                    ),
                ),
                (
                    "deal_progression",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crmpipeline.dealprogression",
                    ),
                ),
                (
                    "merchant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="merchants",
                        to="users.company",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TaskSchedule",
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
            ],
        ),
        migrations.CreateModel(
            name="TeamMemberPermission",
            fields=[
                ("name", models.CharField(max_length=100, null=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
            ],
            options={
                "verbose_name": "TEAM MEMBER PERMISSION",
                "verbose_name_plural": "TEAM MEMBER PERMISSIONS",
            },
        ),
        migrations.CreateModel(
            name="TeamMemberRole",
            fields=[
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("ADMIN", "ADMIN"),
                            ("HEAD_OF_SALES", "HEAD_OF_SALES"),
                            ("SALES_LEAD", "SALES_LEAD"),
                            ("SALES_OFFICER", "SALES_OFFICER"),
                            ("MEMBER", "MEMBER"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
            ],
            options={
                "verbose_name": "TEAM MEMBER PERMISSION",
                "verbose_name_plural": "TEAM MEMBER PERMISSIONS",
            },
        ),
        migrations.CreateModel(
            name="TeamMemberRolePermission",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                (
                    "merchant",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.company",
                    ),
                ),
                (
                    "permission",
                    models.ManyToManyField(
                        blank=True, to="crmpipeline.teammemberpermission"
                    ),
                ),
                (
                    "role",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crmpipeline.teammemberrole",
                    ),
                ),
            ],
            options={
                "verbose_name": "TEAM MEMBER ROLE PERMISSION",
                "verbose_name_plural": "TEAM MEMBER ROLE PERMISSIONS",
            },
        ),
        migrations.CreateModel(
            name="TaskNotification",
            fields=[
                ("notified_at", models.DateTimeField(auto_now=True)),
                ("message", models.TextField()),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                (
                    "task",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crmpipeline.task",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TaskComment",
            fields=[
                ("comment", models.TextField()),
                ("show_as_single_comment", models.BooleanField(default=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                (
                    "parent_comment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crmpipeline.taskcomment",
                    ),
                ),
                (
                    "sales_officer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_comments",
                        to="users.salesofficer",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="crmpipeline.task",
                    ),
                ),
            ],
            options={
                "verbose_name": "TASK COMMENT",
                "verbose_name_plural": "TASK COMMENTS",
            },
        ),
        migrations.CreateModel(
            name="MerchantDealPipeline",
            fields=[
                ("name", models.CharField(max_length=100)),
                ("order", models.IntegerField(default=0)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                (
                    "merchant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="merchant_pipeline",
                        to="users.company",
                    ),
                ),
            ],
            options={
                "verbose_name": "MERCHANT DEAL PIPELINE",
                "verbose_name_plural": "MERCHANT DEAL PIPELINES",
            },
        ),
        migrations.CreateModel(
            name="Lead",
            fields=[
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("email_address", models.EmailField(max_length=254)),
                ("company", models.CharField(blank=True, max_length=100, null=True)),
                ("address", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "label",
                    models.CharField(
                        choices=[("HOT", "HOT"), ("WARM", "WARM"), ("COLD", "COLD")],
                        default="COLD",
                        max_length=100,
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "stage",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crmpipeline.stage",
                    ),
                ),
            ],
            options={
                "verbose_name": "LEADS",
            },
        ),
        migrations.CreateModel(
            name="DealsComment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("comment", models.TextField()),
                ("show_as_single_comment", models.BooleanField(default=True)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                (
                    "deal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="crmpipeline.deal",
                    ),
                ),
                (
                    "parent_comment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crmpipeline.dealscomment",
                    ),
                ),
                (
                    "sales_officer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="deals_comments",
                        to="users.salesofficer",
                    ),
                ),
            ],
            options={
                "verbose_name": "DEAL COMMENT",
                "verbose_name_plural": "DEAL COMMENTS",
            },
        ),
        migrations.AddField(
            model_name="dealprogression",
            name="current_stage",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="crmpipeline.stage",
            ),
        ),
        migrations.AddField(
            model_name="dealprogression",
            name="deal",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="crmpipeline.deal",
            ),
        ),
        migrations.AddField(
            model_name="dealprogression",
            name="pipeline",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="crmpipeline.pipeline",
            ),
        ),
        migrations.CreateModel(
            name="DealPipeline",
            fields=[
                ("name", models.CharField(max_length=255)),
                ("order", models.IntegerField(default=0)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                (
                    "deal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="deal_pipeline",
                        to="crmpipeline.deal",
                    ),
                ),
            ],
            options={
                "verbose_name": "DEAL PIPELINE",
                "verbose_name_plural": "DEAL PIPELINES",
            },
        ),
        migrations.AddField(
            model_name="deal",
            name="current_stage",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="crmpipeline.stage",
            ),
        ),
        migrations.AddField(
            model_name="deal",
            name="merchant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="leads",
                to="users.company",
            ),
        ),
        migrations.AddField(
            model_name="deal",
            name="team_member",
            field=models.ManyToManyField(
                related_name="team_member", to="users.salesofficer"
            ),
        ),
        migrations.AddField(
            model_name="deal",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="activity",
            name="stage",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="crmpipeline.stage"
            ),
        ),
        migrations.CreateModel(
            name="TeamMember",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "member",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.salesofficer",
                    ),
                ),
                (
                    "merchant",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.company",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crmpipeline.teammemberrolepermission",
                    ),
                ),
            ],
            options={
                "verbose_name": "TEAM MEMBER",
                "unique_together": {("merchant", "member")},
            },
        ),
    ]
