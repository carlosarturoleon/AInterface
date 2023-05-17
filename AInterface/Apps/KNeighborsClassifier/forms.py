from django import forms
from .models import CSVData

class CSVDataForm(forms.ModelForm):
    class Meta:
        model = CSVData
        fields = ['ia_model', 'csv_file']
