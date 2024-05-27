# main/forms.py

from django import forms
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']

class SymptomForm(forms.Form):
    incubation = forms.IntegerField(min_value=0, max_value=20, initial=10)
    sorethroat = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')])
    temperature = forms.FloatField(min_value=30.0, max_value=45.0, initial=36.5)
