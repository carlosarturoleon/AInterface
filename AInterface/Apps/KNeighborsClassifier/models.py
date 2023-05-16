from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import csv


def validate_csv_file(value):
    if not value.name.endswith('.csv'):
        raise ValidationError("Only CSV files are allowed.")


class CSVFile(models.Model):
    file = models.FileField(upload_to='csv_files/', validators=[validate_csv_file])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prediction = models.IntegerField(null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.file:
            # Read the CSV file
            csv_data = []
            with self.file.open(mode='r') as csv_file:
                reader = csv.reader(csv_file)
                csv_data = list(reader)

            # Generate fields based on header row data types
            header_row = csv_data[0]
            data_row = csv_data[1] if len(csv_data) > 1 else []
            for field_name, value in zip(header_row, data_row):
                field_type = self.get_field_type(value)
                field = field_type()
                self.add_to_class(field_name, field)

    def get_field_type(self, value):
        try:
            int(value)
            return models.IntegerField
        except ValueError:
            pass

        try:
            float(value)
            return models.FloatField
        except ValueError:
            pass

        return models.CharField(max_length=100)
    

class CSVData(models.Model):
    ia_model = models.CharField(max_length=100, choices=[('model1', 'Model 1'), ('model2', 'Model 2'), ('model3', 'Model 3')])
    csv_file = models.ForeignKey(CSVFile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.ia_model} - {self.csv_file}"