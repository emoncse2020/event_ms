from django.urls import path
from .views import user_dashboard,create_event, organizer_dashboard, view_events, update_event, delete_event, event_details, join_event, dashboard

urlpatterns = [
    path('user-dashboard/', user_dashboard, name='user-dashboard'),
    path('create-event/', create_event, name='create-event'),
    path('update-event/<int:id>/', update_event, name='update-event'),
    path('delete-event/<int:id>/', delete_event, name="delete-event"),
    path('organizer-dashboard/', organizer_dashboard, name='organizer-dashboard'),
    path('view-events/',view_events),
    path('event/<int:event_id>/details/', event_details, name="event-details"),
    path('join-event/<int:event_id>/', join_event, name='join-event'),
    path('dashboard', dashboard, name='dashboard')

]
