import datetime

from django.db import models
from django.utils import timezone
from address.models import AddressField


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Events(models.Model):
    organizer = models.CharField(max_length=200)
    name = models.CharField("Event Name", max_length=200)
    comment = models.CharField("Details", max_length=1000)
    address = AddressField(on_delete=models.CASCADE)
    event_date = models.DateField(null=True)
    event_time = models.TimeField(null=True)

    def __str__(self):
        return self.name

class Response(models.Model):
    event = models.ForeignKey(Events, on_delete = models.CASCADE)
    response_text = models.CharField(max_length=50)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return self.response_text