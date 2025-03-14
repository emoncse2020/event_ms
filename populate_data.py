import os
import django
from faker import Faker
import random
from events.models import Event, Participant, Category  

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') 
django.setup()

# Function to populate the database
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
    print(f" Created {len(events)} events.")

    # Create Participants
    participants = [Participant.objects.create(
        name=fake.name(),
        email=fake.unique.email(),
        event=random.choice(events)
    ) for _ in range(20)]
    print(f" Created {len(participants)} participants.")

    print(" Database populated successfully!")

if __name__ == "__main__":
    populate_db()
