from django.contrib import admin

from audit.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Read-only general log with filters (§32)."""

    list_display = ("timestamp", "user", "action", "content_object", "organisation", "undone")
    list_filter = ("action", "user", "content_type", "undone", "organisation")
    search_fields = ("object_id", "changes")
    date_hierarchy = "timestamp"
    readonly_fields = (
        "user", "organisation", "timestamp", "action",
        "content_type", "object_id", "changes", "session", "undone",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
