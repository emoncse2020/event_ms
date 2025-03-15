from django.urls import path
from .views import home,create_event, organizer_dashboard, view_events, update_event, delete_event

urlpatterns = [
    path('', home, name='home'),
    path('create-event/', create_event, name='create-event'),
    path('update-event/<int:id>/', update_event, name='update-event'),
    path('delete-event/<int:id>/', delete_event, name="delete-event"),
    path('organizer-dashboard/', organizer_dashboard, name='organizer-dashboard'),
    path('view-events/',view_events),
]
