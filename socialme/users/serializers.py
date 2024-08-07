from djoser.serializers import UserCreateSerializer
from users.models import (
    UserAccount, Company, Team, TeamMember, TeamMemberInvite, SalesLead, SalesOfficer, HeadOfSales, SuperAdmin) 
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
import re
from rest_framework.exceptions import PermissionDenied

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
    company_name = serializers.CharField(allow_blank=True, allow_null=True)
    # id = serializers.CharField(allow_blank=True, allow_null=True)
    # teams = serializers.CharField(allow_blank=True, allow_null=True)
    # industry = serializers.CharField(allow_blank=True, allow_null=True)
    

    class Meta:
        model = Company
        fields = [
            "company_name",
            "user",
            # "id",
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


class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['name', 'email']


class HeadOfSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadOfSales
        fields = ['name', 'email', 'super_admin']


class SalesLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesLead
        fields = ['name', 'email', 'head_of_sales']


class SalesOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOfficer
        fields = ['name', 'email', 'sales_lead']
        # fields = ['user', 'sales_lead', 'name', 'email']
        # read_only_fields = ['user', 'sales_lead']


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


class CreateUpdateTeamSerializer(serializers.Serializer):
    team_name = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    team_id = serializers.UUIDField(required=False, allow_null=True)
    team_type = serializers.CharField(required=False)
    company_id = serializers.UUIDField(required=False, allow_null=True)
    members = serializers.ListField(child=serializers.JSONField())

    def validate(self, attrs):
        context = self.context
        company_id = attrs.get("company_id")
        team_id = attrs.get("team_id")
        team_name = attrs.get("team_name").title()
        members = attrs.get("members", [])
        user = context.get("user")

        # Verify Email
        email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
        invalid_emails = [
            member.get("email")
            for member in members
            if not member.get("email") or not email_pattern.match(member.get("email"))
        ]

        if invalid_emails:
            raise serializers.ValidationError({"email": "A valid email is required"})

        # validate company properties if method is create team ----------------------------------------->
        if context.get("create_team") is True:
            if not company_id:
                raise serializers.ValidationError(
                    {"company_id": "Company ID is required"}
                )

            if not team_name:
                raise serializers.ValidationError(
                    {"team_name": "team_name is required"}
                )

            company = Company.objects.filter(pk=company_id)

            if not company:
                raise serializers.ValidationError({"message": "Invalid company"})

            company_instance = company.last()

            if user != company_instance.user:
                admin_roles = ["SUPER_ADMIN", "SALES_LEAD", "HEAD_OF_SALES"]

                user_in_super_admin_roles = TeamMember.objects.filter(
                    team__company=company_instance,
                    member=user,
                    role__in=admin_roles,
                )
                if not user in admin_roles:
                    raise PermissionDenied(
                        "You do not have the necessary permissions to perform this action"
                    )

            existing_teams = Team.objects.filter(
                team_name=team_name, company=company_instance
            )

            # print(existing_teams, "\n\n")

            if existing_teams.exists():
                raise serializers.ValidationError(
                    {"message": f"You have an existing team name {team_name}"}
                )

        # ------------------------------------------------------------------------------------------------->

        # If view method is update team then the following will be required to also validate
        # properties required to

        if context.get("create_team") is False:
            if not team_id:
                raise serializers.ValidationError({"team_id": "Team ID is required"})
            try:
                team_ins = Team.objects.get(pk=team_id)
            except Team.DoesNotExist:
                raise serializers.ValidationError({"message": "Invalid Team"})

            for member in members:
                email = member.get("email")
                team_member = TeamMember.member_exists(email=email, team_ins=team_ins)
                if (
                    team_member
                ):  # validate that user does not add a user that already exist
                    raise serializers.ValidationError(
                        {"message": "Team member exists on selected team"}
                    )
                else:
                    pass

            # Retrieve all emails from members
            emails = [member.get("email") for member in members if member.get("email")]

            # Check if any team member with the given emails already exists
            existing_members = TeamMember.objects.filter(
                email__in=emails, team=team_ins
            )
            if existing_members.exists():
                raise serializers.ValidationError(
                    {"message": "Team member exists on selected team"}
                )

        return attrs
    

class OnboardSuperAdminSerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    email = serializers.CharField()
    company = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = SuperAdmin
        fields = [
            "name",
            "email", 
            "role", 
            "company", 
        ]
    

class OnboardHeadOfSalesSerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    email = serializers.CharField()
    company = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = HeadOfSales
        fields = [
            "name",
            "email", 
            "role", 
            "company", 
        ]


class OnboardSalesLeadSerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    email = serializers.CharField()
    company = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = SalesLead
        fields = [
            "name",
            "email", 
            "role", 
            "company", 
        ]


class OnboardSalesOfficerSerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    email = serializers.CharField()
    company = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = SalesLead
        fields = [
            "name",
            "email", 
            "role", 
            "company", 
        ]