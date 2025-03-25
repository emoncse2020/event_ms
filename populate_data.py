import os
import django
from faker import Faker
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from events.models import Event, Category
from django.contrib.auth.models import User

def populate_db():
    fake = Faker()

    # Create Categories
    categories = [Category.objects.create(
        name=fake.word().capitalize(),
        description=fake.paragraph()
    ) for _ in range(5)]
    print(f" Created {len(categories)} categories.")

    # Create Events
    events = [Event.objects.create(
        name=fake.sentence(nb_words=3),
        description=fake.paragraph(),
        date=fake.date_between(start_date="-1y", end_date="+1y"),
        time=fake.time(),
        location=fake.city(),
        category=random.choice(categories)
    ) for _ in range(10)]
    print(f"Created {len(events)} events.")

    # Create Users (Participants)
    users = [User.objects.create_user(
        username=fake.unique.user_name(),
        email=fake.unique.email(),
        password='testpass123'  
    ) for _ in range(20)]
    print(f" Created {len(users)} users.")


    for event in events:
        participants = random.sample(users, k=random.randint(5, 15))
        event.participants.set(participants)
    print(" Assigned users to events.")

    print("Database populated successfully!")

if __name__ == "__main__":
    populate_db()
