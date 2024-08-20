from django.contrib import admin
from .models import * 


class StageAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Stage._meta.fields]

class PipelineAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Pipeline._meta.fields]

class DealAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Deal._meta.fields]

class LeadAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Lead._meta.fields]

class ActivityAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Activity._meta.fields]

class TaskAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Task._meta.fields]
    
class TaskNotificationAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in TaskNotification._meta.fields]

class TeamMemberRoleAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in TeamMemberRole._meta.fields]


# Register your models here.
admin.site.register(Pipeline, PipelineAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Deal, DealAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskNotification, TaskNotificationAdmin)
admin.site.register(TeamMemberRole, TeamMemberRoleAdmin)
