import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Events


def create_event(organizer="", name="", comment="", address="", days=0):
    """
    Creates an event with the provided parameters that
    takes place `days` from now (negative for past event).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Events.objects.create(organizer=organizer,
                                 name=name,
                                 comment=comment,  # event details
                                 address=address,
                                 event_date=time.date().isoformat(),
                                 event_time=time.time().isoformat())


class EventsIndexViewTests(TestCase):
    def test_no_events(self):
        """
        If no events exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('meetup_finder:index'))  # the list of events
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No events are available.")
        self.assertQuerysetEqual(response.context['comment_list'], [])  # the list of events

    def test_single_event(self):
        """
        An added event is displayed on the events page.
        """
        create_event(organizer="Test Organizer",
                     name="Test Event Name",
                     comment="Test Event Details",  # event details
                     address="Test Address")
        response = self.client.get(reverse('meetup_finder:index'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Test Organizer")
        self.assertContains(response, "Test Event Name")
        self.assertContains(response, "Test Event Details")
        self.assertContains(response, "Test Address")

    def test_multiple_events(self):
        """
        A second added event is displayed on the events page.
        """
        create_event(organizer="Test Organizer",
                     name="Test Event Name",
                     comment="Test Event Details",  # event details
                     address="Test Address")
        create_event(organizer="Test Organizer 2",
                     name="Test Event Name 2",
                     comment="Test Event Details 2",  # event details
                     address="Test Address 2")
        response = self.client.get(reverse('meetup_finder:index'))
        # self.assertContains(response, "Test Organizer 2")
        self.assertContains(response, "Test Event Name 2")
        self.assertContains(response, "Test Event Details 2")
        self.assertContains(response, "Test Address 2")


class EventsCreateViewTests(TestCase):
    def test_event_form(self):
        """
        Check that create event form works.
        """
        response = self.client.get(reverse('meetup_finder:events'))  # the list of events
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Organizer")
        self.assertContains(response, "Event Name")
        self.assertContains(response, "Details")
        self.assertContains(response, "Address")
        self.assertContains(response, "Event date")
        self.assertContains(response, "Event time")
