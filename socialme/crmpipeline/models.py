from django.db import models
import uuid
import string
import random
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext as _
from simplejwtauth.models import Company, SalesOfficer #,Team
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def generate_random_stage_id(length=6):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_random_pipeline_id(length=6):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_random_task_id(length=6):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_random_activity_id(length=6):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


class Pipeline(models.Model):
    PIPELINE_TYPE_CHOICES = [
        ("DEFAULT", "DEFAULT"),
        ("CUSTOM", "CUSTOM"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    stages = models.ManyToManyField("Stage", blank=True)
    pipeline_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pipeline_type = models.CharField(max_length=100, choices=PIPELINE_TYPE_CHOICES, default="DEFAULT")
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)
    # merchant = models.ForeignKey(Company, on_delete=models.CASCADE)
    # automation_enabled = models.BooleanField(blank=False)
    # is_default = models.BooleanField(default=True)

    def __str__(self):
        return self.name
        

class Stage(models.Model):
    name = models.CharField(max_length=100)
    stage_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.IntegerField(default=0)
    activity = models.ManyToManyField("Activity", blank=True)
    email_subject = models.CharField(max_length=100, blank=True, null=True)
    email_body = models.TextField(blank=True, null=True)
    email_text = models.TextField(blank=True, null=True)
    email_notifications_enabled = models.BooleanField(default=True)
    merchant_count = models.IntegerField(blank=True, null=True)
    # pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    # automation_enabled = models.BooleanField(blank=False)
    # is_new_merchant = models.BooleanField(default=False)
    # move_criteria = models.IntegerField(default=1)

    @classmethod
    def create_stage(cls, validated_data):
        stage = cls.objects.create(
            user=validated_data.get('pipeline_id'),
            company_id=validated_data.get("company_id"),
            is_active=True
        )

    def __str__(self):
        return self.name


class Deal(models.Model):
    DEAL_STATUS = [
        ("WON", "WON"),
        ("LOST", "LOST"),
        ("ONGOING", "ONGOING"),
    ]

    LABEL = [
        ("HOT", "HOT"),
        ("WARM", "WARM"),
        ("COLD", "COLD"),
    ]

    PRODUCT_VERTICALS_CHOICES = [
        ("STOCKS_INVENTORY", 'STOCKS_INVENTORY'),
        ("SALES", 'SALES'),
        ("SPEND_MANAGEMENT", 'SPEND_MANAGEMENT'),
        ("HR_MANAGEMENT", 'HR_MANAGEMENT'),
    ]

    deal_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    deal_title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=300, null=True)
    merchant = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='leads')
    sales_officer = models.ForeignKey(SalesOfficer, on_delete=models.CASCADE, null=True, blank=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    trail = ArrayField(models.JSONField(), default=list)
    current_stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, blank=True, null=True)
    contact_person = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    product = models.CharField(max_length=100, choices=PRODUCT_VERTICALS_CHOICES)
    start_date = models.DateTimeField             (auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expected_close_date = models.DateTimeField(auto_now_add=True)
    phone_num = models.CharField(max_length=50)
    email = models.EmailField()
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)
    label = models.CharField(
        max_length=100,
        choices=LABEL,
        default="HOT",
        blank=True,
        null=True,
    )
    deal_status = models.CharField(
        max_length=100,
        choices=DEAL_STATUS,
        default="HOT",
        blank=True,
        null=True,
    )
    # team_member = models.ManyToManyField(SalesOfficer, related_name="team_member")
    
    class Meta:
        verbose_name = "DEAL"
        verbose_name_plural = "DEAL"

    def __str__(self):
        return self.deal_title

    @classmethod
    def create(cls, **kwargs):
        deal = cls(**kwargs)
        deal.save()
        return deal
    
    @classmethod
    def deal_progression_count(cls, deal_id):
        # Filter all deals for the given deal_id where current stage is not null
        all_merchants = cls.objects.filter(deal__unique_id=deal_id, current_stage__isnull=False)

        # Get distinct current stages
        unique_stage = all_merchants.values("current_stage").distinct()

        data = []
        for stage in unique_stage:
            data.append(stage.get("current_stage"))

        all_count = {}
        total_count = cls.objects.filter(deal__unique_id=deal_id).count() or 0

        for stage_id in data:
            # Get the count of applications for the current stage
            this_count = all_merchants.filter(current_stage__id=stage_id).count() or 0

            # Get the stage name from the Stage model
            stage_name = Stage.objects.filter(id=stage_id).values_list("name", flat=True).first()

            # Update the all_count dictionary with the stage name
            all_count.update({stage_name: this_count})

        this_data = {
            "total_count": total_count,
            "data": all_count
        }

        return this_data

    @classmethod
    def deal_count(cls, deal_id):
        # Filter all deals for where current stage is not null
        all_deals = cls.objects.filter(deal__unique_id=deal_id, current_stage__isnull=False)

        # Get distinct current stages
        unique_stage = all_deals.values("current_stage").distinct()

        data = []
        for stage in unique_stage:
            data.append(stage.get("current_stage"))

        all_count = {}
        total_count = cls.objects.filter(deal__unique_id=deal_id).count() or 0

        for stage_id in data:
            # Get the count of all deals for the current stage
            this_count = all_deals.filter(current_stage_id=stage_id).count() or 0
            # Get the stage name from the Stage model
            stage_name = Stage.objects.filter(id=stage_id).values_list("name", flat=True).first()
            # Update the all_count dictionary with the stage name
            all_count.update({stage_name: this_count})

            this_data = {
                "total_count": total_count,
                "data": all_count
            } 

            return this_data
        
        def __str__(self):
            return f"Deal for {self.name}"
        

    def update_deal_status(self):
        """
        Updates the deal status based on the deal's start date and expected close date.
        """
        now = datetime.now().date()

        if self.expected_close_date and self.expected_close_date < now:
            self.deal_status = "LOST"
        elif self.start_date and self.start_date <= now <= self.expected_close_date:
            self.deal_status = "WON"
        elif self.start_date and now < self.start_date:
            self.deal_status = "ONGOING"

        self.save()


