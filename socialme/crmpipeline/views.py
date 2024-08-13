from datetime import datetime
from django.db.models import Q, F

from django.core.exceptions import ObjectDoesNotExist
import django_filters
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count, Max
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.core.validators import validate_email
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import Count
from django.core import signing
from decouple import config
from io import BytesIO
import pandas as pd
import zipfile
# import pdfplumber
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from crmpipeline.reusables import (
    CustomPageNumberPagination, CustomPagination, DealFilter, 
    onboard_super_admin, onboard_head_of_sales, onboard_sales_lead, onboard_sales_officer, onboard_team_member
)
from crmpipeline.utils import DataResponse, stage_notification

from simplejwtauth.models import Company, SuperAdmin, HeadOfSales, SalesLead, SalesOfficer  # TeamMember 
from django.contrib.auth.models import User
from simplejwtauth.serializers import HeadOfSalesSerializer, SalesLeadSerializer, SuperAdminSerializer, SalesOfficerSerializer 
from crmpipeline.models import (
    Stage, Deal, Pipeline, Activity, Task, Lead, TeamMemberRole, 
    # TeamMemberPermission, TeamMemberRolePermission, DealProgression, LeadsDataUpload, HeadOfSales, 
    # TaskNotification, DealsComment, TaskComment, MerchantDealPipeline, DealRequirement, EmaiLog, TaskSchedule, Report, DealPipeline, 
)

from crmpipeline.serializers import (
    PipelineSerializer, StageSerializer, DealSerializer, TaskSerializer, ActivitySerializer, LeadSerializer, 
    # TeamMemberRoleSerializer, TeamMemberPermissionSerializer, CreateDealSerializer, TeamMemberRolePermissionSerializer, 
    # TeamMemberSerializer, ChangeDealStageSerializer, NewTeamMemberSerializer, DealProgressionStageSerializer,
    # TaskNotificationSerializer, LeadsDataUploadSerializer, 
)

# from crmpipeline.permissions import (
#     CanManageDeal,
#     CanManageStage,
#     CanManagePipeline,
#     CanManageMerchantsProgress,
#     create_roles_and_permissions,
# )


