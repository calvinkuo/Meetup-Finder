from django import forms
from address.forms import AddressField
class CommentForm(forms.Form):
    organizer = forms.CharField(label='Organizer', max_length= 50)
    name_text = forms.CharField(label='Event Name', max_length=200)
    comment_text = forms.CharField(label='Description', max_length=1000)
    address = AddressField()
    event_date = forms.DateField(label= 'Date of Event', widget = forms.SelectDateWidget)
    event_time = forms.TimeField(label= 'Event Time')