class Lead(models.Model):
    LABEL = [
        ("HOT", "HOT"),
        ("WARM", "WARM"),
        ("COLD", "COLD"),
    ]

    lead_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    email_address = models.EmailField()
    company = models.CharField(max_length=100, blank=True, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=100, choices=LABEL, default="COLD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "LEAD"
        verbose_name = "LEADS"

    def __str__(self):
        return self.name
    
    def convert_lead_to_deal(self):
        """
        This function can be called to convert a Lead to a Deal if the label is set to "HOT" 
        """
        if self.label == "HOT":
            deal = Deal.objects.create(
                deal_title = self.name,
                phone_num = self.phone_number,
                email = self.email_address,
                merchant = self.company,
                current_stage = self.stage,
                contact_person = self.name,
                label = self.label,
                deal_status = "ONGOING", # Default value
                value = "0", # Default value
                product = "STOCKS_INVENTORY", # Default value
            )
            return deal
        else:
            return None
        

class DealProgression(models.Model):
    STATUS_CHOICES = [
        ("COMPLETED", "COMPLETED"),
        ("CANCELLED", "CANCELLED"),
        ("ONGOING", "ONGOING"),
        ("RESCHEDULE", "RESCHEDULE"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    trail = ArrayField(models.JSONField(), default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)
    unique_id = models.CharField(max_length=20, blank=True, null=True)
    current_stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True, blank=True)
    pipeline = models.ForeignKey("Pipeline", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    class Meta:
        verbose_name = "DEAL PROGRESSION"
        verbose_name_plural = "DEAL PROGRESSIONS"

    def __str__(self):
        return f"Deal progression for {self.name}"
    

class Activity(models.Model):
    STATUS_CHOICES = [
        ("COMPLETED", "COMPLETED"),
        ("CANCELLED", "CANCELLED"),
        ("ONGOING", "ONGOING"),
        ("RESCHEDULE", "RESCHEDULE"),
    ]

    title = models.CharField(max_length=100)
    activity_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stage_id = models.ManyToManyField(Stage, blank=True, related_name='stage')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True, blank=True, default="ONGOING")
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    def __str__(self) -> str:
        return self.title


class Task(models.Model):
    STATUS_CHOICES = [
        ("COMPLETED", "COMPLETED"),
        ("CANCELLED", "CANCELLED"),
        ("ONGOING", "ONGOING"),
        ("RESCHEDULE", "RESCHEDULE"),
    ]

    title = models.CharField(max_length=255)
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True, null=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True)
    deal_progression = models.ForeignKey(DealProgression, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="uncompleted")
    current_stage = models.ForeignKey(Stage, related_name="todos", on_delete=models.SET_NULL, null=True, blank=True)
    trail = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True, related_name="merchants")
    deadline = models.DateTimeField(blank=True, null=True)
    deadline_reminder = models.BooleanField(default=True)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    def __str__(self):
        return self.task_id


