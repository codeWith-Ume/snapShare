from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from .models import Event, Photo
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
# Create your views here.
@login_required
def moments_home(request):
    events = Event.objects.order_by('-created_at')

    return render(request, 'moments/index.html', {
        'events': events
    })

@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('event_upload', event_id=event.id)

    else:
        form = EventForm()

    return render(request, 'moments/add_event.html', {'form': form})

@login_required
def event_upload(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        images = request.FILES.getlist('images')

        for image in images:
            Photo.objects.create(
                event=event,
                image=image,
                uploaded_by=request.user
            )

        return redirect('event_upload', event_id=event.id)

    photos = event.photos.all()

    return render(request, 'moments/event_upload.html', {
        'event': event,
        'photos': photos
    })

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.created_by != request.user:
        return HttpResponseForbidden("You cannot edit this event.")

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)

        if form.is_valid():
            form.save()
            return redirect('moments_home')
    else:
        form = EventForm(instance=event)

    return render(request, 'moments/edit_event.html', {
        'form': form,
        'event': event
    })


@login_required
@require_POST
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.created_by != request.user:
        return HttpResponseForbidden("You cannot delete this event.")

    event.delete()
    return redirect('moments_home')

@login_required
@require_POST
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if photo.uploaded_by != request.user:
        return HttpResponseForbidden("You cannot delete this photo.")

    event_id = photo.event.id

    photo.image.delete(save=False)
    photo.delete()

    return redirect('event_upload', event_id=event_id)