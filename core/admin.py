from django.contrib import admin
from core.models import User, Task, TaskAssignment

class TaskAssignmentInline(admin.TabularInline):
    model = TaskAssignment
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'task_type', 'created_at', 'completed_at', 'status')
    list_filter = ('task_type', 'status')
    search_fields = ('name', 'description')
    inlines = [TaskAssignmentInline]

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile', 'role')
    list_filter = ('role',)
    search_fields = ('username', 'email', 'mobile')

admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)