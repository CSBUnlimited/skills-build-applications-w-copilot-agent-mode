from djongo import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    # Remove team FK from User, use M2M in Team

# Team model
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Activity model
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    calories_burned = models.PositiveIntegerField()
    date = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"

# Workout model
class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    suggested_for = models.ManyToManyField(User, related_name='suggested_workouts', blank=True)

    def __str__(self):
        return self.name
    suggested_for = models.ForeignKey(Team, on_delete=models.CASCADE)

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
