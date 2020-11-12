import datetime

from django.db import models
from django.utils import timezone
# from address.models import AddressField
from django_google_maps import fields as map_fields
from django.conf import settings


# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#     def __str__(self):
#         return self.question_text
#
#     def was_published_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date <= now
#     was_published_recently.admin_order_field = 'pub_date'
#     was_published_recently.boolean = True
#     was_published_recently.short_description = 'Published recently?'
#
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.choice_text


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


class Response(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.response_text
