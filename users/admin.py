# users/admin.py
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
import os

# Optional: hide default Group admin
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # Attractive list display including groups
    list_display = (
        'id', 'user_photo', 'full_name', 'username', 'email',
        'groups_list', 'is_staff_icon', 'is_superuser_icon', 'is_active_icon',
        'date_joined', 'last_login',
    )

    # Clickable links to edit
    list_display_links = ('full_name', 'username')

    # Profile photo column
    def user_photo(self, obj):
        photo_path = f'media/profile_photos/{obj.username}.jpg'
        if os.path.exists(photo_path):
            return format_html(
                '<img src="/media/profile_photos/{}.jpg" width="50" height="50" style="border-radius:50%; object-fit:cover; border:2px solid #ddd"/>',
                obj.username
            )
        # Default avatar (first letter)
        return format_html(
            '<div style="width:50px;height:50px;border-radius:50%;background:#ccc;text-align:center;line-height:50px;color:#fff;font-weight:bold;">{}<div>',
            obj.username[0].upper()
        )
    user_photo.short_description = "Photo"
    user_photo.admin_order_field = 'id'

    # Full name column
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Full Name"
    full_name.admin_order_field = 'first_name'

    # Groups column
    def groups_list(self, obj):
        if obj.groups.exists():
            return ", ".join([g.name for g in obj.groups.all()])
        return "-"
    groups_list.short_description = "Groups"

    # Status columns
    def is_staff_icon(self, obj):
        color = "green" if obj.is_staff else "red"
        return format_html('<b style="color:{};">{}</b>', color, "Yes" if obj.is_staff else "No")
    is_staff_icon.short_description = "Staff"

    def is_superuser_icon(self, obj):
        color = "gold" if obj.is_superuser else "gray"
        return format_html('<b style="color:{};">{}</b>', color, "Yes" if obj.is_superuser else "No")
    is_superuser_icon.short_description = "Admin"

    def is_active_icon(self, obj):
        color = "green" if obj.is_active else "red"
        return format_html('<b style="color:{};">{}</b>', color, "Yes" if obj.is_active else "No")
    is_active_icon.short_description = "Active"

# Unregister default User and register new UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)