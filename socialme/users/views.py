# from django.conf import settings
# from django.shortcuts import get_object_or_404
# from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, generics
# from rest_framework.permissions import AllowAny, IsAuthenticated 
# # from .utils import send_code_to_user, generate_otp, send_otp_email
# from django.core.mail import EmailMultiAlternatives
# from django.contrib.sites.shortcuts import get_current_site
# from .models import UserAccount
# from djoser.social.views import ProviderAuthView
# from drf_spectacular.utils import extend_schema, OpenApiParameter
# from drf_spectacular.types import OpenApiTypes
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# ) 
# from users.models import Company, Team, TeamMember, SuperAdmin, HeadOfSales, SalesLead, SalesOfficer, TeamMemberInvite
# from users.serializers import UserCreateSerializer, UserAccountSerializer, CreateUpdateTeamSerializer, SuperAdminSerializer, HeadOfSalesSerializer, SalesLeadSerializer, SalesOfficerSerializer, UserOTPSerializer
# from users.serializers import SalesLeadSerializer, SalesOfficerSerializer,  CreateCompanySerializer # CompanySerializer 
# import random
# from users.authentication import CustomJWTAuthentication
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from crmpipeline.reusables import CustomPagination


# class CustomProviderAuthView(ProviderAuthView):
#     @extend_schema(
#         operation_id='Google Authentication',
#         description='This endpoint is used to Login with Google',
#         summary='This endpoint is used to Login with Google',
#         request= OpenApiTypes.OBJECT,
#         responses={200: UserCreateSerializer},
#     )
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)

#         if response.status_code == 201:
#             access_token = response.data.get('access')
#             refresh_token = response.data.get('refresh')

#             response.set_cookie(
#                 'access',
#                 access_token,
#                 max_age=settings.AUTH_COOKIE_MAX_AGE,
#                 path=settings.AUTH_COOKIE_PATH,
#                 secure=settings.AUTH_COOKIE_SECURE,
#                 httponly=settings.AUTH_COOKIE_HTTP_ONLY,
#                 samesite=settings.AUTH_COOKIE_SAMESITE
#             )
#             response.set_cookie(
#                 'refresh',
#                 refresh_token,
#                 max_age=settings.AUTH_COOKIE_MAX_AGE,
#                 path=settings.AUTH_COOKIE_PATH,
#                 secure=settings.AUTH_COOKIE_SECURE,
#                 httponly=settings.AUTH_COOKIE_HTTP_ONLY,
#                 samesite=settings.AUTH_COOKIE_SAMESITE
#             )

#         return response


# class CustomTokenObtainPairView(TokenObtainPairView):
#     @extend_schema(
#         operation_id='Login with JWT Token',
#         description='This endpoint is used to Login with with JWT Token',
#         summary='This endpoint is used to Login with JWT Token. The Token is stored using http cookies automatically',
#         request= OpenApiTypes.OBJECT,
#         responses={200: UserCreateSerializer},
#     )
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)

#         if response.status_code == 200:
#             access_token = response.data.get('access')
#             refresh_token = response.data.get('refresh')

#             response.set_cookie(
#                 'access',
#                 access_token,
#                 max_age=settings.AUTH_COOKIE_MAX_AGE,
#                 path=settings.AUTH_COOKIE_PATH,
#                 secure=settings.AUTH_COOKIE_SECURE,
#                 httponly=settings.AUTH_COOKIE_HTTP_ONLY,
#                 samesite=settings.AUTH_COOKIE_SAMESITE
#             )
#             response.set_cookie(
#                 'refresh',
#                 refresh_token,
#                 max_age=settings.AUTH_COOKIE_MAX_AGE,
#                 path=settings.AUTH_COOKIE_PATH,
#                 secure=settings.AUTH_COOKIE_SECURE,
#                 httponly=settings.AUTH_COOKIE_HTTP_ONLY,
#                 samesite=settings.AUTH_COOKIE_SAMESITE
#             )

