from django.shortcuts import render, redirect 
from .forms import EventModelForm, ParticipantModelForm
from .models import Event, Participant,Category
from django.db.models import Count, Q
from django.utils.timezone import now

# Create your views here.

def home(request):
    return render(request, 'events/home.html')

def create_event(request):

    event_form = EventModelForm()
    event_participant_form = ParticipantModelForm()

    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        event_participant_form = ParticipantModelForm(request.POST)
        if event_form.is_valid() and event_participant_form.is_valid():
            
            
            event = event_form.save()
            participant = event_participant_form.save(commit=False)
            participant.event = event
            participant.save()



            return redirect ('home')

    context = {
        "event_form": event_form,
        "event_participant_form":event_participant_form
    }

    return render(request, 'create-event.html', context)

def organizer_dashboard(request):
    today = now().date()
    
    type = request.GET.get('type', 'all')
    counts = Event.objects.aggregate(
        total_event = Count('id'),
        upcoming_event = Count('id', filter=Q(date__gte=today)),
        past_event = Count('id', filter=Q(date__lt=today))

        )
    total_participant = Participant.objects.count()
    # events = Event.objects.select_related('category').prefetch_related('events').all()
    base_query = Event.objects.select_related('category').prefetch_related('events')

    if type == "total-events":
        events = base_query.all()


    elif type == 'upcoming-events':
        events = base_query.filter(date__gte=today)

    elif type =="past-events":
        events = base_query.filter(date__lt=today)
    else:
        events = base_query.all()

    today_events = base_query.filter(date=today)



    context = {
        "today_events":today_events,
        "events":events,
        "counts": counts,
        "total_participant": total_participant
    }
    return render(request, 'dashboard/organizer-dashboard.html', context )

def view_events(request):

    events = Event.objects.select_related('category').prefetch_related('events').all()
    total_participant = Participant.objects.count()

    context = {
        "events":events,
        "pars":total_participant
    }
    return render(request, 'dashboard/view_events.html', context)