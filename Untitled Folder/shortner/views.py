import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user_agents import parse
from .models import Url, UrlClick
from django.db.models import F
import random
import string
from django.contrib import messages

# ================================
# Dashboard View
# ================================
@login_required
def dashboard(request):
    user_urls = Url.objects.filter(user=request.user).order_by('-created_at')
    total_urls = user_urls.count()
    total_clicks = sum(url.click_count for url in user_urls)

    # Build absolute short URLs
    for url in user_urls:
        url.full_short_url = request.build_absolute_uri(f'/{url.uuid}/')  # <-- Make sure uuid exists!

    context = {
        'user_urls': user_urls,
        'total_urls': total_urls,
        'total_clicks': total_clicks,
    }
    return render(request, 'shortner/home.html', context)


# ================================
# Home / Landing Page
# ================================
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect logged-in users to dashboard
    else:
        return redirect('login')      # Redirect guests to login page


# ================================
# Create Short URL via AJAX
# ================================
# ================================
# Helper Function: Generate UID
# ================================
def generate_uid(length=6):
    """Generate a random alphanumeric UID for short URL"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ================================
# Helper Function: Get Client IP
# ================================
def get_client_ip(request):
    """Get client IP address from request headers"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

# ================================
# Create Short URL via AJAX
# ================================

@login_required
def create(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        if not link:
            messages.error(request, "No link provided.")
            return JsonResponse({"error": "No link provided"}, status=400)

        # Generate unique 6-character UID
        uid = str(uuid.uuid4())[:6]

        # Create short URL object
        url_obj = Url.objects.create(user=request.user, link=link, uuid=uid)

        # Full short URL
        short_url = request.build_absolute_uri(f'/{uid}')
        url_obj.full_short_url = short_url
        url_obj.save()

        # Add session message (will show after reload)
        messages.success(request, "Short URL created successfully!")

        # Return JSON (optional) if you still want AJAX dynamic messages
        return JsonResponse({
            "id": url_obj.id,
            "link": url_obj.link,
            "click_count": url_obj.click_count,
            "created_at": url_obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "full_short_url": short_url,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

# =====================
# Edit URL
# =====================
@login_required
def edit_url(request, id):
    url_obj = get_object_or_404(Url, id=id, user=request.user)

    if request.method == 'POST':
        new_link = request.POST.get('link')
        if not new_link:
            return JsonResponse({"error": "URL cannot be empty!"}, status=400)

        url_obj.link = new_link
        url_obj.save()
        return JsonResponse({"success": True, "link": new_link})

    return JsonResponse({"error": "Invalid request"}, status=400)

# =====================
# Delete URL
# =====================
@login_required
def delete_url(request, id):
    url_obj = get_object_or_404(Url, id=id, user=request.user)

    if request.method == 'POST':
        url_obj.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)

# ================================
# Redirect Short URL
# ================================
def redirect_short_url(request, uuid):
    """
    Redirect short URL to the original link
    and log click details
    """
    # Get URL object
    url_obj = get_object_or_404(Url, uuid=uuid, is_active=True)

    # Atomic click count increment
    Url.objects.filter(pk=url_obj.pk).update(click_count=F('click_count') + 1)

    # Parse user agent
    ua_string = request.META.get('HTTP_USER_AGENT', '')
    ua = parse(ua_string)

    # Save click details safely
    UrlClick.objects.create(
        url=url_obj,
        ip_address=get_client_ip(request),
        user_agent=ua_string or '',
        platform=getattr(ua.os, 'family', '') or '',
        browser=getattr(ua.browser, 'family', '') or '',
        device=getattr(ua.device, 'family', '') or '',
    )

    # Redirect to original URL
    return redirect(url_obj.link)


@login_required
@login_required
def clicks_url(request, id):  # <- 'id' comes from the URL pattern
    # Only show URLs belonging to the logged-in user
    url_obj = get_object_or_404(Url, id=id, user=request.user)

    # Get all clicks for this URL
    clicks = UrlClick.objects.filter(url=url_obj).order_by('-created_at')

    context = {
        'url': url_obj,
        'clicks': clicks,
    }
    return render(request, 'shortner/clicks.html', context)


@login_required
def delete_click(request, id):
    """
    Delete a single click record via AJAX
    """
    if request.method == 'POST':
        click = get_object_or_404(UrlClick, id=id)

        # Optional: make sure this click belongs to a URL of the logged-in user
        if click.url.user != request.user:
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)

        click.delete()
        return JsonResponse({'success': True})

    # If not POST
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
