from django.db import models
from django.core.exceptions import ValidationError


def validate_csv_file(value):
    if not value.name.endswith('.csv'):
        raise ValidationError("Only CSV files are allowed.")

class CSVFile(models.Model):
    file = models.FileField(upload_to='csv_files/', validators=[validate_csv_file])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class CSVData(models.Model):
    ia_model = models.CharField(max_length=100, choices=[('model1', 'Model 1'), ('model2', 'Model 2'), ('model3', 'Model 3')])
    csv_file = models.ForeignKey(CSVFile, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"{self.ia_model} - {self.csv_file}"
