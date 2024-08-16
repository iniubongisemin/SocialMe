from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from simplejwtauth.views import (
    MerchantView, SuperAdminView, HeadOfSalesView, 
    SalesLeadView, SalesOfficerView, CreateUser
    # CreateCompanyView, 
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-user/', CreateUser.as_view(), name='create-user'),
    # Pipeline URLs
    path("create-merchant/", MerchantView.as_view(), name="create_merchant"),
    path("get_merchant/<str:id>/", MerchantView.as_view(), name="get_merchant"),
    path('create-super-admin/', SuperAdminView.as_view()),
    path('delete-super-admin/<str:super_admin_id>/', SuperAdminView.as_view()),
    path('get-super-admin/<str:super_admin_id>/', SuperAdminView.as_view()),
    path('create-head-of-sales/', HeadOfSalesView.as_view()),
    path('delete-head-of-sales/<str:head_of_sales_id>/', HeadOfSalesView.as_view()),
    path('get-head-of-sales/<str:head_of_sales_id>/', HeadOfSalesView.as_view()),
    path('create-sales-lead/', SalesLeadView.as_view()),
    path('delete-sales-lead/<str:sales_lead_id>/', SalesLeadView.as_view()),
    path('get-sales-lead/<str:sales_lead_id>/', SalesLeadView.as_view()),
    path('create-sales-officer/', SalesOfficerView.as_view()), 
    path('delete-sales-officer/<str:sales_officer_id>/', SalesOfficerView.as_view()), 
    path('get-sales-officer/<str:sales_officer_id>/', SalesOfficerView.as_view()), 
    # path("create-company/", CreateCompanyView.as_view(), name="create_company"),
]
