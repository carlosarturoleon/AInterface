from django.urls import path
from . import views

app_name='KNeighborsClassifier'

urlpatterns = [
    # Other URL patterns
    path('csv-data/create/', views.CsvCreateView.as_view(), name='create_csv_data'),
    path('csv-data/<int:pk>', views.CsvDetailView.as_view(), name='csv_detail'),
]