#         return response


# class CustomTokenRefreshView(TokenRefreshView):
#     @extend_schema(
#         operation_id='Refresh JWT Token',
#         description='This endpoint refreshes the JWT Token',
#         summary='This endpoint is used to refresh the JWT Token. The Token is then stored using http cookies automatically',
#         request= OpenApiTypes.OBJECT,
#         responses={200: UserCreateSerializer},
#     )
#     def post(self, request, *args, **kwargs):
#         refresh_token = request.COOKIES.get('refresh')

#         if refresh_token:
#             request.data['refresh'] = refresh_token

#         response = super().post(request, *args, **kwargs)

#         if response.status_code == 200:
#             access_token = response.data.get('access')

#             response.set_cookie(
#                 'access',
#                 access_token,
#                 max_age=settings.AUTH_COOKIE_MAX_AGE,
#                 path=settings.AUTH_COOKIE_PATH,
#                 secure=settings.AUTH_COOKIE_SECURE,
#                 httponly=settings.AUTH_COOKIE_HTTP_ONLY,
#                 samesite=settings.AUTH_COOKIE_SAMESITE
#             )

#         return response


# class CustomTokenVerifyView(TokenVerifyView):
#     @extend_schema(
#         operation_id='Verify JWT Token',
#         description='This endpoint verifies the JWT Token',
#         summary='This endpoint is used to verify the JWT Token. The Token is then stored using http cookies automatically',
#         request= OpenApiTypes.OBJECT,
#         responses={200: UserCreateSerializer},
#     )
#     def post(self, request, *args, **kwargs):
#         access_token = request.COOKIES.get('access')

#         if access_token:
#             request.data['token'] = access_token

#         return super().post(request, *args, **kwargs)


# class LogoutView(APIView):
#     @extend_schema(
#         operation_id='Logout Endpoint',
#         description='This endpoint logs out the user by deleting the cookie from the browser.',
#         summary='This endpoint logs out the user by deleting the cookie from the browser.',
#         request= OpenApiTypes.OBJECT,
#         responses={200: UserCreateSerializer},
#     )
#     def post(self, request, *args, **kwargs):
#         response = Response(status=status.HTTP_204_NO_CONTENT)
#         response.delete_cookie('access')
#         response.delete_cookie('refresh')

#         return response
    

# class CreateUserView(generics.CreateAPIView):
#     queryset = UserAccount.objects.all()
#     serializer_class = UserAccountSerializer
#     permission_classes = [AllowAny]

#     @extend_schema(
#         operation_id='Create a user using a One-Time Password',
#         description='This endpoint creates a user using OTP',
#         summary='This endpoint is used to create a user using OTP',
#         request= OpenApiTypes.OBJECT,
#         responses={200: UserAccountSerializer},
#         )
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         # def generate_otp():
#         #     return str(random.randint(100000, 999999))
#         if serializer.is_valid():
#             user = serializer.save(is_active=False)
#             otp = random.randint(100000, 999999)
#             user.otp = otp
#             user.save()

#             email = user.email
#             current_site = get_current_site(request)
#             subject = 'Kindly activate your account'
#             from_email = settings.DEFAULT_FROM_EMAIL
#             to_email = user.email
#             email.send()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class ActivateUserView(APIView):
#     permission_classes = [AllowAny]
#     @extend_schema(
#         operation_id='Activate a user using a One-Time Password',
#         description='This endpoint activates a user using OTP',
#         summary='This endpoint is used to activate a user using OTP',
#         request= OpenApiTypes.OBJECT,
#         responses={200: UserAccountSerializer},
#         )
    
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         otp = request.data.get('otp')

#         if not email or not otp:
#             return Response({'error': ('Email and OTP are required.')}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             user = UserAccount.objects.get(email=email)
#         except UserAccount.DoesNotExist:
#             return Response({'error': ('User does not exist.')}, status=status.HTTP_400_BAD_REQUEST)
        

