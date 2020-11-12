from django.apps import AppConfig


class MeetupFinderConfig(AppConfig):
    name = 'meetup_finder'
    def ready(self):
        import meetup_finder.signals  