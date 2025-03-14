from django.urls import path
from .views import home,create_event, organizer_dashboard, view_events

urlpatterns = [
    path('home/', home, name='home'),
    path('create-event/', create_event, name='create-event'),
    path('organizer-dashboard/', organizer_dashboard, name='organizer-dashboard'),
    path('view-events/',view_events),
]
