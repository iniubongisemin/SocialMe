from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
import django_filters
from crmpipeline.models import Deal, TeamMemberRole 
# from crmpipeline.serializers import OnboardSalesOfficerSerializer
from simplejwtauth.serializers import (
    OnboardSuperAdminSerializer, OnboardHeadOfSalesSerializer,  
    OnboardSalesLeadSerializer, OnboardSalesOfficerSerializer, 
    SuperAdminSerializer, HeadOfSalesSerializer, SalesLeadSerializer, 
    SalesOfficerSerializer,
)
from simplejwtauth.models import (
    Company, HeadOfSales, 
    SuperAdmin, SalesLead, 
    SalesOfficer, # TeamMember 
)


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class extending PageNumberPagination.
    Provides paginated response with next and previous page numbers (instead of links).

    Attributes:
        page_size (int): Default items per page.
        page_size_query_param (str): Query parameter for items per page.
        max_page_size (int): Maximum items per page.
        page_query_param (str): Query parameter for page number.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(self, data):
        """
        Generate Response object with pagination metadata and paginated data.

        Args:
            data (list): List of items for the paginated response.
        """

        # return Response(
        #     {
        #         "next": self.page.next_page_number() if self.page.has_next() else None,
        #         "previous": self.page.previous_page_number()
        #         if self.page.has_previous()
        #         else None,
        #         "count": self.page.paginator.count,
        #         "results": data,
        #     }
        # )
        return Response(
            {
                "page": self.page.next_page_number() if self.page.has_next() else None,
                "count": self.page.paginator.count,
                "results": data,
            }
        )
    
class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = "page_size"
    max_page_size = 100  # Maximum number of items per page


def status_code():
    """
    REST status codes
    """
    code = {
        200: status.HTTP_200_OK,
        201: status.HTTP_201_CREATED,
        202: status.HTTP_202_ACCEPTED,
        203: status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
        204: status.HTTP_204_NO_CONTENT,
        205: status.HTTP_205_RESET_CONTENT,
        206: status.HTTP_206_PARTIAL_CONTENT,
        207: status.HTTP_207_MULTI_STATUS,
        208: status.HTTP_208_ALREADY_REPORTED,
        226: status.HTTP_226_IM_USED,
        300: status.HTTP_300_MULTIPLE_CHOICES,
        301: status.HTTP_301_MOVED_PERMANENTLY,
        302: status.HTTP_302_FOUND,
        303: status.HTTP_303_SEE_OTHER,
        304: status.HTTP_304_NOT_MODIFIED,
        305: status.HTTP_305_USE_PROXY,
        306: status.HTTP_306_RESERVED,
        307: status.HTTP_307_TEMPORARY_REDIRECT,
        308: status.HTTP_308_PERMANENT_REDIRECT,
        400: status.HTTP_400_BAD_REQUEST,
        401: status.HTTP_401_UNAUTHORIZED,
        402: status.HTTP_402_PAYMENT_REQUIRED,
        403: status.HTTP_403_FORBIDDEN,
        404: status.HTTP_404_NOT_FOUND,
        405: status.HTTP_405_METHOD_NOT_ALLOWED,
        406: status.HTTP_406_NOT_ACCEPTABLE,
        407: status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
        408: status.HTTP_408_REQUEST_TIMEOUT,
        409: status.HTTP_409_CONFLICT,
        410: status.HTTP_410_GONE,
        411: status.HTTP_411_LENGTH_REQUIRED,
        412: status.HTTP_412_PRECONDITION_FAILED,
        413: status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        414: status.HTTP_414_REQUEST_URI_TOO_LONG,
        415: status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        416: status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
        417: status.HTTP_417_EXPECTATION_FAILED,
        422: status.HTTP_422_UNPROCESSABLE_ENTITY,
        423: status.HTTP_423_LOCKED,
        424: status.HTTP_424_FAILED_DEPENDENCY,
        426: status.HTTP_426_UPGRADE_REQUIRED,
        428: status.HTTP_428_PRECONDITION_REQUIRED,
        429: status.HTTP_429_TOO_MANY_REQUESTS,
        431: status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
        451: status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
    }
    return code


class DealFilter(django_filters.FilterSet):
    class Meta:
        model = Deal
        fields = {
            "deal_title": ["exact"],
            "description": ["exact"],
        }


