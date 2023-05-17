from django.urls import path
from .views import create_csv_data

urlpatterns = [
    # Other URL patterns
    path('csv-data/create/', create_csv_data, name='create_csv_data'),
]
