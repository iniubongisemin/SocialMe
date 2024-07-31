from djoser.serializers import UserCreateSerializer
from .models import (
    UserAccount, Company, Team, TeamMember, TeamMemberInvite,  #, SalesLead, SalesOfficer, \
    ) 
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserCreateSerializer(UserCreateSerializer):
    class Meta (UserCreateSerializer.Meta):
        model = UserAccount
        fields= ('id', 'email', 'password', 'username')

class UserOTPSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=6)

    class Meta:
        model = UserAccount
        fields = ['otp']

class UserAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'password', 'username']
        extra_kwargs = {'password': {'write_only': True}}
        error_messages = {
            'email': {
                'invalid': ("Enter a valid email."),
                'unique': ("user with this email address already exists.")
            },
        }
        

    def validate_email(self, value):
        if UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError()
        return value

    def validate_password(self, value):
        validate_password(value)
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for char in value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def create(self, validated_data):
        user = UserAccount.objects.create_user(**validated_data)
        return user
    
    def validate(self, attrs):
        # Performing otp validation
        email = attrs.get('email')
        otp = attrs.get('otp')

        try:
            user = UserAccount.objects.get(email=email)
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError({'error': 'User with this email does not exist.'})
        
        if user.otp != otp:
            raise serializers.ValidationError({'error': 'Invalid OTP.'})
        
        # Resetting the OTP field after successful validation
        user.otp = None
        user.save()

        return attrs
    

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "company_name")


class CreateCompanySerializer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=255)
    # teams = serializers.CharField(allow_blank=True, allow_null=True)
    company_name = serializers.CharField(allow_blank=True, allow_null=True)
    # industry = serializers.CharField(allow_blank=True, allow_null=True)
    id = serializers.CharField(allow_blank=True, allow_null=True)
    

    class Meta:
        model = Company
        fields = [
            "company_name",
            "id",
            "user"
        ]
        # exclude = ['user']

    def validate(self, attrs):
        context = self.context
        request = context.get("request")
        user = request.user
        company_name = attrs.get("company_name").title()

        try:
            Company.objects.get(company_name=company_name, user=user)
            raise serializers.ValidationError(
                {"message": "Company name already exists"}
            )

        except Company.DoesNotExist:
            pass


# class SalesLeadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesLead
#         fields = ['name', 'email']


# class SalesOfficerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesOfficer
#         fields = ['user', 'sales_lead', 'name', 'email']
#         read_only_fields = ['user', 'sales_lead']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "team_name",)


class TeamMemberSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="member.email", allow_null=True)
    team_name = serializers.CharField(source="team.team_name", allow_null=True)
    company_name = serializers.CharField(
        source="team.company.company_name", allow_null=True
    )

    class Meta:
        model = TeamMember
        fields = (
            "id",
            "email",
            "team",
            "company_name",
            "role",
            "is_registered",
            "created_at",
            "status",
            "phone_no",
        )


class MembersInviteSerializer(serializers.Serializer):
    # members = serializers.ListSerializer(child=TeamEmailSerializer())

    def validate(self, attrs):
        company = self.context.get("company")
        members = attrs.get("members")
        if len(members) < 1:
            raise serializers.ValidationError({"members": "members cannot be empty"})
        get_members = TeamMemberInvite.objects.filter(company=company)

        team_member_emails = [member.email for member in get_members]

        existing_emails = [
            email["email"] for email in members if email["email"] in team_member_emails
        ]
        if existing_emails:
            raise serializers.ValidationError(
                {"message": "members already exists", "data": existing_emails}
            )
        return attrs


