from django import forms
from .models import ReadersSignals


class SignalForm(forms.ModelForm):
    class Meta:
        model = ReadersSignals
        fields = ['first_name', 'last_name', 'email', 'body']