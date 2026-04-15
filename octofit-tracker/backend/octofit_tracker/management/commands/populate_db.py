from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from octofit_tracker.models import Team, Activity, Workout
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Clear data
        Activity.objects.exclude(pk=None).delete()
        Workout.objects.exclude(pk=None).delete()
        User.objects.exclude(pk=None).delete()
        Team.objects.exclude(pk=None).delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users
        tony = User.objects.create_user(username='ironman', email='tony@marvel.com', password='pass', first_name='Tony', last_name='Stark')
        steve = User.objects.create_user(username='cap', email='steve@marvel.com', password='pass', first_name='Steve', last_name='Rogers')
        bruce = User.objects.create_user(username='hulk', email='bruce@marvel.com', password='pass', first_name='Bruce', last_name='Banner')
        clark = User.objects.create_user(username='superman', email='clark@dc.com', password='pass', first_name='Clark', last_name='Kent')
        bruce_dc = User.objects.create_user(username='batman', email='bruce@dc.com', password='pass', first_name='Bruce', last_name='Wayne')
        diana = User.objects.create_user(username='wonderwoman', email='diana@dc.com', password='pass', first_name='Diana', last_name='Prince')

        # Add users to teams
        try:
            marvel.members.add(tony)
            marvel.members.add(steve)
            marvel.members.add(bruce)
            dc.members.add(clark)
            dc.members.add(bruce_dc)
            dc.members.add(diana)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error adding members to teams: {e}"))

        # Create Activities
        Activity.objects.create(user=tony, activity_type='Run', duration=30, calories_burned=300, date=date(2024, 1, 1), team=marvel)
        Activity.objects.create(user=steve, activity_type='Swim', duration=45, calories_burned=400, date=date(2024, 1, 2), team=marvel)
        Activity.objects.create(user=bruce, activity_type='Lift', duration=60, calories_burned=500, date=date(2024, 1, 3), team=marvel)
        Activity.objects.create(user=clark, activity_type='Fly', duration=50, calories_burned=600, date=date(2024, 1, 4), team=dc)
        Activity.objects.create(user=bruce_dc, activity_type='Martial Arts', duration=40, calories_burned=350, date=date(2024, 1, 5), team=dc)
        Activity.objects.create(user=diana, activity_type='Run', duration=35, calories_burned=320, date=date(2024, 1, 6), team=dc)

        # Create Workouts
        w1 = Workout.objects.create(name='Super Strength', description='Heavy lifting and power moves', difficulty='Hard')
        w2 = Workout.objects.create(name='Flight Training', description='Aerobic and flying drills', difficulty='Medium')
        w3 = Workout.objects.create(name='Shield Practice', description='Agility and shield handling', difficulty='Easy')
        w1.suggested_for.set([bruce, clark])
        w2.suggested_for.set([tony, diana])
        w3.suggested_for.set([steve, bruce_dc])

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
