from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        trunc_des = (self.description[:20])
        return f'{self.name} | {trunc_des}'


class Event(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=150)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='details', default=1)

    participants = models.ManyToManyField(User, related_name='events_participated')


    def __str__(self):
        return f'{self.name} | {self.location} | {self.category}'
