from django.shortcuts import render

# Create your views here.
def home(request):
    display_name = ""

    if request.user.is_authenticated:
        display_name = request.user.email.split('@')[0].split('.')[0].capitalize()

    return render(request, 'home/index.html', {
        'display_name': display_name
    })