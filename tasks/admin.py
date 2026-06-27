from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import Position, TaskType, Task, Worker, Tag


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "task_type__name",
        "tags__name",
    ]
    list_display = [
        "name",
        "task_type",
        "get_tags",
        "deadline",
        "priority",
        "get_assignees"
    ]
    list_filter = ["deadline", "priority", "task_type", "tags"]

    def get_assignees(self, obj):
        return ", ".join([worker.username for worker in obj.assignees.all()])
    get_assignees.short_description = "Assignees"

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = "Tags"

    def get_queryset(self, request):
        qs = super(TaskAdmin, self).get_queryset(request)
        return (qs.select_related("task_type").
                prefetch_related("assignees", "tags"))


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    search_fields = ["username", "position__name"]
    list_display = [
        "username",
        "position",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    ]
    list_filter = ["position", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (("Additional info:",
                                        {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info:",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "position",
                )
            },
        ),
    )

    def get_queryset(self, request):
        qs = super(WorkerAdmin, self).get_queryset(request)
        return qs.select_related("position")
