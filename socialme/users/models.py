from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    # User,
    # Permission,
)
from typing import Optional
import uuid
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils import timezone
from django.db import IntegrityError, models, transaction
from crmpipeline.helpers.enums import UserRole, UserStatus, TeamType
from django.db.models import Count, F, Q, Sum
# from django.contrib.auth import get_user_model


class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **kwargs):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email) # To convert email to standard email format
        email = email.lower()

        user = self.model(
            email=email,
            username=username,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            **kwargs
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """User model."""

    CHANNEL = [
        ("USSD", "USSD"),
        ("WEB", "WEB"),
        ("MOBILE", "MOBILE"),
        ("POS", "POS"),
    ]

    default_company = models.ForeignKey(
        "Company",
        on_delete=models.SET_NULL,
        related_name="default_company",
        null=True,
        blank=True,
    )

    email = models.EmailField(max_length=255, unique=True,)
    username = models.CharField(max_length=255, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    has_company = models.BooleanField(default=False)

    channel = models.CharField(
        max_length=200, choices=CHANNEL, default="WEB", null=True, blank=True
    )


    # groups = models.ManyToManyField(User, related_name='useraccount_groups')  # Added related_name argument
    # groups = models.ManyToManyField(get_user_model(), related_name='useraccount_groups')
    # user_permissions = models.ManyToManyField(Permission, related_name='useraccount_user_permissions')  # Added related_name argument
    # user_permissions = models.ManyToManyField(Permission, related_name='useraccount_user_permissions')  # Added related_name argument

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "USER PROFILE"
        verbose_name_plural = "USER PROFILES"
    

class Company(models.Model):

    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="company_owner",
        blank=True, null=True
    )
    teams = models.ManyToManyField(
        "Team", blank=True, related_name="company_related_teams"
    )
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    sales_officer = models.ForeignKey(
        "SalesOfficer",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "COMPANY"
        verbose_name_plural = "COMPANIES"

    def __str__(self):
        return str(self.company_name)


    @classmethod
    def create_company(cls, user, validated_data):

        company = cls.objects.create(
            user=user,
            company_name=validated_data.get("company_name").title(),
            industry=validated_data.get("industry"),
            is_active=True,
        )
        return company

    @classmethod
    def retrieve_company(cls, id: str, user: Optional[UserAccount] = None):  # type: ignore
        """
        Retrieve a company using its ID and associated user if provided.
        Args:
            id (str): The ID of the company to retrieve.
            user (User, optional): The user associated with the company.
        Returns:
            Company or None: The retrieved Company object if found and active, or None if not found.
        """
        try:
            if user is not None:
                company = cls.objects.get(id=id, user=user, is_active=True)
            else:
                company = cls.objects.get(id=id, is_active=True)
        except cls.DoesNotExist:
            company = None
        return company
    

class SalesLead(models.Model):
    STOCKS_INVENTORY = 'SI'
    SALES = 'SA'
    SPEND_MANAGEMENT = 'SM'
    HR_MANAGEMENT = 'HRM'

    PRODUCT_VERTICALS_CHOICES = [
        (STOCKS_INVENTORY, 'Stock Inventory & Stock Management'),
        (SALES, 'Sales'),
        (SPEND_MANAGEMENT, 'Spend Management'),
        (HR_MANAGEMENT, 'HR Management'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    name = models.CharField(max_length=255)
    is_sales_lead = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    date_hired = models.DateField(default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    def __str__(self):
        return self.name

    # @property
    # def active_merchants_percentage(self):
    #     total_merchants = self.active_merchants_count + self.inactive_merchants_count
    #     return (self.active_merchants_count / total_merchants) * 100 if total_merchants > 0 else 0

    # @property
    # def inactive_merchants_percentage(self):
    #     total_merchants = self.active_merchants_count + self.inactive_merchants_count
    #     return (self.inactive_merchants_count / total_merchants) * 100 if total_merchants > 0 else 0

    # @property
    # def active_vs_inactive_comparison_ratio(self):
    #     return f"{self.active_merchants_count}:{self.inactive_merchants_count}"


class SalesOfficer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    sales_lead = models.ForeignKey(SalesLead, on_delete=models.CASCADE, related_name='sales_officers')
    name = models.CharField(max_length=255)
    is_sales_officer = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    date_hired = models.DateField(default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    def __str__(self):
        return self.name

    # @property
    # def active_merchants_percentage(self):
    #     total_merchants = self.active_merchants_count + self.inactive_merchants_count
    #     return (self.active_merchants_count / total_merchants) * 100 if total_merchants > 0 else 0

    # @property
    # def inactive_merchants_percentage(self):
    #     total_merchants = self.active_merchants_count + self.inactive_merchants_count
    #     return (self.inactive_merchants_count / total_merchants) * 100 if total_merchants > 0 else 0

    # @property
    # def active_vs_inactive_comparison_ratio(self):
    #     return f"{self.active_merchants_count}:{self.inactive_merchants_count}"
    

class HeadOfSales(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="team_owner")
    team_name = models.CharField(max_length=255)
    team_type = models.CharField(
        max_length=255, choices=TeamType.choices, default=TeamType.SPEND_MGMT
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company"
    )
    members = models.ManyToManyField("TeamMember", blank=True, related_name="members")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "TEAM"
        verbose_name_plural = "TEAMS"

    def __str__(self):
        return self.team_name

    @classmethod
    def create_team(
        cls,
        user: object,
        team_name: str,
        members: list,
        company_id: str,
        team_type: Optional[str] = None,
    ):
        from users.models import TeamMember
        req_team_name = team_name.title()

        with transaction.atomic():
            try:
                team_ins = cls.objects.create(
                    user=user,
                    company_id=company_id,
                    team_name=req_team_name,
                    team_type="SPEND_MGMT" if team_type is None else team_type,
                )
                TeamMember.create_and_add_team_members_to_expected_team(
                    members=members, team_ins=team_ins
                )
                company = team_ins.company
                company.teams.add(team_ins)
                company.save()
                # print(team_ins)
                return {"status": True, "team": team_ins}
            except IntegrityError as error:
                return {
                    "status": False,
                    "message": f"Team type {team_type} exists already in the company's branch.",
                }

    @classmethod
    def update_team(cls, validated_data):
        _team_id = validated_data["team_id"]
        members = validated_data["members"]
        team_name = validated_data["team_name"]

        team_ins = cls.objects.get(id=_team_id)
        TeamMember.create_and_add_team_members_to_expected_team(
            members=members, team_ins=team_ins
        )
        if team_name:
            team_ins.team_name = team_name.title()
            team_ins.save()
        else:
            pass

        return True

    @classmethod
    def add_team_members(cls, company_ins, members):
        from crmpipeline.tasks import send_email

        for member in members:
            email = member["email"]
            member = TeamMemberInvite.objects.create(
                email=email,
                company=company_ins,
            )
            send_email.delay(
                recipient=email,
                subject="Member Invite",
                # template_dir="non_registered_team_member_invite.html",
                # call_back_url=f"https://www.paybox360.com/sign-up/get-started",
                company_name=company_ins.company_name,
            )

        return True
    

class TeamMember(models.Model):
    member = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        # related_name="team_member",
        null=True,
        blank=True,
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone_no = models.CharField(max_length=255, null=True, blank=True)
    is_registered = models.BooleanField(default=False)
    status = models.CharField(
        max_length=255, choices=UserStatus.choices, null=True, blank=True
    )
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="team"
    )
    role = models.CharField(
        max_length=255, choices=UserRole.choices, default=UserRole.MEMBER
    )
    req_no = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.email)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "TEAM MEMBER"
        verbose_name_plural = "TEAM MEMBERS"

    @classmethod
    def member_exists(cls, email, team_ins=None):

        if team_ins is None:
            mem = cls.objects.filter(email=email)
        else:
            # print("email and team instance check")
            mem = cls.objects.filter(email=email, team_id=team_ins.id)

        if mem.aggregate(count=Count("id"))["count"] > 0:
            return mem
        else:
            return None

    @classmethod
    def create_and_add_team_members_to_expected_team(cls, members, team_ins):
        created_team_members = []
        for member in members:
            email = member.get("email")
            phone_no = member.get("phone_no")
            role = member.get("role")

            team_member = cls.member_exists(email=email, team_ins=team_ins)

            if team_member is not None:
                continue

            user = UserAccount.user_exist(email=email, phone_no=phone_no)
            member = cls.objects.create(
                email=email,
                phone_no=phone_no,
                member=user if user is not None else None,
                team=team_ins,
                is_registered=True if user is not None else False,
                status="NOT_JOINED" if not user else "ACTIVE",
                role="MEMBER" if not role else role,
                channel=team_ins.channel,
            )
            created_team_members.append(member)

        team_ins.members.add(*created_team_members)


class TeamMemberInvite(models.Model):
    email = models.EmailField(null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    class Meta:
        verbose_name = "TEAM MEMBER INVITATION"
        verbose_name_plural = "TEAM MEMBER INVITATIONS"

    def __str__(self):
        return str(self.email)


class OneTimePassword(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.username} - otp code"