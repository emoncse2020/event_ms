from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventModelForm
from .models import Event,Category
from django.db.models import Count, Q
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib import messages
from users.views import is_admin

from django.contrib.auth.decorators import user_passes_test, login_required

# Create your views here.

def is_organizer(user):
    return user.groups.filter(name = "Organizer").exists()

def is_user(user):
    return user.groups.filter (name = "User").exists()

def user_dashboard(request):
    today = now().date()

    up_events = Event.objects.select_related('category').prefetch_related('participants').filter(date__gte=today)

    context = {
        "up_events":up_events,
    }

    return render(request, 'events/user_dashboard.html', context)

@login_required
@user_passes_test(is_organizer, login_url='no-permission')
def create_event(request):

    event_form = EventModelForm(prefix='event')
    

    if request.method == "POST":
        event_form = EventModelForm(request.POST,request.FILES, prefix='event')
        if event_form.is_valid():
            
            event_form.save()
            

            return redirect ('home')

    context = {
        "event_form": event_form
    }

    return render(request, 'create-event.html', context)


@user_passes_test(is_organizer, login_url='no-permission')
def update_event(request, id):
    event = get_object_or_404(Event, id=id)
    event_form = EventModelForm(instance=event, prefix='event')


    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event, prefix='event')
        
        if event_form.is_valid():

            event_form.save()
            return redirect ('home')

    context = {
        "event_form": event_form,
    }

    return render(request, 'create-event.html', context)


@user_passes_test(is_organizer, login_url='no-permission')
def delete_event(request, id):
    event = get_object_or_404(Event, id= id)
    if request.method == "POST":
        event.delete()
        return redirect('home')
    
    

@user_passes_test(is_organizer, login_url='no-permission')
def organizer_dashboard(request):
    today = now().date()
    
    type = request.GET.get('type', 'all')
    counts = Event.objects.aggregate(
        total_event = Count('id'),
        upcoming_event = Count('id', filter=Q(date__gte=today)),
        past_event = Count('id', filter=Q(date__lt=today))

        )
    total_participant = User.objects.count()
    base_query = Event.objects.select_related('category').prefetch_related('participants')

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

@login_required
@user_passes_test(is_organizer, login_url='no-permission')
def view_events(request):

    events = Event.objects.select_related('category').prefetch_related('participants').all()
    total_participant = Participant.objects.count()

    context = {
        "events":events,
        "pars":total_participant
    }
    return render(request, 'dashboard/view_events.html', context)

@login_required
@user_passes_test(is_organizer, login_url='no-permission')
def event_details(request, event_id):
    event = Event.objects.get(id = event_id)
    return render(request, 'event_details.html', {"event":event})

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.participants.all():
        messages.info(request, "You already joined this event.")
    else:
        event.participants.add(request.user)
        messages.success(request, f"You've joined {event.name}. Confirmation email sent.")

    return redirect('user-dashboard')


@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_user(request.user):
        return redirect('user-dashboard')
    
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    
    return redirect('no-permission')
    