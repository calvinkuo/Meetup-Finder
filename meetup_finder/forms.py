from django import forms
# from address.forms import AddressField
from django_google_maps import widgets as map_widgets
# from django_google_maps import fields as map_fields
from .models import Events, Profile, EventComment

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'
class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholder = {
            'organizer': 'Enter the group or person hosting this event',
            'name': 'Enter a title',
            'comment': 'Enter a description',
            'event_date': 'Enter a date',
            'event_time': 'Enter a time',
            'address': 'Enter a location',
            'geolocation': '',
        }
        for name, value in self.fields.items():
            value.widget.attrs['placeholder'] = placeholder[name]

    class Meta: 
        model = Events
        fields = ['organizer', 'name', 'comment', 'event_date', 'event_time', 'address', 'geolocation']
        widgets = {
            'event_date' : DateInput(),
            'event_time' : TimeInput(),
            'address': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'}),
            'geolocation': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['comment_field']


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholder = {
            'full_name': 'Your name',
            'bio': 'A short description of yourself',
            'birthday': 'Your birthday',
            'default_filter': 'Keywords to use as your default home page (separate terms with commas)',
        }
        for name, value in self.fields.items():
            value.widget.attrs['placeholder'] = placeholder[name]

    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'birthday', 'default_filter']
        widgets = {
            'birthday': DateInput(),
        }
