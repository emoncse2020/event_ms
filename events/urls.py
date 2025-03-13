from django.urls import path
from .views import home,create_event

urlpatterns = [
    path('home/', home, name='home'),
    path('create-event/', create_event, name='create-event')
]