def onboard_super_admin(data, user):
    serializer = OnboardSuperAdminSerializer(data=data)
    print(data)
    serializer.is_valid(raise_exception=True)

    # print(serializer.data)
    merchant = serializer.validated_data["company"]
    company_email = data.get("company_email", None)
    role = serializer.validated_data["role"]

    try:
        merchant = Company.objects.get(id=merchant)
    except Company.DoesNotExist:
        return {
            "success": False,
            "message": "Company does not exist",
            "status": status.HTTP_404_NOT_FOUND,
        }
    
    try:
        SuperAdmin.objects.get(user=user, merchant=merchant)
        return {
            "success": False,
            "message": "Super Admin already onboarded",
            "status": status.HTTP_404_NOT_FOUND,
        }
    except SuperAdmin.DoesNotExist:
        pass

    super_admin_instance = SuperAdmin.objects.create(
        user=user,
        merchant=merchant,
        role=role,
    )

    if super_admin_instance and super_admin_instance.verified == True:
        super_admin_instance.save()

    user.save()


def onboard_head_of_sales(data, user):
    serializer = OnboardHeadOfSalesSerializer(data=data)
    print(data)
    serializer.is_valid(raise_exception=True)

    # print(serializer.data)
    merchant = serializer.validated_data["company"]
    company_email = data.get("company_email", None)
    role = serializer.validated_data["role"]

    try:
        merchant = Company.objects.get(id=merchant)
    except Company.DoesNotExist:
        return {
            "success": False,
            "message": "Company does not exist",
            "status": status.HTTP_404_NOT_FOUND,
        }
    
    try:
        HeadOfSales.objects.get(user=user, merchant=merchant)
        return {
            "success": False,
            "message": "Head of sales already onboarded",
            "status": status.HTTP_404_NOT_FOUND,
        }
    except HeadOfSales.DoesNotExist:
        pass

    head_of_sales_instance = HeadOfSales.objects.create(
        user=user,
        merchant=merchant,
        role=role,
    )

    if head_of_sales_instance and head_of_sales_instance.verified == True:
        head_of_sales_instance.save()

    user.save()


def onboard_sales_lead(data, user):
    serializer = OnboardSalesLeadSerializer(data=data)
    print(data)
    serializer.is_valid(raise_exception=True)

    # print(serializer.data)
    merchant = serializer.validated_data["company"]
    company_email = data.get("company_email", None)
    role = serializer.validated_data["role"]

    try:
        merchant = Company.objects.get(id=merchant)
    except Company.DoesNotExist:
        return {
            "success": False,
            "message": "Company does not exist",
            "status": status.HTTP_404_NOT_FOUND,
        }
    
    try:
        SalesLead.objects.get(user=user, merchant=merchant)
        return {
            "success": False,
            "message": "Sales lead already onboarded",
            "status": status.HTTP_404_NOT_FOUND,
        }
    except SalesLead.DoesNotExist:
        pass

    sales_lead_instance = SalesLead.objects.create(
        user=user,
        merchant=merchant,
        role=role,
    )

    if sales_lead_instance and sales_lead_instance.verified == True:
        sales_lead_instance.save()

    user.save()


def onboard_sales_officer(data, user):
    serializer = OnboardSalesOfficerSerializer(data=data)
    print(data)
    serializer.is_valid(raise_exception=True)

    # print(serializer.data)
    merchant = serializer.validated_data["company"]
    company_email = data.get("company_email", None)
    role = serializer.validated_data["role"]

    try:
        merchant = Company.objects.get(id=merchant)
    except Company.DoesNotExist:
        return {
            "success": False,
            "message": "Company does not exist",
            "status": status.HTTP_404_NOT_FOUND,
        }
    
    try:
        SalesOfficer.objects.get(user=user, merchant=merchant)
        return {
            "success": False,
            "message": "Sales officer already onboarded",
            "status": status.HTTP_404_NOT_FOUND,
        }
    except SalesOfficer.DoesNotExist:
        pass

    sales_officer_instance = SalesOfficer.objects.create(
        user=user,
        merchant=merchant,
        role=role,
    )

    if sales_officer_instance and sales_officer_instance.verified == True:
        sales_officer_instance.save()

    user.save()


# def onboard_team_member(user, sales_officer_instance):
#     merchant = sales_officer_instance.company

#     if not TeamMember.objects.filter(merchant=merchant).exists():
#         role_name = "ADMIN"
#     else:
#         role_name = "MEMBER"

#     TeamMember.create_record(
#         member=sales_officer_instance,
#         role=TeamMemberRole.objects.get_or_create(name="ADMIN")[0],
#         merchant=merchant,
#     )

#     return {
#         "success": True
#     }