class LeadView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        lead_id = request.data.get('id')
        lead = get_object_or_404(Lead, id=lead_id)

        serializer = LeadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lead, created = Lead.objects.get_or_create(
            user=user,
            defaults={
                'id': lead.id,
                'name': lead.name,
                'email': lead.email_address,
                'label': serializer.validated_data.get('label', 'COLD'), # Default set to cold
            }
        )

        if not created:
            return Response({"detail": "Lead already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Checking if the lead label is HOT and convert to Deal if True

        if lead.label == "HOT":
            with transaction.atomic():
                deal = lead.convert_lead_to_deal()
                if deal:
                    # Include the deal information in the response if created
                    return Response({
                        "lead": serializer.data,
                        "deal": {
                            "id": deal.unique_id,
                            "title": deal.deal_title,
                            "status": deal.deal_status,
                        }
                    }, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        task_id = request.data.get('task_id')
        task = get_object_or_404(Task, id=task_id)

        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task, created = Task.objects.get_or_create(
            user=user,
            defaults={
                'title': task.title,
                'status': task.status,
                'current_stage': task.current_stage,
            }
        )

        if not created:
            return Response({"detail": "Lead already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ActivityView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        id = request.data.get('activity_id')
        activity = get_object_or_404(Activity, id=id)

        serializer = ActivitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        activity, created = Activity.objects.get_or_create(
            user=user,
            defaults={
                'id': activity.id,
                'title': activity.title,
                'status': activity.status,
                'stage': activity.stage,
            }
        )

        if not created:
            return Response({"detail": "Activity already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TrackTaskView(APIView):
    def post(self, request):
        unique_id = request.data.get('unique_id')
        if unique_id is None:
            return Response({'message': 'unique_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(unique_id=unique_id)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        task.viewers_count += 1
        task.save()

        return Response({'message': 'Viewer count updated successfully'}, status=status.HTTP_200_OK)


class TrackActivityView(APIView):
    def post(self, request):
        unique_id = request.data.get('unique_id')
        if unique_id is None:
            return Response({'message': 'unique_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            activity = Activity.objects.get(unique_id=unique_id)
        except Activity.DoesNotExist:
            return Response({'message': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)

        activity.viewers_count += 1
        activity.save()

        return Response({'message': 'Viewer count updated successfully'}, status=status.HTTP_200_OK)
    
    
class TrackDealView(APIView):
    def post(self, request):
        unique_id = request.data.get('unique_id')
        if unique_id is None:
            return Response({'message': 'unique_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            deal = Deal.objects.get(unique_id=unique_id)
        except Deal.DoesNotExist:
            return Response({'message': 'Deal not found'}, status=status.HTTP_404_NOT_FOUND)

        deal.viewers_count += 1
        deal.save()

        return Response({'message': 'Viewer count updated successfully'}, status=status.HTTP_200_OK)


    
    
class DealView(APIView):
    """
    API endpoint for CRUD operations related to deals.

    Attributes:
    - authentication_classes: List of authentication classes required for access.
    - permission_classes: List of permission classes required for access.
    - create_deal_serializer_class: Serializer class for creating a deal.
    - filter_backends: List of filter backends for deal listing.
    - filterset_class: Filterset class for deal filtering.

    Methods:
    - post(request): Create a new deal.
    - get(request): Retrieve a deal by ID.
    - delete(request): Delete a deal by ID.
    - put(request): Update a deal by ID.
    - patch(request): Partially update a deal by ID.

    Returns:
    - Response: Result of the CRUD operations on deals.
    """

    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, CanManageDeal]
    permission_classes = [
        AllowAny, 
        # CanManageDeal
    ]

    # create_deal_serializer_class = CreateDealSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = DealFilter

    def post(self, request):
        """
        Create a new deal.

        Args:
        - request: HTTP request object.

        Returns:
        - Response: Result of the deal creation operation.
        """
        serializer = self.create_deal_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        print("serializer.validated_data---", serializer.validated_data)

        print("Nameeeee -----------", serializer.validated_data.get("name"))

        name = request.data.get("name", deal.deal_title)
        description = serializer.validated_data.get("description")
        deal_status = serializer.validated_data.get("deal_status", "DRAFT")
        team_members = serializer.validated_data.get("team_member")
        merchant_overview = serializer.validated_data.get("merchant_overview")
        industry = serializer.validated_data.get("industry")
        pipeline_type = serializer.validated_data.get("pipeline_type")
        deal_type = serializer.validate_data.get("deal_type")

        if pipeline_type == "DEFAULT":
            # Create a default pipeline with default stages
            try:
                with transaction.atomic():
                    sales_officer = SalesOfficer.objects.get(user=self.request.user)
                    merchant = sales_officer.merchant
                    default_stage_names = [
                        "Qualified",
                        "Demo scheduled",
                        "Proposal made",
                        "Invoice",
                    ]
                    pipeline = Pipeline.objects.create(
                        name = "Default Pipeline", sales_officer=sales_officer, merchant=merchant
                    )
                    default_stages = []
                    for index, name in enumerate(default_stage_names):
                        stage_kwargs = {"name": name, "order": index}
                        if name == "New deal":
                            stage_kwargs["is_new_deal"] = True
                        default_stages.append(Stage.objects.create(**stage_kwargs))

                    pipeline.stages.add(*default_stages)
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        
        else:
            pipeline = serializer.validated_data.get("pipeline")

        serializer.validated_data["pipeline"] = pipeline

        if deal_deadline != None:
            deal_deadline = deal_deadline.date()

        if deal_start_date != None:
            deal_start_date = deal_start_date.date()

         # check if the application start date is in the feature
        if deal_deadline != None and deal_start_date != None:
            if deal_start_date > deal_deadline:
                return Response(
                    {
                        "message": "Deal start date cannot be greater than deal deadline"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if deal_start_date != None:
            if deal_start_date > datetime.date(datetime.now()):
                deal_status = "QUEUED"

        # END check if the deal's start date is in present

        # list_of_team_members = []   
        # if (team_members != None) and (len(team_members) > 0):
        #     for _team_member in team_members:
        #         try:
        #             team_member = TeamMember.objects.get(
        #                 id=_team_member, merchant=request.user.sales_officer.merchant
        #             )
        #             list_of_team_members.append(team_member)
        #         except TeamMember.DoesNotExist:
        #             return Response(
        #                 {"message": "Team member does not exist"}, status=status.HTTP_404_NOT_FOUND,
        #             )
                
        #         print("NaMe----", name)

                # Create deal
                deal = Deal.objects.create(
                    deal_title=serializer.validated_data.get("name"),
                    description=description,
                    sales_officer=sales_officer,
                    deal_type=deal_type,
                    deal_status=deal_status, 
                    merchant_overview=merchant_overview,
                    industry=industry,
                    pipeline_type=pipeline_type,
                    pipeline=pipeline,
                )

                print("deal--", deal)

                deal.update_deal_status()

                # if len(list_of_team_members) > 0:
                #     deal.team_member.set(list_of_team_members)

    def get(self, request, unique_id):
        """
        Retrieve a deal by it's unique_id.

        Args:
        - request: HTTP request object.

        Returns:
        - Response: Result of retrieving the deal by it's unique_id.
        """
        try:
            deal = Deal.objects.get(unique_id=unique_id)
        except Deal.DoesNotExist:
            raise Http404("Deal does not exist")
        
        serializer = DealSerializer(deal)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        """
        Delete deal by ID.

        Args:
        - request: HTTP request object.

        Returns:
        - Response: Result of deleting the deal by it's ID.
        """

        id = request.GET.get("id", None)
        if id is None:
            return Response(
                {"message": "id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            deal = Deal.objects.get(id=id)
        except Deal.DoesNotExist:
            return Response(
                {"message": "Deal does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        deal.delete()

        return Response(
            data={"message": "Deal deleted successfully"}, status=status.HTTP_200_OK
        )
        
    def put(self, request):
        """
        Update a deal by ID.

        Args:
        - Response: Result of updating the job by ID.
        """

        id = request.GET.get("id", None)
        if id is None:
            return Response(
                {"message": "id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            deal = Deal.objects.get(id=id)
        except Deal.DoesNotExist:
            return Response(
                {"message": "Deal does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.create_deal_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = request.data.get("name", deal.deal_title)
        description = serializer.validated_data.get("description")
        deal_status = serializer.validated_data.get("deal_status", "DRAFT")
        team_members = serializer.validated_data.get("team_member")
        merchant_overview = serializer.validated_data.get("merchant_overview")
        industry = serializer.validated_data.get("industry")
        pipeline_type = serializer.validated_data.get("pipeline_type")
        # deal_type = serializer.validated_data.get("deal_type")

        # list_of_team_members = []
        # if (team_members != None) and (len(team_members) > 0):
        #     for _team_member in team_members:
        #         try:
        #             team_member = TeamMember.objects.get(
        #                 id=_team_member, merchant=request.user.sales_officer.merchant
        #             )
        #             list_of_team_members.append(team_member)
        #         except TeamMember.DoesNotExist:
        #             return Response(
        #                 {"message": "Team member does not exist"}, status=status.HTTP_404_NOT_FOUND
        #             )
        
        # Update deal
        deal.deal_title = name
        deal.description = description
        deal.deal_status = deal_status
        deal.merchant_overview = merchant_overview
        deal.industry = industry
        deal.pipeline_type = pipeline_type

        # if len(list_of_team_members) > 0:
        #     deal.team_member.set(list_of_team_members)

        deal.save()

        deal_serializer = DealSerializer(deal).data

        return Response(deal_serializer, status=status.HTTP_201_CREATED)

    def patch(self, request):
        """
        Partially update a deal by ID.

        Args:
        - request: HTTP request object.

        Returns:
        - Response: Result of partially updating the deal by ID.
        """

        id = request.GET.get("id", None)
        if id is None:
            return Response(
                {"message": "id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            deal = deal.objects.get(id=id)
        except deal.DoesNotExist:
            return Response(
                {"message": "Deal does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        name = request.data.get("name", deal.deal_title)
        description = request.data.get("description")
        deal_status = request.data.get("deal_status", "DRAFT")
        team_members = request.data.get("team_member")
        merchant_overview = request.data.get("merchant_overview")
        industry = request.data.get("industry")
        pipeline_type = request.data.get("pipeline_type")

        # Update deal
        deal.deal_title = name
        deal.description = description
        deal.deal_status = deal_status
        deal.merchant_overview = merchant_overview
        deal.industry = industry
        deal.team_members = team_members
        deal.pipeline_type = pipeline_type

        deal.save()

        # team_members = request.data.get("team_member")
        # if team_members is not None:
        #     list_of_team_members = []
        #     for _team_member_id in team_members:
        #         try:
        #             team_member = TeamMember.objects.get(
        #                 id=_team_member_id, company=request.user.recruiter.company
        #             )
        #             list_of_team_members.append(team_member)
        #         except TeamMember.DoesNotExist:
        #             return Response(
        #                 {"message": f"Team member with ID {_team_member_id} does not exist"},
        #                 status=status.HTTP_404_NOT_FOUND,
        #             )

        #     deal.team_member.set(list_of_team_members)

        deal_serializer = DealSerializer(deal).data

        return Response(deal_serializer, status=status.HTTP_200_OK)


# class TrackDealView(APIView):
#     def post(self, request):
#         unique_id = request.data.get("unique_id")
#         if unique_id is None:
#             return Response({"message": "unique_id is required."}, 
#     )
        

class StageView(APIView):
    # permission_classes = [IsAuthenticated, CanManageStage]
    permission_classes = [
        AllowAny, 
        # CanManageStage
    ]
    

    def post(self, request, pipeline_id):
        # Get the pipeline instance
        pipeline = get_object_or_404(Pipeline, id=pipeline_id)

        # Create a list to store newly created stages
        created_stages = []

        # Get the current maximum order of stages in the pipeline
        max_order = pipeline.stages.aggregate(max_order=Max("order"))["max_order"]
        if max_order is None:
            max_order = 0

        # Check if request data is a list of stages
        if isinstance(request.data, list):
            for stage_data in request.data:
                # Increment the order by 1
                max_order += 1

                # Add "order" field to each stage_data
                stage_data["order"] = max_order

                # Create a serializer instance for each stage data
                serializer = StageSerializer(data=stage_data)
                if serializer.is_valid():
                    # Save the stage and add it to the pipeline's stages
                    stage = serializer.save()
                    pipeline.stages.add(stage)
                    created_stages.append(stage)
                else:
                    # If any stage data is invalid, return error response
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            # Save the pipeline to persist changes
            pipeline.save()

            # Serialize the created stages and return success response
            created_stages_serializer = StageSerializer(created_stages, many=True)
            return Response(
                created_stages_serializer.data, status=status.HTTP_201_CREATED
            )
        else:
            # If request data is not a list, return error response
            return Response(
                {"error": "Request data should be a list of stages."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, pipeline_id):
        new_order = request.data.get("new_order", [])
        if new_order:
            try:
                # Get the pipeline instance
                pipeline = get_object_or_404(Pipeline, id=pipeline_id)

                # Retrieve stages based on the provided order
                stage_ids = [int(id) for id in new_order]
                stages = Stage.objects.filter(id__in=stage_ids, pipeline=pipeline)

                if len(stages) != len(stage_ids):
                    return Response(
                        {"error": "One or more stages do not belong to this pipeline."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Update the order of stages based on the provided order
                for index, stage_id in enumerate(stage_ids):
                    stage = stages.get(id=stage_id)
                    stage.order = (
                        index
                    )
                    stage.save()

                # Serialize the updated pipeline
                pipeline_serializer = PipelineSerializer(pipeline)

                return Response(
                    {
                        "message": "Stages reordered successfully.",
                        "deal_pipeline": pipeline_serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            except Pipeline.DoesNotExist:
                return Response(
                    {"error": "Pipeline does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except Stage.DoesNotExist:
                return Response(
                    {"error": "One or more stages do not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": "New order of stages not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, stage_id, **kwargs):
        try:
            stage = Stage.objects.get(id=stage_id)
        except Stage.DoesNotExist:
            raise NotFound(f"Stage with id {stage_id} does not exist.")

        serializer = StageSerializer(instance=stage, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, stage_id, **kwargs):
        try:
            stage = Stage.objects.get(id=stage_id)
            stage.delete()
            return Response(
                {"message": "Stage deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Stage.DoesNotExist:
            raise Http404(f"Stage with id {stage_id} does not exist.")


class PipelineView(APIView):
    # permission_classes = [IsAuthenticated, CanManagePipeline]
    permission_classes = [
        AllowAny, 
        # CanManagePipeline
    ]

    def get(self, request, pipeline_id):
        pipeline = get_object_or_404(Pipeline, id=pipeline_id)

        serializer = PipelineSerializer(pipeline)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PipelineSerializer(data=request.data)
        if serializer.is_valid():
            sales_officer = SalesOfficer.objects.get(user=self.request.user)
            serializer.validated_data["sales_officer"] = sales_officer
            serializer.validated_data["company"] = sales_officer.merchant

            if not serializer.validated_data.get("is_default"):
                # If it's a custom pipeline, ensure "New candidate" stage is added
                with transaction.atomic():
                    new_pipeline = serializer.save()
                    new_merchant_stage = Stage.objects.create(
                        name="New candidate", order=0, is_new_candidate=True
                    )
                    new_pipeline.stages.add(new_merchant_stage)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pipeline_id):
        try:
            pipeline = Pipeline.objects.get(id=pipeline_id)
        except Pipeline.DoesNotExist:
            return Response(
                {"error": "Pipeline not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PipelineSerializer(pipeline, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pipeline_id):
        try:
            pipeline = Pipeline.objects.get(id=pipeline_id)
        except Pipeline.DoesNotExist:
            return Response(
                {"error": "Pipeline not found."}, status=status.HTTP_404_NOT_FOUND
            )

        pipeline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class AddTeamMemberView(CreateAPIView):
#     """
#     API endpoint for adding team members to manage a merchant.

#     Requires JWT authentication.

#     Attributes:
#     - queryset: Queryset of all team members.
#     - serializer_class: Serializer class for team member data.
#     - permission_classes: Permission classes required for access.

#     Methods:
#     - perform_create(serializer): Custom method to perform the creation of a team member instance.
#     - create(request, *args, **kwargs): Custom method to handle creation requests, supports bulk addition of team members.

#     Returns:
#     - 201 Created: Team member(s) added successfully.
#     - 400 Bad Request: If the provided data is invalid or a recruiter with the provided email does not exist.
#     """

#     queryset = TeamMember.objects.all()
#     serializer_class = TeamMemberSerializer
#     # permission_classes = [IsAuthenticated]
#     permission_classes = [AllowAny]

#     def perform_create(self, serializer):
#         """
#         Perform creation of a team member instance.

#         Args:
#         - serializer: Serializer instance for team member data.

#         Raises:
#         - ValidationError: If a recruiter with the provided email does not exist.
#         """

#         try:
#             salesofficer = SalesOfficer.objects.get(user=self.request.user)
#         except ObjectDoesNotExist:
#             raise ValidationError("SalesOfficer with the provided email does not exist.")

#         # Set the company and member fields of the TeamMember instance
#         merchant = salesofficer.merchant
#         member = salesofficer
#         serializer.save(merchant=merchant, member=member)

#     def create(self, request, *args, **kwargs):
#         """
#         Create method to handle creation requests, supports bulk addition of team members.

#         Args:
#         - request: HTTP request object.
#         - *args, **kwargs: Additional arguments and keyword arguments.

#         Returns:
#         - Response: HTTP response containing the result of the operation.
#         """

#         # Support bulk addition by handling a list of team members
#         data = request.data
#         if isinstance(data, list):
#             serializer = self.get_serializer(data=data, many=True)
#         else:
#             serializer = self.get_serializer(data=data)

#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             serializer.data, status=status.HTTP_201_CREATED, headers=headers
#         )

    
# class InviteTeamMemberView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         if not isinstance(request.data, list):
#             return Response(
#                 {"error": "Payload should be a list of dictionaries"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         sales_officer = SalesOfficer.objects.get(user=request.user)
#         company_id = sales_officer.company.id

#         for recipient in request.data:
#             if not isinstance(recipient, dict):
#                 return Response(
#                     {"error": "Each item in the list should be a dictionary"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             recipient_email = recipient.get("recipient_email")
#             role = recipient.get("role")
#             type_of_recruiter = recipient.get("type_of_recruiter")

#             if not recipient_email or not role or not type_of_recruiter:
#                 return Response(
#                     {"error": "recipient_email, role, and type_of_recruiter are required fields"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             send_team_member_invite_mail(recipient_email, sales_officer, company_id, role, type_of_recruiter)

#         return Response(
#             {"message": "Invitations sent successfully"},
#             status=status.HTTP_200_OK
#         )
    

# class AcceptTeamMemberInviteView(APIView):
#     pass


# class RemoveTeamMemberView(DestroyAPIView):
#     """
#     API endpoint for removing a team member from managing a merchant.

#     Requires JWT authentication.

#     Attributes:
#     - queryset: Queryset of all team members.
#     - permission_classes: Permission classes required for access.

#     Methods:
#     - perform_destroy(instance): Custom method to perform the deletion of a team member instance.
#     - get_object(): Custom method to retrieve the team member instance to be deleted.
#     - destroy(request, *args, **kwargs): Custom method to handle deletion requests.

#     Returns:
#     - 204 No Content: Team member removed successfully.
#     - 403 Forbidden: If the requesting recruiter is not authorized to remove the team member.
#     - 404 Not Found: If the team member to be removed does not exist.
#     """

#     queryset = TeamMember.objects.all()
#     # permission_classes = [IsAuthenticated]
#     permission_classes = [AllowAny]

#     def perform_destroy(self, instance):
#         """
#         Perform deletion of a team member instance.

#         Args:
#         - instance: Team member instance to be deleted.
#         """

#         instance.delete()

#     def get_object(self):
#         """
#         Retrieve the team member instance to be deleted.

#         Returns:
#         - Team member instance to be deleted.

#         Raises:
#         - Http404: If the team member to be removed does not exist.
#         """

#         queryset = self.get_queryset()
#         try:
#             email = self.request.data.get("recruiter_email")
#             instance = queryset.get(member__user__email=email)
#         except ObjectDoesNotExist:
#             raise Http404("Team member not found.")
#         self.check_object_permissions(self.request, instance)
#         return instance

#     def destroy(self, request, *args, **kwargs):
#         """
#         Handle deletion requests for removing a team member.

#         Returns:
#         - Response: HTTP response indicating the result of the operation.
#         """

#         instance = self.get_object()

#         # Check if the recruiter requesting the removal is the same as the team member being removed
#         sales_officer = SalesOfficer.objects.get(user=request.user)
#         if instance.member != sales_officer:
#             return Response(status=status.HTTP_403_FORBIDDEN)

#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

# class UpdateTeamMemberRoleView(UpdateAPIView):
#     """
#     API endpoint for updating the role of a team member that is managing a merchant.

#     Requires JWT authentication.

#     Attributes:
#     - queryset: Queryset of all team members.
#     - serializer_class: Serializer class for team member data.
#     - permission_classes: Permission classes required for access.

#     Methods:
#     - perform_update(serializer): Custom method to perform the update of a team member instance.
#     - update(request, *args, **kwargs): Custom method to handle update requests.

#     Returns:
#     - Updated team member details.
#     """

#     queryset = TeamMember.objects.all()
#     serializer_class = TeamMemberSerializer
#     # permission_classes = [IsAuthenticated]
#     permission_classes = [AllowAny]

#     def perform_update(self, serializer):
#         """
#         Perform update of a team member instance.

#         Args:
#         - serializer: Serializer instance for team member data.
#         """

#         serializer.save()

#     def update(self, request, *args, **kwargs):
#         """
#         Handle update requests for updating the role of a team member.

#         Returns:
#         - Response: HTTP response containing the updated team member details.
#         """

#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)


# class TeamMemberRoleView(APIView):
#     """
#     API endpoint for retrieving team member roles.

#     Attributes:
#     - None

#     Methods:
#     - get(request, id=None): Custom method to handle retrieval of team member roles.

#     Returns:
#     - Response: List of all team member roles or details of a specific role.
#     """

#     def get(self, request, id=None):
#         """
#         Retrieve team member roles.

#         Args:
#         - request: HTTP request object.
#         - id (optional): Identifier of the specific team member role to retrieve.

#         Returns:
#         - Response: List of all team member roles or details of a specific role.
#         """

#         if id:
#             role = TeamMemberRole.objects.get(id=id)
#             serializer = TeamMemberRoleSerializer(role)
#         else:
#             roles = TeamMemberRole.objects.all()
#             serializer = TeamMemberRoleSerializer(roles, many=True)
#         return Response(serializer.data)


# class TeamMemberPermissionView(APIView):
#     """
#     API endpoint for retrieving team member permissions.

#     Attributes:
#     - None

#     Methods:
#     - get(request, id=None): Custom method to handle retrieval of team member permissions.

#     Returns:
#     - Response: List of all team member permissions or details of a specific permission.
#     """

#     def get(self, request, id=None):
#         """
#         Retrieve team member permissions.

#         Args:
#         - request: HTTP request object.
#         - id (optional): Identifier of the specific team member permission to retrieve.

#         Returns:
#         - Response: List of all team member permissions or details of a specific permission.
#         """

#         if id:
#             permission = TeamMemberPermission.objects.get(id=id)
#             serializer = TeamMemberPermissionSerializer(permission)
#         else:
#             permissions = TeamMemberPermission.objects.all()
#             serializer = TeamMemberPermissionSerializer(permissions, many=True)
#         return Response(serializer.data)


# class TeamMemberRolePermissionView(APIView):
#     """
#     API endpoint for updating team member role permissions.

#     Attributes:
#     - None

#     Methods:
#     - patch(request, id): Custom method to handle partial updates of team member role permissions.

#     Returns:
#     - Response: Updated team member role permission details.
#     """

#     def patch(self, request, id):
#         """
#         Partially update team member role permissions.

#         Args:
#         - request: HTTP request object.
#         - id: Identifier of the team member role permission to update.

#         Returns:
#         - Response: Updated team member role permission details.
#         """

#         role_permission = get_object_or_404(TeamMemberRolePermission, id=id)

#         # Assuming 'permission' is a list of permission IDs in the request
#         permission_ids = request.data.get("permission", [])
#         if not isinstance(permission_ids, list):
#             return Response(
#                 {"permission": ["Invalid data. Expected a list."]},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         permissions = []
#         for permission_id in permission_ids:
#             permission = get_object_or_404(TeamMemberPermission, id=permission_id)
#             permissions.append(permission)

#         # Update the instance directly
#         role_permission.permission.set(permissions)

#         # Optionally, update other fields
#         role_permission.role = request.data.get("role", role_permission.role)
#         role_permission.company = request.data.get("company", role_permission.company)
#         role_permission.save()

#         # Serialize the updated instance
#         serializer = TeamMemberRolePermissionSerializer(role_permission)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class RolePermissionsView(APIView):
#     """
#     API endpoint for retrieving permissions associated with a specific merchant.

#     Attributes:
#     - None

#     Methods:
#     - get(request, role_id): Custom method to retrieve role permissions.

#     Returns:
#     - Response: Permissions associated with the specified role.
#     """

#     def get(self, request, role_id):
#         """
#         Retrieve permissions associated with a specific merchant.

#         Args:
#         - request: HTTP request object.
#         - role_id: Identifier of the role to retrieve permissions for.

#         Returns:
#         - Response: Permissions associated with the specified role.
#         """

#         merchant = request.user.merchant
#         company = merchant.company
#         role = get_object_or_404(TeamMemberRole, id=role_id)
#         role_permissions = TeamMemberRolePermission.objects.filter(
#             role=role, company=company
#         ).first()
#         if role_permissions:
#             # permissions = role_permissions.permission.values_list('name', flat=True)
#             # return Response({'permissions': permissions})
#             serializer = TeamMemberRolePermissionSerializer(role_permissions)
#             return Response(serializer.data)
#         else:
#             return Response(
#                 {"error": "Role permissions not found for the merchant."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
        

# class SalesOfficerTeamView(generics.ListAPIView):
#     """
#     API endpoint for retrieving the team members associated with the salesofficer's company.

#     Requires JWT authentication.

#     Attributes:
#     - serializer_class: Serializer class for team member data.
#     - permission_classes: Permission classes required for access.

#     Methods:
#     - get_queryset(): Custom method to retrieve the queryset of team members.

#     Returns:
#     - List of team members associated with the salesofficer's company.
#     """

#     serializer_class = NewTeamMemberSerializer
#     # permission_classes = [IsAuthenticated]
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         """
#         Retrieve the queryset of team members associated with the salesofficer's company.

#         Returns:
#         - Queryset: List of team members associated with the salesofficer's company.

#         Note:
#         - Requires JWT authentication.
#         """

#         sales_officer_instance = None
#         if hasattr(self.request.user, "salesofficer"):
#             sales_officer_instance = self.request.user.sales_officer

#         if sales_officer_instance is None:
#             return Response(
#                 {"message": "Salesofficer does not exist"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         user = self.request.user
#         sales_officer = get_object_or_404(SalesOfficer, user=user)

#         # Check if the recruiter is a team member
#         team_memberships = TeamMember.objects.filter(member=sales_officer)

#         if team_memberships.exists():
#             # Get the company from the first team membership (assuming the salesofficer can belong to only one company)
#             merchant = team_memberships.first().company

#             # Get all team members for the salesofficer's company
#             return TeamMember.objects.filter(company=merchant)
        

# class DealProgression(APIView):
#     """
#     API endpoint for managing deal progression within stages.

#     Methods:
#     - post(request): Move deals to a specified stage within a deal's pipeline.
#     - delete(request): Remove deals from stages.

#     Returns:
#     - Response: Result of deal progression operations.
#     """

#     def post(self, request):
#         """
#         Move deals to a specified stage within the pipeline.

#         Args:
#         - request: HTTP request object containing deal_unique_id, stage_id, and task_ids.

#         Returns:
#         - Response: Result of moving deals to the specified stage.
#         """
#         # Get the user instance associated with the request
#         user_instance = UserAccount.objects.get(email=request.user)

#         deal_unique_id = request.data.get("deal_unique_id")
#         stage_id = request.data.get("stage_id")
#         dealprogression_unique_ids = request.data.get("dealprogression_unique_ids", [])

#         if not deal_unique_id:
#             return Response(
#                 {"message": "Deal unique ID is required"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             deal = Deal.objects.get(unique_id=deal_unique_id)
#             pipeline = deal.pipeline
#             stage_instance = pipeline.stages.get(id=stage_id)
#         except Deal.DoesNotExist:
#             return Response(
#                 {"message": "Invalid deal unique ID"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         except Stage.DoesNotExist:
#             return Response(
#                 {"message": "Invalid stage ID"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         for dealprogression_unique_id in dealprogression_unique_ids:
#             try:
#                 deal = Deal.objects.get(id=dealprogression_unique_id)
#                 old_stage_id = deal.deal_stage
#                 deal.current_stage = stage_instance
#                 # deal_progression.deal_stage = stage_instance.name
#                 deal.save()

#                 # Retrieve the full name of the user
#                 user_fullname = user_instance.get_fullname()

#                 # Update trail
#                 trail_entry = {
#                     "event": "progression",
#                     "timestamp": timezone.now().isoformat(),
#                     "deal_name": deal.name,
#                     "stage_name": stage_instance.name,
#                     "moved_by": user_fullname
#                 }
#                 deal.trail.append(trail_entry)
#                 deal.save()

#                 # Send email notification if enabled for the stage
#                 if stage_instance.email_notification_enabled:
#                     stage_notification(stage_instance, deal)

#             except Deal.DoesNotExist:
#                 continue
#         deal_count = Deal.deal_progression_count(unique_id=dealprogression_unique_id)
#         return Response(
#             {
#                 "message": f"Your deal has been moved to {stage_instance.name} stage"
#             }
#         )

#     def delete(self, request):
#         """
#         Remove deals from stages.

#         Args:
#         - request: HTTP request object containing deal_ids.

#         Returns:
#         - Response: Result of removing candidates from stages.
#         """

#         deal_ids = request.data.get("deal_ids", [])

#         for deal_id in deal_ids:
#             try:
#                 deal = Deal.objects.get(id=deal_id)
#                 old_stage_id = deal.current_stage
#                 deal.current_stage = None
#                 deal.save()

#                 # Update counts for the stages
#                 if old_stage_id:
#                     old_stage = Stage.objects.get(id=old_stage_id)
#                     old_stage.deal_count = F("deal_count") - 1
#                     old_stage.save()

#             except Deal.DoesNotExist:
#                 continue

#         return Response({"message": "Deal removed from stages"})

# # class SalesOfficerPipelinesAPIView(APIView):

# #     def get(self, request):
# #         sales_officer = get_object_or_404(SalesOfficer, user=request.user)
# #         merchant = sales_officer.company
# #         pipelines = Pipeline.objects.filter(
# #             sales_officer=sales_officer, merchant=merchant, is_default=False
# #         )

# #         paginator = CustomPageNumberPagination()
# #         result_page = paginator.paginate_queryset(pipelines, request)

# #         serializer = PipelineSerializer(result_page, many=True)

# #         return paginator.get_paginated_response(serializer.data)


# class SalesOfficersPipelines(APIView):
#     pagination_class = CustomPagination

#     def get(self, request):
#         sales_officer = get_object_or_404(SalesOfficer, user=request.user)
#         merchant = sales_officer.merchant

#         # Filter pipelines where is_default is set to false
#         pipelines = Pipeline.objects.filter(
#             sales_officer=sales_officer, merchant=merchant, is_default=False
#         )

#         serializer = PipelineSerializer(pipelines, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class CreateRolesAndPermissionsAPIView(APIView):
#     def post(self, request):
#         try:
#             with transaction.atomic():
#                 create_roles_and_permissions()
#             return Response(
#                 {"message": "Roles and permissions created successfully."},
#                 status=status.HTTP_201_CREATED,
#             )
#         except Exception as e:
#             return Response(
#                 {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

# class ChangeDealStageView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = ChangeDealStageSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         deal_id = serializer.validated_data.get("deal_id")
#         stage_id = serializer.validated_data.get("stage_id")

#         try:
#             if deal_id:
#                 deal = Deal.objects.get(id=deal_id)

#         except deal.ObjectDoesNotExist:
#             res = DataResponse(success=False, data=[], status_code=400, message="Deal Application does not exist")
#             return res.respond()

#         try:
#             if stage_id:
#                 stage = Stage.objects.get(id=stage_id)

#         except stage.ObjectDoesNotExist:
#             res = DataResponse(success=False, data=[], status_code=400, message="Pipeline Stage does not exist")
#             return res.respond()

#         deal.current_stage = stage
#         return Response(
#             {"message": f"Candidate successfully moved to the next stage"},
#             status=status.HTTP_200_OK,
#         )


# class FetchCreatedDealsView(APIView):
#     """
#     API endpoint for fetching deals created by a sales officer or their team members.

#     Attributes:
#     - authentication_classes: List of authentication classes required for accessing the endpoint.
#     - permission_classes: List of permission classes required for accessing the endpoint.

#     Methods:
#     - get(request): Retrieves deals created by the authenticated sales officer or their team members.

#     Returns:
#     - Response: Paginated list of deal data including total deal count.
#     """

#     authentication_classes = [JWTAuthentication]
#     # permission_classes = [IsAuthenticated]
#     permission_classes = [AllowAny]

#     def get(self, request):
#         """
#         Retrieves deals created by the authenticated sales officer or their team members

#         Args:
#         - request: HTTP request object containing query parameters for filtering deals.

#         Returns:
#         - Response: Paginated list of deal data including total task & activity count for each deal.
#         """

#         sales_officer = SalesOfficer.objects.get(user=request.user)

#         user = request.user
#         sales_officer = get_object_or_404(SalesOfficer, user=user)

#         # Check if the sales officer is a team member
#         team_memberships = TeamMember.objects.filter(member=sales_officer)

#         if team_memberships.exists():
#             # Get the merchant from the first team membership (assuming the sales officer can belong to only one company)
#             merchant = team_memberships.first().company

#             # Get all team members for the sales officer's company 
#             team_members = TeamMember.objects.filter(merchant=merchant)
#             member_ids = team_members.values_list("member_id", flat=True)
#         else:
#             # If the sales officer is not part of any team, use only their own ID
#             member_ids = [sales_officer.id]

#         # Fetch all deals created by these team members or the sales officer
#         deals = Deal.objects.filter(sales_officer_id__in=member_ids).order_by("-created_at")

#         # Apply filters if provided in the query parameters
#         search = request.GET.get("search", None)
#         if search:
#             deals = deals.filter(deal_title__icontains=search)

#         unique_id = request.GET.get("unique_id", None)
#         if unique_id:
#             deals = deals.filter(unique_id=unique_id)
        
#         deal_title = request.GET.get("deal_title", None)
#         if deal_title:
#             deals = deals.filter(deal_title__icontains=deal_title)

#         deal_status = request.GET.get("deal_status", None)
#         if deal_status:
#             deals = deals.filter(deal_status=deal_status)

#         # Create a dictionary to map deal IDs to total deals count
#         total_deals_map = {
#             count["deal_id"]: count["total_deals"] for count in total_deals_map
#         } 

#         deals_data = []
#         for deal in deals:
#             deal_data = DealSerializer(deal).data
#             deal_data["total_deals"] = total_deals_map.get(deal.id, 0)
#             deals_data.append(deal_data)

#         paginator = CustomPageNumberPagination()
#         result_page = paginator.paginate_queryset(deals_data, request)

#         return paginator.get_paginated_response(result_page)
    

# class FetchCreatedActivitiesView(APIView):
#     """
#     API endpoint for fetching activities created by a sales officer or their team members.

#     Attributes:
#     - authentication_classes: List of authentication classes required for accessing the endpoint.
#     - permission_classes: List of permission classes required for accessing the endpoint.

#     Methods:
#     - get(request): Retrieves activities created by the authenticated sales officer or their team members.

#     Returns:
#     - Response: Paginated list of activity data including activity count.
#     """

#     authentication_classes = [JWTAuthentication]
#     # permission_classes = [IsAuthenticated]
#     permission_classes = [AllowAny]

#     def get(self, request):
#         """
#         Retrieves activities created by the authenticated sales officer or their team members

#         Args:
#         - request: HTTP request object containing query parameters for filtering activities.

#         Returns:
#         - Response: Paginated list of activity data including total activity count for each deal.
#         """

#         sales_officer = SalesOfficer.objects.get(user=request.user)

#         user = request.user
#         sales_officer = get_object_or_404(SalesOfficer, user=user)

#         # Check if the sales officer is a team member
#         team_memberships = TeamMember.objects.filter(member=sales_officer)

#         if team_memberships.exists():
#             # Get the merchant from the first team membership (assuming the sales officer can belong to only one company)
#             merchant = team_memberships.first().company

#             # Get all team members for the sales officer's company 
#             team_members = TeamMember.objects.filter(merchant=merchant)
#             member_ids = team_members.values_list("member_id", flat=True)
#         else:
#             # If the sales officer is not part of any team, use only their own ID
#             member_ids = [sales_officer.id]

#         # Fetch all activities created by these team members or the sales officer
#         activities = Activity.objects.filter(sales_officer_id__in=member_ids).order_by("-created_at")

#         # Apply filters if provided in the query parameters
#         search = request.GET.get("search", None)
#         if search:
#             activities = activities.filter(deal_title__icontains=search)

#         unique_id = request.GET.get("unique_id", None)
#         if unique_id:
#             activities = activities.filter(unique_id=unique_id)
        
#         activity_title = request.GET.get("activity_title", None)
#         if activity_title:
#             activities = activities.filter(deal_title__icontains=activity_title)

#         # deal_status = request.GET.get("deal_status", None)
#         # if deal_status:
#         #     deals = deals.filter(deal_status=deal_status)

#         # Create a dictionary to map deal IDs to total deals count
#         total_activities_map = {
#             count["activity_id"]: count["total_activities"] for count in total_activities_map
#         } 

#         activities_data = []
#         for activity in activities:
#             activity_data = ActivitySerializer(activity).data
#             activity_data["total_activities"] = total_activities_map.get(activity.id, 0)
#             activities_data.append(activity_data)

#         paginator = CustomPageNumberPagination()
#         result_page = paginator.paginate_queryset(activities_data, request)

#         return paginator.get_paginated_response(result_page)
    

# class FetchCreatedTasksView(APIView):
#     """
#     API endpoint for fetching tasks created by a sales officer or their team members.

#     Attributes:
#     - authentication_classes: List of authentication classes required for accessing the endpoint.
#     - permission_classes: List of permission classes required for accessing the endpoint.

#     Methods:
#     - get(request): Retrieves tasks created by the authenticated sales officer or their team members.

#     Returns:
#     - Response: Paginated list of task data.
#     """

#     authentication_classes = [JWTAuthentication]
#     # permission_classes = [IsAuthenticated]
#     permission_classes = [AllowAny]

#     def get(self, request):
#         """
#         Retrieves tasks created by the authenticated sales officer or their team members

#         Args:
#         - request: HTTP request object containing query parameters for filtering tasks.

#         Returns:
#         - Response: Paginated list of task data including total task count for each deal.
#         """

#         sales_officer = SalesOfficer.objects.get(user=request.user)

#         user = request.user
#         sales_officer = get_object_or_404(SalesOfficer, user=user)

#         # Check if the sales officer is a team member
#         team_memberships = TeamMember.objects.filter(member=sales_officer)

#         if team_memberships.exists():
#             # Get the merchant from the first team membership (assuming the sales officer can belong to only one company)
#             merchant = team_memberships.first().company

#             # Get all team members for the sales officer's company 
#             team_members = TeamMember.objects.filter(merchant=merchant)
#             member_ids = team_members.values_list("member_id", flat=True)
#         else:
#             # If the sales officer is not part of any team, use only their own ID
#             member_ids = [sales_officer.id]

#         # Fetch all tasks created by these team members or the sales officer
#         tasks = Task.objects.filter(sales_officer_id__in=member_ids).order_by("-created_at")

#         # Apply filters if provided in the query parameters
#         search = request.GET.get("search", None)
#         if search:
#             tasks = tasks.filter(deal_title__icontains=search)

#         unique_id = request.GET.get("unique_id", None)
#         if unique_id:
#             tasks = tasks.filter(unique_id=unique_id)
        
#         task_title = request.GET.get("deal_title", None)
#         if task_title:
#             tasks = tasks.filter(task_title__icontains=task_title)

#         # deal_status = request.GET.get("deal_status", None)
#         # if deal_status:
#         #     deals = deals.filter(deal_status=deal_status)

#         # Create a dictionary to map deal IDs to total deals count
#         total_tasks_map = {
#             count["task_id"]: count["total_tasks"] for count in total_tasks_map
#         } 

#         tasks_data = []
#         for task in tasks:
#             task_data = TaskSerializer(task).data
#             task_data["total_tasks"] = total_tasks_map.get(task.id, 0)
#             tasks_data.append(task_data)

#         paginator = CustomPageNumberPagination()
#         result_page = paginator.paginate_queryset(tasks_data, request)

#         return paginator.get_paginated_response(result_page)
