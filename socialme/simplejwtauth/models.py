from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.translation import gettext as _
from typing import Optional
from django.conf import settings
from django.utils import timezone


# Create your models here.

from django.db import models, IntegrityError, transaction
# from crmpipeline.helpers.enums import UserRole, UserStatus, TeamType
# from django.db.models import Count, F, Q, Sum
# # from django.contrib.auth import get_user_model


class Company(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="company_owner",
        blank=True, null=True
    )
    # teams = models.ManyToManyField(
    #     "Team", blank=True, related_name="company_related_teams"
    # )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    sales_officer = models.ForeignKey(
        "SalesOfficer",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "COMPANY"
        verbose_name_plural = "COMPANIES"

    def __str__(self):
        return str(self.company_name)


    @classmethod
    def create_company(cls, validated_data):

        company = cls.objects.create(
            user=validated_data.get("id"),
            company_name=validated_data.get("company_name").title(),
            industry=validated_data.get("industry"),
            is_active=True,
        ) 

        company.save()
        return company

    @classmethod
    def retrieve_company(cls, id: str, user: Optional[User] = None):  # type: ignore
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
    

class SuperAdmin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    def __str__(self):
        return f"Super Admin: {self.first_name} {self.last_name}"


class HeadOfSales(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    super_admin = models.ForeignKey(SuperAdmin, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Head of Sales: {self.first_name} {self.last_name}"


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
    head_of_sales = models.ForeignKey("HeadOfSales", on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    date_hired = models.DateField(default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    def __str__(self):
        return f"Sales Lead: {self.first_name} {self.last_name}"


class SalesOfficer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    sales_lead = models.ForeignKey(SalesLead, on_delete=models.CASCADE, related_name='sales_officers')
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    date_hired = models.DateField(default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    def __str__(self):
        return f"Sales Officer: {self.first_name} {self.last_name}"
    


# class OneTimePassword(models.Model):
#     user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
#     otp = models.CharField(max_length=6)

#     def __str__(self):
#         return f"{self.user.username} - otp code"