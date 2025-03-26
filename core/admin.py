from django.contrib import admin
from core.models import User, Task, TaskAssignment, Team, TeamRoles

class TaskAssignmentInline(admin.TabularInline):
    model = TaskAssignment
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'task_type', 'created_at', 'completed_at', 'status')
    list_filter = ('task_type', 'status')
    search_fields = ('name', 'description')
    inlines = [TaskAssignmentInline]

class UserTeamInline(admin.TabularInline):
    model = TeamRoles
    extra = 1

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile')
    search_fields = ('username', 'email', 'mobile')
    inlines = [UserTeamInline]

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner__username')
    inlines = [UserTeamInline]

admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Team, TeamAdmin)