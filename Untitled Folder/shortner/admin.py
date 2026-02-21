from django.contrib import admin
from .models import Url, UrlClick
from django.utils.html import format_html

# Url admin
@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_url_admin', 'link_preview', 'user', 'click_count', 'is_active', 'created_at')
    list_display_links = ('short_url_admin', 'link_preview')
    search_fields = ('uuid', 'link', 'user__username')
    list_filter = ('is_active', 'created_at', 'user')
    ordering = ('-created_at',)

    def link_preview(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.link, obj.link)
    link_preview.short_description = "Original Link"

    def short_url_admin(self, obj):
        return format_html('<a href="/{}" target="_blank">{}</a>', obj.uuid, obj.uuid)
    short_url_admin.short_description = "Short URL"


# UrlClick admin
@admin.register(UrlClick)
class UrlClickAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'ip_address', 'browser', 'platform', 'device', 'created_at')
    search_fields = ('url__uuid', 'ip_address', 'browser', 'platform', 'device')
    list_filter = ('created_at', 'platform', 'browser')
    ordering = ('-created_at',)