#         if user.otp == otp:
#             user.is_active = True
#             user.otp = None # Clear OTP after successful activation
#             user.save()

#             email = user.email
#             current_site = get_current_site(self.request)
#             subject = 'Your account has been activated successfully'
#             protocol = 'https' if self.request.is_secure() else 'http'
#             from_email = settings.DEFAULT_FROM_EMAIL
#             to_email = user.email

#             email = EmailMultiAlternatives(subject, from_email, [to_email])
#             email.send()

#             return Response({'message': ('Your account has been activated successfully')}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': ('Invalid OTP.')}, status=status.HTTP_400_BAD_REQUEST)


# class ResendOTPView(APIView):
#     permission_classes = [AllowAny]
#     @extend_schema(
#         operation_id='Resend OTP to user',
#         description='This endpoint resends OTP to user',
#         summary='This endpoint is used to resend OTP to user provided they have their email address.',
#         request= OpenApiTypes.OBJECT,
#         responses={200: UserAccountSerializer},
#         )

#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')

#         if not email:
#             return Response({'error': ('Email is required.')}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = UserAccount.objects.get(email=email)
#         except UserAccount.DoesNotExist:
#             return Response({'error': ('User does not exist.')}, status=status.HTTP_400_BAD_REQUEST)

#         otp = random.randint(100000, 999999)
#         user.otp = otp  # Save the OTP to the user model 
#         user.save()
#         email = user.email
#         current_site = get_current_site(self.request)
#         subject = 'Your new OTP'
        
#         from_email = settings.DEFAULT_FROM_EMAIL
#         to_email = user.email
#         email = EmailMultiAlternatives(subject, from_email, [to_email])
#         email.send()

#         return Response({'message': ('OTP resent successfully.')}, status=status.HTTP_200_OK)




# class MerchantView(APIView):
#     """
#     API endpoint for handling merchant-related operations.

#     Requires JWT authentication.
#     """

#     authentication_classes = [JWTAuthentication]
#     # permission_classes = [IsAuthenticated]
#     permission_classes = [AllowAny]

#     serializer_class = CreateCompanySerializer

#     pagination_class = CustomPagination

#     def post(self, request):
#         """
#         Create a new merchant.

#         Required Parameters:
#         - company_name: Name of the company.
#         - id: ID of the company.

#         Returns:
#             - 201 Created: Company created successfully.
#             - 400 Bad Request: If any required parameter is missing or invalid.
#         """

#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         company_name = request.data.get("company_name",)
#         # company_name = serializer.validated_data.get["company_name"]
#         # id = serializer.validated_data.get["id"]
#         id = serializer.validated_data.get("id",)
#         user = serializer.validated_data.get("user")

#         # check if merchant exists
#         existing_merchant = Company.objects.filter(company_name=company_name, id=id)
#         if existing_merchant.exists():
#             return Response(
#                 {"message": "Merchant already exists"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
        
#         # create merchant
#         merchant = get_object_or_404(Company, id=id)
#         # merchant = Company.objects.create(
#         #     company_name=company_name,
#         #     user=UserAccount.default_company,
#         # )

#         serializer = CreateCompanySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # merchant_serialized_data = CompanySerializer(merchant).data

#         return Response(
#             {
#                 "message": "Merchant created successfully",
#                 # "company": merchant_serialized_data,
#                 "company": serializer,
#             },
#             status=status.HTTP_201_CREATED,
#         )

#     def get(self, request):
#         """
#         Retrieve a list of all merchants.

#         Returns:
#         - Paginated list of merchant details.

#         Note:
#         - Requires JWT authentication.
#         """

#         merchants = Company.objects.all()
#         paginator = CustomPagination()
#         result_page = paginator.paginate_queryset(merchants, request)
#         serializer = CreateCompanySerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)


