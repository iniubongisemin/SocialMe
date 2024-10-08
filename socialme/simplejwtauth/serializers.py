from django.contrib.auth.models import User
from simplejwtauth.models import Company, SuperAdmin, HeadOfSales, SalesLead, SalesOfficer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email",)
        extra_kwargs = {"password": {"write_only": True}}

        def create(self, validated_data):
            password = validated_data.pop("password")
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return {
                "username": user.username,
                "email": user.email
            }
        

class CreateCompanySerializer(serializers.Serializer):
    user = serializers.CharField(max_length=255)
    company_name = serializers.CharField(allow_blank=True, allow_null=True)
    industry = serializers.CharField(allow_blank=True, allow_null=True)
    # user = serializers.IntegerField()
    # id = serializers.CharField(allow_blank=True, allow_null=True)
    # teams = serializers.CharField(allow_blank=True, allow_null=True)
    
    # def validate(self, company_name, industry):
    def validate(self, data):
        # user = user
        company_name = data.get("company_name")
        id = data.get("id")
        # industry = industry
        
        try:
            # company = Company.objects.filter(company_name=company_name)
            # industry = Company.objects.filter(company_name=company_name)
            company = Company.objects.get(company_name=company_name)
            raise serializers.ValidationError({"message": f"{company_name} already exists"})
        except Company.DoesNotExist:
            pass 
        return data

        # except Company.DoesNotExist:
        #     raise serializers.ValidationError(
        #         {"message": f"{company} name already exists"}
        #     )

        # return Company


    class Meta:
        model = Company
        fields = [
            "user",
            "company_name",
            "industry"
        ]
        # exclude = ['user']

    # def validate(self, attrs):
        # context = self.context
        # request = context.get("request")
        # user = request.user
        # # user_id = request.user.id
        # company_name = attrs.get("company_name").title()
        


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "company_name")

# class CreateMerchantSerializer(serializers.ModelSerializer):
#     name = serializers.CharField()
#     merchant = CreateCompanySerializer()

#     class Meta:
#         model = Company
#         fields = ('id', 'name')
        

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['email', 'first_name', 'last_name',]


class HeadOfSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadOfSales
        fields = ['email', 'first_name', 'last_name',]
        # fields = ['name', 'email', 'super_admin']


class SalesLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesLead
        fields = ['email', 'first_name', 'last_name',]
        # fields = ['name', 'email', 'head_of_sales']


class SalesOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOfficer
        fields = ['email', 'first_name', 'last_name',]
        # fields = ['name', 'email', 'sales_lead']


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