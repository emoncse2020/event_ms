from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .models import Event

@receiver(m2m_changed, sender=Event.participants.through)
def send_join_email(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            send_mail(
                subject="Event Registration Confirmation",
                message=f"Hi {user.first_name},\n\nYou have successfully joined the event: {instance.name} on {instance.date} at {instance.location}.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
