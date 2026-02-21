from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # ✅ Home / index page
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create, name='create'),
    path('<str:uuid>/', views.redirect_short_url, name='redirect'),
    path('edit/<int:id>/', views.edit_url, name='edit_url'),
    path('delete/<int:id>/', views.delete_url, name='delete_url'),
    path('clicks/url/<int:id>/', views.clicks_url, name='clicks_url'),          # New Clicks page
    path('click/delete/<int:id>/', views.delete_click, name='delete_click'),  # AJAX delete
]