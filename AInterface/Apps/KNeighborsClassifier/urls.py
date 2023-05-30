from django.urls import path, reverse_lazy
from . import views

app_name='KNeighborsClassifier'

urlpatterns = [
    # Other URL patterns
    path('csv-data/create/', views.CsvCreateView.as_view(), name='create_csv_data'),
    path('csv-data/<int:pk>', views.CsvDetailView.as_view(), name='csv_detail'),
    path('', views.CsvListView.as_view(), name='all'),
    path('csv/<int:pk>/delete', views.CsvDeleteView.as_view(success_url=reverse_lazy('KNeighborsClassifier:all')), name='csv_delete'),
]
