from django.contrib import admin
from .models import * 

class CompanyAdmin(admin.ModelAdmin):
    list_display = list_display =  [field.name for field in Company._meta.fields]
    # list_display = ("id", "email", "phone_number", "created_at", "updated_at", "user", "first_name", "is_staff", "is_superuser")

class Super_Admin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in SuperAdmin._meta.fields]

class HeadOfSalesAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in HeadOfSales._meta.fields]

class SalesLeadAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in SalesLead._meta.fields]

class SalesOfficerAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in SalesOfficer._meta.fields]

# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(SuperAdmin, Super_Admin)
admin.site.register(HeadOfSales, HeadOfSalesAdmin)
admin.site.register(SalesLead, SalesLeadAdmin)
admin.site.register(SalesOfficer, SalesOfficerAdmin)
