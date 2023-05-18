from django import forms
from .models import CSVFile

class CSVDataForm(forms.ModelForm):

    class Meta:
        model = CSVFile
        fields = ['file']
