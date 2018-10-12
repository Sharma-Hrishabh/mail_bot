from django import forms
from . import models


class CreateContacts(forms.ModelForm):
    class Meta:
        model = models.Contacts
        fields = ['name','email']
