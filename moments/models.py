from django.db import models
from django.conf import settings

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_events'
    )

    def __str__(self):
        return self.name

class Photo(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    image = models.ImageField(upload_to='event_photos/')
    is_preserved = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.name} - Photo {self.id}"