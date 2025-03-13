from django.shortcuts import render, redirect 
from .forms import EventModelForm

# Create your views here.

def home(request):
    return render(request, 'events/home.html')

def create_event(request):

    form = EventModelForm()
    if request.method == "POST":
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect ('home')

    context = {
        "form": form
    }

    return render(request, 'create-event.html', context)