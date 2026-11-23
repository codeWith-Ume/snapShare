from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from moments.models import Photo


class Command(BaseCommand):
    help = "Delete photos from events older than 7 days"

    def handle(self, *args, **options):
        cutoff_date = timezone.now() - timedelta(days=7)

        old_photos = Photo.objects.filter(
            event__created_at__lte=cutoff_date,
            is_preserved=False
        )

        deleted_count = 0

        for photo in old_photos:
            photo.image.delete(save=False)
            photo.delete()
            deleted_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deleted {deleted_count} photos."
            )
        )