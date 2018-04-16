from django import forms


class AlarmForm(forms.Form):
    label = forms.CharField(label="Alarm Name", max_length=128)
    time = forms.TimeField(label="Wake up time")
    origin = forms.CharField(label="Home Address", max_length=512)
    destination = forms.CharField(label="Destination Address", max_length=512)
