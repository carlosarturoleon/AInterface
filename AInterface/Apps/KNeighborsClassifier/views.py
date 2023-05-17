from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import CSVDataForm

def create_csv_data(request):
    if request.method == 'POST':
        form = CSVDataForm(request.POST, request.FILES)
        if form.is_valid():
            csv_data = form.save()
            # Additional processing or redirection logic
            return redirect('csv_data_detail', pk=csv_data.pk)
    else:
        form = CSVDataForm()
    
    return render(request, 'KNeighborsClassifier/create_csv_data.html', {'form': form})
