from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from tasks.models import Position, TaskType, Task, Worker, Tag


admin.site.unregister(Group)


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
        "get_assignees",
        "is_completed",
    ]
    list_editable = ["deadline", "priority", "is_completed"]
    list_filter = ["deadline", "priority", "task_type", "tags"]
    list_select_related = ["task_type"]
    date_hierarchy = "deadline"

    @admin.display(description="Assignees")
    def get_assignees(self, obj):
        return (", ".join(worker.username for worker in obj.assignees.all())
                or "-")

    @admin.display(description="Tags")
    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all()) or "-"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("assignees", "tags")


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    search_fields = [
        "username",
        "email",
        "position__name",
    ]
    list_display = [
        "username",
        "position",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    ]
    list_filter = ["position", "is_staff"]
    list_select_related = ["position"]
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
