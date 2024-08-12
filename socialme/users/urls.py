# from django.urls import path, re_path
# from users.views import (
#     CustomProviderAuthView, CustomTokenObtainPairView, CustomTokenRefreshView,
#     CustomTokenVerifyView, LogoutView, ActivateUserView, ResendOTPView,

#     # LoginWithOTP, ValidateOTP,
# )

# from users.views import (
#     MerchantView, 
#     CreateDeleteTeam, EditTeam, SuperAdminView, HeadOfSalesView, 
#     SalesLeadView, SalesOfficerView
#     # CreateCompanyView, 
# )

# urlpatterns = [
#     re_path(
#         r'^o/(?P<provider>\S+)/$',
#         CustomProviderAuthView.as_view(),
#         name='provider-auth'
#     ),
#     path('jwt/create/', CustomTokenObtainPairView.as_view()),
#     path('jwt/refresh/', CustomTokenRefreshView.as_view()),
#     path('jwt/verify/', CustomTokenVerifyView.as_view()),
#     path('logout/', LogoutView.as_view()),
#     path('activate/', ActivateUserView.as_view(), name='activate'),
#     path('resend-otp/', ResendOTPView.as_view(), name='send-otp'),
#     # path('login-with-otp', LoginWithOTP.as_view(), name='login-with-otp'),
#     # path('validate-otp/', ValidateOTP.as_view(), name='validate-otp')
#     # Pipeline URLs
#     path("create-merchant/", MerchantView.as_view(), name="create_merchant"),
#     path('create-team/', CreateDeleteTeam.as_view(), name='create-team'),
#     path('delete-team/<int:team_id>/', EditTeam.as_view(), name='delete-team'),
#     path('create-super-admin/', SuperAdminView.as_view()),
#     path('delete-super-admin/<str:super_admin_id>/', SuperAdminView.as_view()),
#     path('get-super-admin/<str:super_admin_id>/', SuperAdminView.as_view()),
#     path('create-head-of-sales/', HeadOfSalesView.as_view()),
#     path('delete-head-of-sales/<str:head_of_sales_id>/', HeadOfSalesView.as_view()),
#     path('get-head-of-sales/<str:head_of_sales_id>/', HeadOfSalesView.as_view()),
#     path('create-sales-lead/', SalesLeadView.as_view()),
#     path('delete-sales-lead/<str:sales_lead_id>/', SalesLeadView.as_view()),
#     path('get-sales-lead/<str:sales_lead_id>/', SalesLeadView.as_view()),
#     path('create-sales-officer/', SalesOfficerView.as_view()), 
#     path('delete-sales-officer/<str:sales_officer_id>/', SalesOfficerView.as_view()), 
#     path('get-sales-officer/<str:sales_officer_id>/', SalesOfficerView.as_view()), 
#     # path("create-company/", CreateCompanyView.as_view(), name="create_company"),
# ]
