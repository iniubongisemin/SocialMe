from rest_framework import serializers
from simplejwtauth.serializers import CreateCompanySerializer
from crmpipeline.models import (
    Deal, Pipeline, Stage, Activity, Task, Lead, 
    #TaskNotification, DealProgression, TeamMemberRole, 
    #TeamMemberPermission, TeamMemberRolePermission, LeadsDataUpload,
)
from simplejwtauth.serializers import SalesOfficerSerializer
from simplejwtauth.models import SalesOfficer


class StageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stage
        fields = ('name', 'order', 'merchant_count',)
        
        # (
                    # 'name', 'order', 'merchant_count', # 'pipeline',  
                    #'email_subject', 'email_body', 
                    #'email_text', 'email_notifications_enabled', 
                    # 'automation_enabled', 'move_criteria',
                # )
        

class DealSerializer(serializers.ModelSerializer):
    merchant = CreateCompanySerializer()
    sales_officer = SalesOfficerSerializer()


    # def get_fields(self):
    #     fields = super(DealSerializer, self).get_fields()
    #     return fields

    def get_fields(self):
        fields = super().get_fields()
        fields['pipeline'] = PipelineSerializer()
        # fields['team_member'] = TeamMemberSerializer()
        return fields

    class Meta:
        model = Deal
        fields = (
            'deal_title', 'description', 'merchant', 'sales_officer', 'phone_num', 'user',
            'industry', 'current_stage', 'contact_person', 'pipeline',  
            'value', 'product', 'start_date', 'updated_at', 'expiry_date', 
            'email', 'label', 'deal_status',
            "label", "deal_status" 
             # 'team_member', 'deal_id', 'trail', 'pipeline_type', 
        )

class CreateDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = (
            'deal_title', 'description', 'merchant', 'sales_officer', 'phone_num', 'user',
            'industry', 'current_stage', 'value', 'product', 'start_date', 'updated_at', 'expiry_date', 
            'email', 'label', 'deal_status', 
        )
        


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = (
        "name", "phone_number", "email_address", 
        "company", "stage", "address", "label", "sales_officer",
    )


class PipelineSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True, required=False)
    # deals = DealSerializer()
    # sales_officer = SalesOfficerSerializer()
    # merchant = CreateCompanySerializer()

    class Meta:
        model = Pipeline
        fields = (
            "name", "pipeline_type", "stages" # "pipeline_id", # "automation_enabled"
        )
        read_only_fields = ["stages"]
        depth = 1

    def create(self, validated_data):
        stages_data = validated_data.pop('stages', [])
        pipeline = Pipeline.objects.create(**validated_data)
        
        for stage_data in stages_data:
            stage = Stage.objects.create(**stage_data)
            pipeline.stages.add(stage)

        return pipeline


class ActivitySerializer(serializers.ModelSerializer):
    # pipeline = PipelineSerializer()
    # stage = StageSerializer()

    class Meta:
        model = Activity
        fields = (
                'title', 'deal',
                 # 'pipeline', 'status',
            )
        
        # def __str__(self) -> str:
        #     fields = ("title", "stage_id")
        #     stage_id = "('%s')"%",".join(fields)
            
        #     return stage_id


class TaskSerializer(serializers.ModelSerializer):
    # activity = ActivitySerializer()
    # current_stage = StageSerializer()
    # merchant = CreateCompanySerializer()
    # created_by = UserSerializer()

    class Meta:
        model = Task
        fields = (
                    'title', 'activity_id', 'description', # 'created_by',
                    # 'deal', 'due_date', 'status', 'current_stage', 
                    # 'created_by', 'merchant', 'trail', 
                )


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



# class SalesOfficerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesOfficer
#         fields = ['user', 'sales_lead', 'name', 'email', 'product_vertical']
#         read_only_fields = ['user', 'sales_lead', 'referral_code', 'product_vertical']
#         exclude = ['product_vertical', 'user']
        

# class DealProgressionStageSerializer(serializers.ModelSerializer):
#     deal = DealSerializer()
#     current_stage = StageSerializer()
#     pipeline = PipelineSerializer()

#     class Meta:
#         model = DealProgression
#         fields = ('id', 'deal', 'name', 'email', 'trail', 'status', 'current_stage', 'pipeline')
# class TaskNotificationSerializer(serializers.ModelSerializer):
#     task = TaskSerializer()
#     # user = UserSerializer()

#     class Meta:
#         model = TaskNotification
#         fields = ('task','user','notified_at','message')


# class TeamMemberRoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TeamMemberRole
#         fields = 'name'


# class TeamMemberPermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TeamMemberPermission
#         fields = 'name'


# class TeamMemberRolePermissionSerializer(serializers.ModelSerializer):
#     role = TeamMemberRoleSerializer()
#     permission = TeamMemberPermissionSerializer(many=True)
#     merchant = CreateCompanySerializer()

#     class Meta:
#         model = TeamMemberRolePermission
#         fields = ('role', 'permission', 'merchant')


# class TeamMemberSerializer(serializers.ModelSerializer):
#     merchant = CreateCompanySerializer()
#     member = SalesOfficerSerializer()
#     role = TeamMemberRolePermissionSerializer()

#     class Meta:
#         model = TeamMember
#         fields = ('merchant', 'permission', 'role')

#     # class Serializer(serializers.ModelSerializer):
# #
# #     class Meta:
# #         model =
# #         fields = "__all__"
# #
        

# class NewTeamMemberSerializer(serializers.ModelSerializer):
#     role_name = serializers.SerializerMethodField()
#     role_id = serializers.SerializerMethodField()
#     permission_names = serializers.SerializerMethodField()
#     permission_ids = serializers.SerializerMethodField()

#     class Meta:
#         model = TeamMember
#         fields = ["id", "member", "role", "role_name", "role_id", "permission_names", "permission_ids"]
#         depth = 1

#     def get_role_name(self, obj):
#         return obj.role.role.name if obj.role.role else None

#     def get_role_id(self, obj):
#         return obj.role.role.id if obj.role.role else None

#     def get_permission_names(self, obj):
#         return [p.name for p in obj.role.permission.all()] if obj.role else []

#     def get_permission_ids(self, obj):
#         return [p.id for p in obj.role.permission.all()] if obj.role else []

#     def validate(self, data):
#         sales_officer = SalesOfficer.objects.get(user=self.context["request"].user)

#         member = data.get("member")
#         if member and member.company != sales_officer.company:
#             raise serializers.ValidationError(
#                 "Team member must belong to the same company as the recruiter."
#             )

#         return data

#     def to_representation(self, instance):
#         data = super(NewTeamMemberSerializer, self).to_representation(instance)
#         data["member"] = SalesOfficer(instance.member).data

#         return data
    



# class CreateMerchantSerializer(serializers.ModelSerializer):
#     name = serializers.CharField()
#     merchant = CreateCompanySerializer()

#     class Meta:
#         model = Company
#         fields = ('id', 'name')


# class ChangeDealStageSerializer(serializers.ModelSerializer):
#     deal_id = serializers.IntegerField(required=True)
#     stage_id = serializers.IntegerField(required=True)




# class LeadsDataUploadSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = LeadsDataUpload
#         fields = 'leads_file'