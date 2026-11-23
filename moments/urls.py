from django.urls import path
from . import views

urlpatterns = [
    path('', views.moments_home, name='moments_home'),
    path('add-event/', views.add_event, name='add_event'),
    path('event/<int:event_id>/', views.event_upload, name='event_upload'),
    path('delete-photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
]