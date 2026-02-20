from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data.'

    def handle(self, *args, **options):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]

        # Clean up existing data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Ensure unique index on email
        db.users.create_index('email', unique=True)

        # Superhero test data
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': 'Marvel'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': 'DC'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
        ]
        db.users.insert_many(marvel_heroes + dc_heroes)

        db.teams.insert_many([
            {'name': 'Marvel', 'members': [h['username'] for h in marvel_heroes]},
            {'name': 'DC', 'members': [h['username'] for h in dc_heroes]},
        ])

        db.activities.insert_many([
            {'user': 'ironman', 'activity': 'run', 'distance': 10},
            {'user': 'batman', 'activity': 'cycle', 'distance': 15},
            {'user': 'spiderman', 'activity': 'swim', 'distance': 2},
            {'user': 'superman', 'activity': 'fly', 'distance': 100},
        ])

        db.leaderboard.insert_many([
            {'team': 'Marvel', 'points': 250},
            {'team': 'DC', 'points': 300},
        ])

        db.workouts.insert_many([
            {'user': 'ironman', 'workout': 'pushups', 'reps': 50},
            {'user': 'batman', 'workout': 'pullups', 'reps': 30},
            {'user': 'wonderwoman', 'workout': 'squats', 'reps': 40},
        ])

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with superhero test data.'))