# class CreateDeleteTeam(APIView):
#     # permission_classes = [IsAuthenticated]
#     permission_classes = [AllowAny]
#     # authentication_classes = [CustomUserAuthentication]

#     def post(self, request):
#         serializer = CreateUpdateTeamSerializer(
#             data=request.data, context={
#                 "user": request.user, "request": request, "create_team": True}
#         )
#         serializer.is_valid(raise_exception=True)
#         data = serializer.validated_data

#         create_team_result = Team.create_team(
#             user=request.user, **data
#         )
#         # handle response data
#         if create_team_result.get("status") == False:
#             response_data = {
#                 "status": "Failed",
#                 "message": create_team_result.get("message")
#             }
#             return Response(
#                 response_data, status=status.HTTP_400_BAD_REQUEST
#             )
#         data["team_id"] = create_team_result.get("team").id
#         response_data = {
#             "status": "Success",
#             "data": data
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

#     def delete(self, request):
#         pk = request.query_params.get("team_id")
#         try:
#             team = Team.objects.get(user=request.user, pk=pk)
#         except Team.DoesNotExist:
#             return Response({"status": "Error", 'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

#         team.soft_delete()
#         return Response({"status": "Success", "message": "Team deleted successfully"}, status=status.HTTP_200_OK)


# class EditTeam(APIView):
#     permission_classes = [IsAuthenticated, ]
#     # authentication_classes = [CustomUserAuthentication]
#     authentication_classes = [CustomJWTAuthentication]

#     def post(self, request):

#         serializer = CreateUpdateTeamSerializer(
#             data=request.data,
#             context={
#                 "user": request.user, 
#                 "request": request,
#                 "create_team": False
#             }
#         )
#         serializer.is_valid(raise_exception=True)
#         Team.update_team(validated_data=serializer.validated_data)
#         response_data = {
#             "status": "success",
#             "data": serializer.data
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

#     def delete(self, request):
#         params = request.query_params
#         team_id = params.get("team_id")
#         member_id = params.get("member_id")

#         try:
#             team = Team.objects.get(pk=team_id)
#         except Team.DoesNotExist:
#             return Response({"status": "Error", "message": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

#         try:
#             member = TeamMember.objects.get(
#                 team_lead=request.user, pk=member_id, team_id=team_id)
#         except TeamMember.DoesNotExist:
#             return Response({"status": "Error", "message": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

#         if member in team.members.all():
#             team.members.remove(member)
#             member.is_deleted = True
#             member.save()
#             return Response(
#                 {
#                     "status": "Success", 
#                     "message": "Team member removed successfully"
#                 },
#                 status=status.HTTP_200_OK)
#         else:
#             return Response(
#                 {
#                     "status": "Error", 
#                     "message": "Member not found on team"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST)


# class SuperAdminView(APIView):
#     permission_classes = [AllowAny]
#     # permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         serializer = SuperAdminSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         super_admin, created = SuperAdmin.objects.get_or_create(
#             user=user,
#             # super_admin=super_admin,
#             defaults={
#                 'name': user.name,
#                 'email': user.email,
#             }
#         )

#         if not created:
#             return Response({"detail": "Super Admin already exists."}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     def get(self, request):
#         """
#         Retrieve details of the authenticated super admin instance.

#         Args:
#         - request: HTTP request object.

#         Returns:
#         - Response: Details of the authenticated super admin instance.
#         """

#         id = request.user.id
#         if id is None:
#             return Response(
#                 {"message": "id is required"}, status=status.HTTP_400_BAD_REQUEST
#             )
        
#         try:
#             super_admin = SuperAdmin.objects.get(user__id=id)
#         except SuperAdmin.DoesNotExist:
#             return Response(
#                 {"message": f"The requested {super_admin} does not exist"}, status=status.HTTP_404_NOT_FOUND
#             )
    
#     def delete(self, request):
#         params = request.query_params
#         email = params.get("email")
#         super_admin_id = params.get("super_admin_id")

