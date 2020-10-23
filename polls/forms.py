from django import forms
from address.forms import AddressField

class CommentForm(forms.Form):
    name_text = forms.CharField(label='Title', max_length=200)
    comment_text = forms.CharField(label='Comment', max_length=1000)
    address = AddressField()