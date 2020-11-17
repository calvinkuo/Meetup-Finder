import datetime

from django.db import models
from django.utils import timezone
# from address.models import AddressField
from django_google_maps import fields as map_fields
from django.conf import settings
from django.contrib.auth.models import User


class Events(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True)
    organizer = models.CharField(max_length=200)
    name = models.CharField("Event Name", max_length=200)
    comment = models.CharField("Details", max_length=1000)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(null=True, max_length=100)
    event_date = models.DateField(null=True)
    event_time = models.TimeField(null=True)

    class Meta:
        verbose_name_plural = "Events"
        permissions = (
            ('can_delete', 'Can delete event'),
        )

    def __str__(self):
        return self.name

    def is_past(self):
        event_datetime = datetime.datetime(self.event_date.year,
                                           self.event_date.month,
                                           self.event_date.day,
                                           self.event_time.hour,
                                           self.event_time.minute,
                                           self.event_time.second,
                                           self.event_time.microsecond,
                                           timezone.now().tzinfo)
        return event_datetime < timezone.now()


class EventComment(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    comment_field = models.CharField(max_length=500)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.comment_field


class Response(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.response_text


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField("First and Last Name", max_length=200)
    bio = models.CharField("Bio", max_length=500, blank=True)
    birthday = models.DateField("Birthday", null=True, blank=True)
    default_filter = models.CharField("Default Search Filter", max_length=500, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_name(self):
        return self.full_name if self.full_name else self.user.username