#         try:
#             super_admin = SuperAdmin.objects.get(pk=super_admin_id, email=email)
#         except SuperAdmin.DoesNotExist:
#             return Response(
#                 {
#                     "status": "Error",
#                     "message": "Super Admin not found",
#                 }, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         if super_admin in super_admin.objects:
#             super_admin.delete(super_admin)
#             super_admin.save()
#             return Response(
#                 {
#                     "status": "Success",
#                     "message": "Super Admin deleted successfully"
#                 },
#                 status=status.HTTP_200_OK
#             )


# class HeadOfSalesView(APIView):
#     permission_classes = [AllowAny]
#     # permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         super_admin_id = request.data.get('super_admin_id')
#         super_admin = get_object_or_404(SuperAdmin, id=super_admin_id)

#         serializer = HeadOfSalesSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         head_of_sales, created = HeadOfSales.objects.get_or_create(
#             user=user,
#             head_of_sales=head_of_sales,
#             defaults={
#                 'name': user.name,
#                 'email': user.email,
#             }
#         )

#         if not created:
#             return Response({"detail": "Head of Sales already exists."}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     def get(self, request):
#         """
#         Retrieve details of the authenticated head of sales.

#         Args:
#         - request: HTTP request object.

#         Returns:
#         - Response: Details of the authenticated head of sales.
#         """

#         id = request.user.id
#         if id is None:
#             return Response(
#                 {"message": "id is required"}, status=status.HTTP_400_BAD_REQUEST
#             )
        
#         try:
#             head_of_sales = HeadOfSales.objects.get(user__id=id)
#         except HeadOfSales.DoesNotExist:
#             return Response(
#                 {"message": f"The requested {head_of_sales} does not exist"}, status=status.HTTP_404_NOT_FOUND
#             )
    
#     def delete(self, request):
#         params = request.query_params
#         email = params.get("email")
#         head_of_sales_id = params.get("head_of_sales_id")

#         try:
#             head_of_sales = HeadOfSales.objects.get(pk=head_of_sales_id, email=email)
#         except HeadOfSales.DoesNotExist:
#             return Response(
#                 {
#                     "status": "Error",
#                     "message": "Head of Sales not found",
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         if head_of_sales in head_of_sales.objects:
#             head_of_sales.delete(head_of_sales)
#             head_of_sales.save()
#             return Response(
#                 {
#                     "status": "Success",
#                     "message": "Head of Sales deleted successfully"
#                 }, 
#                 status=status.HTTP_200_OK
#             )

    
# class SalesLeadView(APIView):
#     permission_classes = [AllowAny]
#     # permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         head_of_sales_id = request.data.get('head_of_sales_id')
#         head_of_sales = get_object_or_404(HeadOfSales, id=head_of_sales_id)

#         serializer = SalesLeadSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         sales_lead, created = SalesLead.objects.get_or_create(
#             user=user,
#             sales_lead=sales_lead,
#             defaults={
#                 'name': user.name,
#                 'email': user.email,
#             }
#         )

#         if not created:
#             return Response({"detail": "Sales lead already exists."}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     def get(self, request):
#         """
#         Retrieve details of the authenticated sales lead.

#         Args:
#         - request: HTTP request object.

#         Returns:
#         - Response: Details of the authenticated sales lead.
#         """

#         id = request.user.id
#         if id is None:
#             return Response(
#                 {"message": "id is required"}, status=status.HTTP_400_BAD_REQUEST
#             )
        
#         try:
#             sales_lead = SalesLead.objects.get(user__id=id)
#         except SalesLead.DoesNotExist:
#             return Response(
#                 {"message": f"The requested {sales_lead} does not exist"}, status=status.HTTP_404_NOT_FOUND
#             )
    
#     def delete(self, request):
#         params = request.query_params
#         email = params.get("email")
#         sales_lead_id = params.get("sales_lead_id")
    
