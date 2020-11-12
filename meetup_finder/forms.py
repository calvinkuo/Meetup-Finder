from django import forms
# from address.forms import AddressField
from django_google_maps import widgets as map_widgets
# from django_google_maps import fields as map_fields
from .models import Events


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
            'address': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'}),
            'geolocation': forms.HiddenInput(),
        }
        # organizer = forms.CharField(label='Organizer', max_length= 50)
        # name_text = forms.CharField(label='Event Name', max_length=200)
        # comment_text = forms.CharField(label='Description', max_length=1000)
        # address = AddressField()
        # event_date = forms.DateField(label= 'Date of Event', widget = forms.SelectDateWidget)
        # event_time = forms.TimeField(label= 'Event Time')