class TaskNotification(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notified_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    def __str__(self):
        return f"Notification for {self.user} about {self.task}"
    

class TeamMemberRole(models.Model):
    ROLES = [
        ("ADMIN", "ADMIN"),
        ("HEAD_OF_SALES", "HEAD_OF_SALES"),
        ("SALES_LEAD", "SALES_LEAD"),
        ("SALES_OFFICER", "SALES_OFFICER"),
        ("MEMBER", "MEMBER"),
    ]

    name = models.CharField(max_length=255, choices=ROLES, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    class Meta:
        verbose_name = "TEAM MEMBER ROLE"
        verbose_name_plural = "TEAM MEMBER ROLES"

        def __str__(self):
            return self.name


# class TeamMemberPermission(models.Model):
#     name = models.CharField(max_length=100, null=True)
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     created_at = models.DateTimeField(_("date created"), auto_now_add=True)
#     updated_at = models.DateTimeField(_("date updated"), auto_now=True)

#     class Meta:
#         verbose_name = "TEAM MEMBER PERMISSION"
#         verbose_name_plural = "TEAM MEMBER PERMISSIONS"

#     def __str__(self):
#         return self.name


# class TeamMemberRolePermission(models.Model):
#     role = models.OneToOneField(TeamMemberRole, on_delete=models.CASCADE, null=True)
#     permission = models.ManyToManyField(TeamMemberPermission, blank=True)
#     merchant = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     created_at = models.DateTimeField(_("date created"), auto_now_add=True)
#     updated_at = models.DateTimeField(_("date updated"), auto_now=True)

#     class Meta:
#         verbose_name = "TEAM MEMBER ROLE PERMISSION"
#         verbose_name_plural = "TEAM MEMBER ROLE PERMISSIONS"

#     def __str__(self):
#         return f"{self.role} Permissions"
    

# class DealsComment(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="comments")
#     sales_officer = models.ForeignKey(SalesOfficer, on_delete=models.CASCADE, related_name="deals_comments")
#     comment = models.TextField()
#     parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
#     show_as_single_comment = models.BooleanField(default=True)
#     created_at = models.DateTimeField(_("date created"), auto_now_add=True)
#     updated_at = models.DateTimeField(_("date updated"), auto_now=True)

#     class Meta:
#         verbose_name = "DEAL COMMENT"
#         verbose_name_plural = "DEAL COMMENTS"

#     def __str__(self):
#         return f"{self.id}"


# # class TaskComment(models.Model):
# #     task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
# #     sales_officer = models.ForeignKey(SalesOfficer, on_delete=models.CASCADE, related_name="task_comments")
# #     comment = models.TextField()
# #     parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
# #     show_as_single_comment = models.BooleanField(default=True)
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     created_at = models.DateTimeField(_("date created"), auto_now_add=True)
# #     updated_at = models.DateTimeField(_("date updated"), auto_now=True)

# #     class Meta:
# #         verbose_name = "TASK COMMENT"
# #         verbose_name_plural = "TASK COMMENTS"

# #     def __str__(self):
# #         return f"{self.id}"    


# # class LeadsDataUpload(models.Model):
# #     leads_file = models.FileField(upload_to="leads_file", blank=True, null=True)
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     created_at = models.DateTimeField(_("date created"), auto_now_add=True)
# #     updated_at = models.DateTimeField(_("date updated"), auto_now=True)

# #     # created_at = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return f"LeadsDataUploaded {self.id}"

# #     class Meta:
# #         verbose_name = "LEADS DATA UPLOAD"
# #         verbose_name_plural = "LEADS DATA UPLOADS"
        

# # class EmaiLog(models.Model):
    
# #     SUCCESS = "success"
# #     FAILURE = "failure"

# #     STATUS_CHOICES = [
# #         ("success", "Success"),
# #         ("failure", "Failure"),
# #     ]

# #     subject = models.CharField(max_length=255, null=True, blank=True)
# #     message = models.TextField(null=True, blank=True)
# #     recipient = models.EmailField()
# #     sender = models.EmailField()
# #     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=FAILURE)
# #     sent_at = models.DateTimeField(auto_now_add=True)
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     created_at = models.DateTimeField(_("date created"), auto_now_add=True)
# #     updated_at = models.DateTimeField(_("date updated"), auto_now=True)

# #     class Meta:
# #         verbose_name = "Email Log"
# #         verbose_name_plural = "Email Logs"

# #     def __str__(self):
# #         return f"Subject: {self.subject}, Recipient: {self.recipient}, Status: {self.status}"


# # class TaskSchedule(models.Model):
# #     pass


# # class Report(models.Model):
# #     pass
    

# # class DealRequirement(models.Model):
# #     custom_fields = ArrayField(models.JSONField(), blank=True, null=True)
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     created_at = models.DateTimeField(_("date created"), auto_now_add=True)
# #     updated_at = models.DateTimeField(_("date updated"), auto_now=True)

# #     class Meta:
# #         verbose_name = "DEAL REQUIREMENT"
# #         verbose_name_plural = "DEAL REQUIREMENTS"

# #         def __str__(self):
# #             return f"{self.id}"


# # class DealPipeline(models.Model):
# #     name = models.CharField(max_length=255)
# #     deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="deal_pipeline")
# #     order = models.IntegerField(default=0)
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     created_at = models.DateTimeField(_("date created"), auto_now_add=True)
# #     updated_at = models.DateTimeField(_("date updated"), auto_now=True)

# #     class Meta:
# #         verbose_name = "DEAL PIPELINE"
# #         verbose_name_plural = "DEAL PIPELINES"


# # class MerchantDealPipeline(models.Model):
# #     merchant = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="merchant_pipeline")
# #     name = models.CharField(max_length=100)
# #     order = models.IntegerField(default=0)
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     created_at = models.DateTimeField(_("date created"), auto_now_add=True)
# #     updated_at = models.DateTimeField(_("date updated"), auto_now=True)

# #     class Meta:
# #         verbose_name = "MERCHANT DEAL PIPELINE"
# #         verbose_name_plural = "MERCHANT DEAL PIPELINES"

# #     def __str__(self):
# #         return self.name

# #     @classmethod
# #     def create_default_pipelines(cls, merchant):
# #         default_pipelines = [
# #             "Qualified",
# #             "Demo Scheduled",
# #             "Proposal Made",
# #             "Invoice",
# #         ]

# #         try:
# #             merchant_pipeline = cls.objects.get(merchant=merchant)
# #             return merchant_pipeline
# #         except cls.DoesNotExist:
# #             pass

# #         for index, pipeline in enumerate(default_pipelines):
# #             merchant_pipeline = cls.objects.create(
# #                 merchant=merchant, name=pipeline, order=index
# #             )
# #         return merchant_pipeline
    
# #     @classmethod
# #     def create_pipeline(cls, merchant, name, order):
# #         merchant_pipeline = cls.objects.create(merchant=merchant, name=name, order=order)
# #         return merchant_pipeline
