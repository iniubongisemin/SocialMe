from rest_framework import serializers
from users.serializers import CompanySerializer
from users.models import Company, TeamMember
from crmpipeline.models import (SalesOfficer, Activity, Deal, DealProgression, Pipeline, Stage, Task, \
    TaskNotification, TeamMemberPermission, TeamMemberRole, TeamMemberRolePermission, Lead, # LeadsDataUpload,
    )


class StageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stage
        fields = ('name', #'move_criteria', \
                  'is_new_merchant', 'order', 'email_subject', 'email_body', 'email_text',
                  'email_notifications_enabled', 'merchant_count', 'automation_enabled')

class SalesOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOfficer
        fields = ['user', 'sales_lead', 'name', 'email', 'product_vertical']
        read_only_fields = ['user', 'sales_lead', 'referral_code', 'product_vertical']
        exclude = ['product_vertical', 'user']

class DealSerializer(serializers.ModelSerializer):
    merchant = CompanySerializer()
    sales_officer = SalesOfficerSerializer()
    # team_member = 'TeamMemberSerializer'
    # pipeline = 'PipelineSerializer'

    # def get_fields(self):
    #     fields = super(DealSerializer, self).get_fields()
    #     return fields

    def get_fields(self):
        fields = super().get_fields()
        fields['team_member'] = TeamMemberSerializer()
        fields['pipeline'] = PipelineSerializer()
        return fields

    class Meta:
        model = Deal
        fields = (
            'deal_title', 'description', 'merchant', 'sales_officer', 'label', 'industry',
            'deal_status', 'team_member', 'pipeline_type', 'pipeline', 'contact_person', 'value', 
            'product', 'start_date', 'updated_at', 'expected_close_date', 'phone_num', 'email'
        )


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = (
        "id", "name", "phone_number", "email_address", "company",
        "stage", "address", "label",
    )


class PipelineSerializer(serializers.ModelSerializer):
    stages = StageSerializer()
    deals = DealSerializer()
    sales_officer = SalesOfficerSerializer()
    merchant = CompanySerializer()

    class Meta:
        model = Pipeline
        fields = (
            "name", "stages", "deals", "sales_officer", "merchant", "is_default", #"automation_enabled"
        )


class DealProgressionStageSerializer(serializers.ModelSerializer):
    deal = DealSerializer()
    current_stage = StageSerializer()
    pipeline = PipelineSerializer()

    class Meta:
        model = DealProgression
        fields = ('id', 'deal', 'name', 'email', 'trail', 'status', 'current_stage', 'pipeline')


class ActivitySerializer(serializers.ModelSerializer):
    pipeline = PipelineSerializer()
    stage = StageSerializer()

    class Meta:
        model = Activity
        fields = ('title', 'pipeline', 'stage', 'status')


class TaskSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    current_stage = StageSerializer()
    # created_by = UserSerializer()
    merchant = CompanySerializer()

    class Meta:
        model = Task
        fields = ('title', 'activity', 'description', 'due_date', 'task_id', 'status', 'current_stage', 'trail',
                  'created_by', 'merchant')


class TaskNotificationSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    # user = UserSerializer()

    class Meta:
        model = TaskNotification
        fields = ('task','user','notified_at','message')


class TeamMemberRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberRole
        fields = 'name'


class TeamMemberPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberPermission
        fields = 'name'


class TeamMemberRolePermissionSerializer(serializers.ModelSerializer):
    role = TeamMemberRoleSerializer()
    permission = TeamMemberPermissionSerializer(many=True)
    merchant = CompanySerializer()

    class Meta:
        model = TeamMemberRolePermission
        fields = ('role', 'permission', 'merchant')


class TeamMemberSerializer(serializers.ModelSerializer):
    merchant = CompanySerializer()
    member = SalesOfficerSerializer()
    role = TeamMemberRolePermissionSerializer()

    class Meta:
        model = TeamMember
        fields = ('merchant', 'permission', 'role')

    # class Serializer(serializers.ModelSerializer):
#
#     class Meta:
#         model =
#         fields = "__all__"
#
        

class NewTeamMemberSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()
    role_id = serializers.SerializerMethodField()
    permission_names = serializers.SerializerMethodField()
    permission_ids = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = ["id", "member", "role", "role_name", "role_id", "permission_names", "permission_ids"]
        depth = 1

    def get_role_name(self, obj):
        return obj.role.role.name if obj.role.role else None

    def get_role_id(self, obj):
        return obj.role.role.id if obj.role.role else None

    def get_permission_names(self, obj):
        return [p.name for p in obj.role.permission.all()] if obj.role else []

    def get_permission_ids(self, obj):
        return [p.id for p in obj.role.permission.all()] if obj.role else []

    def validate(self, data):
        sales_officer = SalesOfficer.objects.get(user=self.context["request"].user)

        member = data.get("member")
        if member and member.company != sales_officer.company:
            raise serializers.ValidationError(
                "Team member must belong to the same company as the recruiter."
            )

        return data

    def to_representation(self, instance):
        data = super(NewTeamMemberSerializer, self).to_representation(instance)
        data["member"] = SalesOfficer(instance.member).data

        return data
    

class CreateDealSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    industry = serializers.CharField(required=False, allow_blank=True)
    deal_status = serializers.ChoiceField(choices=Deal.DEAL_STATUS, required=False, allow_null=True)
    team_member = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True)
    merchant_overview = serializers.CharField(required=False, allow_blank=True)
    # pipeline_type = serializers.ChoiceField(choices=Deal.PIPELINE_TYPE_CHOICES, required=False, allow_null=True)
    deal_start_date = serializers.DateTimeField(required=True)
    deal_deadline = serializers.DateTimeField(required=True)
    deal_type = serializers.CharField(required=False)

    def create(self, validated_data):
        deal_tags = validated_data.pop("job_tags", None)
        deal = Deal.objects.create(**validated_data)
        if deal_tags:
            deal.deal_tags = deal_tags
            deal.save()
        return deal


class CreateMerchantSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    merchant = CompanySerializer()

    class Meta:
        model = Company
        fields = ('id', 'name')


class ChangeDealStageSerializer(serializers.ModelSerializer):
    deal_id = serializers.IntegerField(required=True)
    stage_id = serializers.IntegerField(required=True)


class OnboardSalesOfficerSerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    sales_lead = serializers.CharField()
    email = serializers.CharField()
    company = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = SalesOfficer
        fields = [
            "sales_lead", 
            "name",
            "email", 
            "role", 
            "company", 
        ]


# class LeadsDataUploadSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = LeadsDataUpload
#         fields = 'leads_file'