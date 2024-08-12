from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status, generics
from simplejwtauth.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated 
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from simplejwtauth.models import Company, SuperAdmin, HeadOfSales, SalesLead, SalesOfficer #, Team, TeamMember, TeamMemberInvite
from simplejwtauth.serializers import SuperAdminSerializer, HeadOfSalesSerializer, SalesLeadSerializer, SalesOfficerSerializer #, CreateUpdateTeamSerializer,
from simplejwtauth.serializers import SalesLeadSerializer, SalesOfficerSerializer,  CreateCompanySerializer # CompanySerializer 
from rest_framework_simplejwt.authentication import JWTAuthentication
from crmpipeline.reusables import CustomPagination
# from django.core.mail import EmailMultiAlternatives
# from .utils import send_code_to_user, generate_otp, send_otp_email


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class MerchantView(APIView):
    """
    API endpoint for handling merchant-related operations.

    Requires JWT authentication.
    """

    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    serializer_class = CreateCompanySerializer

    pagination_class = CustomPagination

    def post(self, request):
        """
        Create a new merchant.

        Required Parameters:
        - company_name: Name of the company.
        - id: ID of the company.

        Returns:
            - 201 Created: Company created successfully.
            - 400 Bad Request: If any required parameter is missing or invalid.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        print("Serializing Data Passed...\n\n\n")
        user_id = serializer.validated_data.get("user")
        company_name = serializer.validated_data.get("company_name")
        industry = serializer.validated_data.get("industry")

        # company_name = serializer.validated_data.get["company_name"]
        # id = serializer.validated_data.get["id"]

        # check if merchant exists
        existing_merchant = Company.objects.filter(company_name=company_name)
        if existing_merchant.exists():
            return Response(
                {"message": "Merchant already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            ) 
        
        existing_user = User.objects.filter(user_id) 
        if not existing_user: 
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            ) 
        
        # create merchant
        # merchant = get_object_or_404(Company, id=id)
        print("Creating Created...\n\n\n")
        merchant = Company.create_company(
            user=user_id,
            company_name=company_name,
            industry=industry
        )
        print("Company Created")
        # serializer = CreateCompanySerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        # merchant_serialized_data = CompanySerializer(merchant).data

        return Response(
            {
                "message": "Merchant created successfully",
                "company": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        """
        Retrieve a list of all merchants.

        Returns:
        - Paginated list of merchant details.

        Note:
        - Requires JWT authentication.
        """

        merchants = Company.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(merchants, request)
        serializer = CreateCompanySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class SuperAdminView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = SuperAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        super_admin, created = SuperAdmin.objects.get_or_create(
            user=user,
            # super_admin=super_admin,
            defaults={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        )

        if not created:
            return Response({"detail": "Super Admin already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        """
        Retrieve details of the authenticated super admin instance.

        Args:
        - request: HTTP request object.

        Returns:
        - Response: Details of the authenticated super admin instance.
        """

        id = request.user.id
        if id is None:
            return Response(
                {"message": "id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            super_admin = SuperAdmin.objects.get(user__id=id)
        except SuperAdmin.DoesNotExist:
            return Response(
                {"message": f"The requested {super_admin} does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request):
        params = request.query_params
        email = params.get("email")
        super_admin_id = params.get("super_admin_id")

        try:
            super_admin = SuperAdmin.objects.get(pk=super_admin_id, email=email)
        except SuperAdmin.DoesNotExist:
            return Response(
                {
                    "status": "Error",
                    "message": "Super Admin not found",
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if super_admin in super_admin.objects:
            super_admin.delete(super_admin)
            super_admin.save()
            return Response(
                {
                    "status": "Success",
                    "message": "Super Admin deleted successfully"
                },
                status=status.HTTP_200_OK
            )


class HeadOfSalesView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        super_admin_id = request.data.get('super_admin_id')
        super_admin = get_object_or_404(SuperAdmin, id=super_admin_id)

        serializer = HeadOfSalesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        head_of_sales, created = HeadOfSales.objects.get_or_create(
            user=user,
            head_of_sales=head_of_sales,
            defaults={
                'name': user.name,
                'email': user.email,
            }
        )

        if not created:
            return Response({"detail": "Head of Sales already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        """
        Retrieve details of the authenticated head of sales.

        Args:
        - request: HTTP request object.

        Returns:
        - Response: Details of the authenticated head of sales.
        """

        id = request.user.id
        if id is None:
            return Response(
                {"message": "id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            head_of_sales = HeadOfSales.objects.get(user__id=id)
        except HeadOfSales.DoesNotExist:
            return Response(
                {"message": f"The requested {head_of_sales} does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request):
        params = request.query_params
        email = params.get("email")
        head_of_sales_id = params.get("head_of_sales_id")

        try:
            head_of_sales = HeadOfSales.objects.get(pk=head_of_sales_id, email=email)
        except HeadOfSales.DoesNotExist:
            return Response(
                {
                    "status": "Error",
                    "message": "Head of Sales not found",
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if head_of_sales in head_of_sales.objects:
            head_of_sales.delete(head_of_sales)
            head_of_sales.save()
            return Response(
                {
                    "status": "Success",
                    "message": "Head of Sales deleted successfully"
                }, 
                status=status.HTTP_200_OK
            )

    
class SalesLeadView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        head_of_sales_id = request.data.get('head_of_sales_id')
        head_of_sales = get_object_or_404(HeadOfSales, id=head_of_sales_id)

        serializer = SalesLeadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sales_lead, created = SalesLead.objects.get_or_create(
            user=user,
            sales_lead=sales_lead,
            defaults={
                'name': user.name,
                'email': user.email,
            }
        )

        if not created:
            return Response({"detail": "Sales lead already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        """
        Retrieve details of the authenticated sales lead.

        Args:
        - request: HTTP request object.

        Returns:
        - Response: Details of the authenticated sales lead.
        """

        id = request.user.id
        if id is None:
            return Response(
                {"message": "id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            sales_lead = SalesLead.objects.get(user__id=id)
        except SalesLead.DoesNotExist:
            return Response(
                {"message": f"The requested {sales_lead} does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request):
        params = request.query_params
        email = params.get("email")
        sales_lead_id = params.get("sales_lead_id")
    
        try:
            sales_lead = SalesLead.objects.get(pk=sales_lead_id, email=email)
        except SalesLead.DoesNotExist:
            return Response(
                {
                    "status": "Error",
                    "message": "Sales Lead not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if sales_lead in sales_lead.objects:
            sales_lead.delete(sales_lead)
            sales_lead.save()
            return Response(
                {
                    "status": "Success",
                    "message": "Sales Lead deleted successfully"
                },
                status=status.HTTP_200_OK
            )


class SalesOfficerView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        sales_lead_id = request.data.get('sales_lead_id')
        sales_lead = get_object_or_404(SalesLead, id=sales_lead_id)

        # referral_code = generate_random_referral_code(6)
        # product_vertical = sales_lead.product_verticals

        serializer = SalesOfficerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sales_officer, created = SalesOfficer.objects.get_or_create(
            user=user,
            sales_officer=sales_officer,
            defaults={
                'name': user.name,
                'email': user.email,
                # 'product_vertical': product_vertical,
                # 'referral_code': referral_code,
            }
        )

        if not created:
            return Response({"detail": "Sales officer already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        params = request.query_params
        sales_officer_id = params.get("sales_officer_id")

        if sales_officer_id is None:
            return Response(
                {
                    "message": "sales_officer_id",
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            sales_officer = SalesOfficer.objects.get(id=sales_officer_id)
        except SalesOfficer.DoesNotExist:
            return Response(
                {
                    "message": f"The Sales Officer does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request):
        params = request.query_params
        email = params.get("email")
        sales_officer_id = params.get("sales_officer_id")

        try:
            sales_officer = SalesOfficer.objects.get(pk=sales_officer_id, email=email)
        except SalesOfficer.DoesNotExist:
            return Response(
                {
                    "status": "Error",
                    "message": "Sales Officer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if sales_officer in sales_officer.objects:
            sales_officer.delete(sales_officer)
            sales_officer.save()
            return Response(
                {
                    "status": "Success",
                    "message": "Sales Officer deleted successfully"
                },
                status=status.HTTP_200_OK
            )
        

# class CreateCompanyView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):  # create a new company
#             serializer = CreateCompanySerializer(data=request.data, context={"request": request})
#             serializer.is_valid(raise_exception=True)
#             validated_data = serializer.validated_data

#             company = Company.create_company(user=request.user, validated_data=validated_data)

#             res_data = {"status": "Success",
#                         "data": {
#                             "company_name": validated_data.get("company_name"),
#                             "user": validated_data.get("user"),
#                             # "id": company.id,
#                         },
#                     }

#             return Response(res_data, status=status.HTTP_200_OK)