from django import forms
from address.forms import AddressField
from .models import Events
class EventForm(forms.ModelForm):
    class Meta: 
        model = Events
        fields = ['organizer', 'name', 'comment', 'address', 'event_date', 'event_time']
        # organizer = forms.CharField(label='Organizer', max_length= 50)
        # name_text = forms.CharField(label='Event Name', max_length=200)
        # comment_text = forms.CharField(label='Description', max_length=1000)
        # address = AddressField()
        # event_date = forms.DateField(label= 'Date of Event', widget = forms.SelectDateWidget)
        # event_time = forms.TimeField(label= 'Event Time')