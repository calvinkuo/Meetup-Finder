import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Events, Response


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
                                 geolocation="0,0",
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
        self.assertQuerysetEqual(response.context['event_list'], [])  # the list of events

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
        self.assertContains(response, "Test Organizer")
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
        self.assertContains(response, "Test Organizer 2")
        self.assertContains(response, "Test Event Name 2")
        self.assertContains(response, "Test Event Details 2")
        self.assertContains(response, "Test Address 2")


def create_user_and_login(self, username, password):
    self.user = User.objects.create_user(username=username, password=password)
    self.client.login(username=username, password=password)
    return self.user


def login_and_add_event(self):
    self.user = create_user_and_login(self, 'testuser', '12345')
    response = self.client.post(reverse('meetup_finder:events'), {
        'organizer': "Test Organizer",
        'name': "Test Event Name",
        'comment': "Test Event Details",
        'address': "Test Address",
        'geolocation': "0,0",
        'event_date': "12/1/2020",
        'event_time': "1:00",
        'user': self.user
    }, follow=True)  # the list of events
    return response, Events.objects.latest('pk')


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

    def test_event_form_create(self):
        """
        Check that submitting the create event form works.
        """
        response, _ = login_and_add_event(self)
        self.assertEqual(response.status_code, 200)  # after redirect
        self.assertContains(response, "Test Organizer")
        self.assertContains(response, "Test Event Name")
        self.assertContains(response, "Test Event Details")
        self.assertContains(response, "Test Address")
        self.assertContains(response, "Dec. 1, 2020")
        # self.assertContains(response, "Event time")


class EventsDetailViewTests(TestCase):
    def test_event_details(self):
        """
        Detailed view displays correctly. Votes are initialized to 0.
        """
        _, event = login_and_add_event(self)

        response = self.client.get(reverse('meetup_finder:detail', args=[event.pk]))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Test Organizer")
        self.assertContains(response, "Test Event Name")
        self.assertContains(response, "Test Event Details")
        self.assertContains(response, "Test Address")
        self.assertContains(response, "Going -- 0 votes")
        self.assertContains(response, "Not Going -- 0 votes")
        self.assertContains(response, "Maybe -- 0 votes")
        self.assertContains(response, "Respond")
        self.assertNotContains(response, "Login to respond to event, or delete event if you are the event creator")
        self.assertContains(response, "Delete Event")  # authorized user

    def test_event_details_noauth(self):
        """
        Detailed view displays correctly for non-authorized user
        """
        _, event = login_and_add_event(self)
        self.client.logout()
        self.user = create_user_and_login(self, 'differenttestuser', '12345')

        response = self.client.get(reverse('meetup_finder:detail', args=[event.pk]))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Test Organizer")
        self.assertContains(response, "Test Event Name")
        self.assertContains(response, "Test Event Details")
        self.assertContains(response, "Test Address")
        self.assertContains(response, "Going -- 0 votes")
        self.assertContains(response, "Not Going -- 0 votes")
        self.assertContains(response, "Maybe -- 0 votes")
        self.assertContains(response, "Respond")
        self.assertNotContains(response, "Login to respond to event, or delete event if you are the event creator")
        self.assertContains(response, "Delete Event")  # not authorized user
        # self.assertNotContains(response, "Delete Event")  # not authorized user

    def test_event_details_noauth(self):
        """
        Detailed view displays correctly for logged-out user
        """
        _, event = login_and_add_event(self)
        self.client.logout()

        response = self.client.get(reverse('meetup_finder:detail', args=[event.pk]))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Test Organizer")
        self.assertContains(response, "Test Event Name")
        self.assertContains(response, "Test Event Details")
        self.assertContains(response, "Test Address")
        self.assertContains(response, "Going -- 0 votes")
        self.assertContains(response, "Not Going -- 0 votes")
        self.assertContains(response, "Maybe -- 0 votes")
        self.assertNotContains(response, "Respond")  # not authorized user
        self.assertContains(response, "Login to respond to event, or delete event if you are the event creator")
        self.assertNotContains(response, "Delete Event")  # not authorized user


class EventsResponseVoteTests(TestCase):
    def test_response_vote(self):
        """
        Check that Votes are added properly
        """
        _, event = login_and_add_event(self)
        self.user = create_user_and_login(self, 'differenttestuser', '12345')

        for r in event.response_set.all():
            self.client.post(reverse('meetup_finder:vote',
                                     args=[event.id]),
                             {'response': r.id},
                             follow=True)

        response = self.client.get(reverse('meetup_finder:detail', args=[event.pk]))
        self.assertContains(response, "Going -- 1 vote")
        self.assertContains(response, "Not Going -- 1 vote")
        self.assertContains(response, "Maybe -- 1 vote")

        for r in event.response_set.all():
            self.client.post(reverse('meetup_finder:vote',
                                     args=[event.id]),
                             {'response': r.id},
                             follow=True)

        response = self.client.get(reverse('meetup_finder:detail', args=[event.pk]))
        self.assertContains(response, "Going -- 2 votes")
        self.assertContains(response, "Not Going -- 2 votes")
        self.assertContains(response, "Maybe -- 2 votes")


class EventsResponseDeleteTests(TestCase):
    def test_delete_event_auth(self):
        """
        Check that authorized user can delete event
        """
        _, event = login_and_add_event(self)

        response = self.client.post(reverse('meetup_finder:event_delete', args=[event.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Organizer")
        self.assertNotContains(response, "Test Event Name")
        self.assertNotContains(response, "Test Event Details")
        self.assertNotContains(response, "Test Address")
        self.assertNotContains(response, "Dec. 1, 2020")

        response = self.client.get(reverse('meetup_finder:detail', args=[event.pk]))
        self.assertEqual(response.status_code, 404)
#
#
#     def test_delete_event_no_auth(self):
#         """
#         Check that non-authorized user cannot delete event
#         """
#         _, event = login_and_add_event(self)
#         self.client.logout()
#         self.user = create_user_and_login(self, 'differenttestuser', '12345')
#
#         response = self.client.get(reverse('meetup_finder:event_delete', args=[event.pk]))
#         self.assertContains(response, "You don't have access to delete this event")
