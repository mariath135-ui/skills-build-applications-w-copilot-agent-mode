from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the MongoDB database with initial data for Octofit Tracker.'

    def handle(self, *args, **options):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]

        # Example: Insert initial collections and documents
        db.users.insert_many([
            {'username': 'alice', 'email': 'alice@example.com', 'team': 'Team A'},
            {'username': 'bob', 'email': 'bob@example.com', 'team': 'Team B'},
        ])
        db.teams.insert_many([
            {'name': 'Team A', 'members': ['alice']},
            {'name': 'Team B', 'members': ['bob']},
        ])
        db.activities.insert_many([
            {'user': 'alice', 'activity': 'run', 'distance': 5},
            {'user': 'bob', 'activity': 'cycle', 'distance': 10},
        ])
        db.leaderboard.insert_one({'team': 'Team A', 'points': 100})
        db.workouts.insert_one({'user': 'alice', 'workout': 'pushups', 'reps': 20})

        self.stdout.write(self.style.SUCCESS('Database populated with initial data.'))