#         try:
#             sales_lead = SalesLead.objects.get(pk=sales_lead_id, email=email)
#         except SalesLead.DoesNotExist:
#             return Response(
#                 {
#                     "status": "Error",
#                     "message": "Sales Lead not found"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         if sales_lead in sales_lead.objects:
#             sales_lead.delete(sales_lead)
#             sales_lead.save()
#             return Response(
#                 {
#                     "status": "Success",
#                     "message": "Sales Lead deleted successfully"
#                 },
#                 status=status.HTTP_200_OK
#             )

# class SalesOfficerView(APIView):
#     permission_classes = [AllowAny]
#     # permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         sales_lead_id = request.data.get('sales_lead_id')
#         sales_lead = get_object_or_404(SalesLead, id=sales_lead_id)

#         # referral_code = generate_random_referral_code(6)
#         # product_vertical = sales_lead.product_verticals

#         serializer = SalesOfficerSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         sales_officer, created = SalesOfficer.objects.get_or_create(
#             user=user,
#             sales_officer=sales_officer,
#             defaults={
#                 'name': user.name,
#                 'email': user.email,
#                 # 'product_vertical': product_vertical,
#                 # 'referral_code': referral_code,
#             }
#         )

#         if not created:
#             return Response({"detail": "Sales officer already exists."}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     def get(self, request):
#         params = request.query_params
#         sales_officer_id = params.get("sales_officer_id")

#         if sales_officer_id is None:
#             return Response(
#                 {
#                     "message": "sales_officer_id",
#                 }, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         try:
#             sales_officer = SalesOfficer.objects.get(id=sales_officer_id)
#         except SalesOfficer.DoesNotExist:
#             return Response(
#                 {
#                     "message": f"The Sales Officer does not exist"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#     def delete(self, request):
#         params = request.query_params
#         email = params.get("email")
#         sales_officer_id = params.get("sales_officer_id")

#         try:
#             sales_officer = SalesOfficer.objects.get(pk=sales_officer_id, email=email)
#         except SalesOfficer.DoesNotExist:
#             return Response(
#                 {
#                     "status": "Error",
#                     "message": "Sales Officer not found"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         if sales_officer in sales_officer.objects:
#             sales_officer.delete(sales_officer)
#             sales_officer.save()
#             return Response(
#                 {
#                     "status": "Success",
#                     "message": "Sales Officer deleted successfully"
#                 },
#                 status=status.HTTP_200_OK
#             )


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


# class LoginWithOTP(APIView):
#     @extend_schema(
#         operation_id='Login With OTP',
#         description='This endpoint is used to Login with a One Time Password',
#         summary='This endpoint is used to Login with an OTP',
#         request= OpenApiTypes.OBJECT,
#         responses={200: UserOTPSerializer},
#     )
#     def post(self, request):
#         email = request.data.get('email', '')
#         try:
#             user = UserAccount.objects.get(email=email)
#         except UserAccount.DoesNotExist:
#             return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
#         otp = generate_otp()
#         user.otp = otp
#         user.save()

#         send_otp_email(email, otp)

#         return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)
    

# class ValidateOTP(APIView):
#     @extend_schema(
#         operation_id='Validate OTP',
#         description='This endpoint is used to validate a One Time Password',
#         summary='This endpoint is used to validate OTP',
#         request= OpenApiTypes.OBJECT,
#         responses={200: UserOTPSerializer},
#     )
#     def post(self, request):
#         email = request.data.get('email', '')
#         otp = request.data.get('otp', '')

#         try:
#             user = UserAccount.objects.get(email=email)
#         except UserAccount.DoesNotExist:
#             return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
#         if user.otp == otp:
#             user.otp = None # Resetting the OTP field after successful validation
#             user.save()

#             # Authenticate the user and create or get an authentication token
#             token, _ = Token.objects.get_or_create(user=user)

#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)