from django.db import models
from django.contrib.auth.models import User
import uuid

class Url(models.Model):
    link = models.URLField(max_length=10000)
    uuid = models.CharField(max_length=10, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls')
    click_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.uuid} -> {self.link}"

    def short_url(self, request=None):
        if request:
            protocol = 'https' if request.is_secure() else 'http'
            host = request.get_host()
            return f"{protocol}://{host}/{self.uuid}"
        return f"/{self.uuid}"


# ✅ NEW: UrlClick model to track click details
class UrlClick(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE, related_name='clicks')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    platform = models.CharField(max_length=100, blank=True, null=True)
    browser = models.CharField(max_length=100, blank=True, null=True)
    device = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Click on {self.url.uuid} at {self.created_at} from {self.ip_address}"