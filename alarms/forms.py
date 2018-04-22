from django import forms


class AlarmForm(forms.Form):
    label = forms.CharField(label="Alarm Name", max_length=128)
    time = forms.TimeField(label="Wake up time")
    origin = forms.CharField(label="Home Address", max_length=512)
    destination = forms.CharField(label="Destination Address", max_length=512)
    sunRepeat = forms.BooleanField(label="Sunday", widget=forms.CheckboxInput(), required=False)
    monRepeat = forms.BooleanField(label="Monday", widget=forms.CheckboxInput(), required=False)
    tueRepeat = forms.BooleanField(label="Tuesday", widget=forms.CheckboxInput(), required=False)
    wedRepeat = forms.BooleanField(label="Wednesday", widget=forms.CheckboxInput(), required=False)
    thuRepeat = forms.BooleanField(label="Thursday", widget=forms.CheckboxInput(), required=False)
    friRepeat = forms.BooleanField(label="Friday", widget=forms.CheckboxInput(), required=False)
    satRepeat = forms.BooleanField(label="Saturday", initial="False", required=False)


