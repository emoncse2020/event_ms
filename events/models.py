from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=150)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='details', default=1)


    def __str__(self):
        return f'{self.name} | {self.location} | {self.category}'

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='participants')

    def __str__(self):
        return f'{self.name} | {self.name} | {self.email}'

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        trunc_des = (self.description[:20])
        return f'{self.name} | {trunc_des}'


