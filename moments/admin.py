from django.contrib import admin
from .models import Event, Photo

# Register your models here.
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'uploaded_at', 'is_preserved')
    list_filter = ('is_preserved', 'event')
    list_editable = ('is_preserved',)


admin.site.register(Event)
