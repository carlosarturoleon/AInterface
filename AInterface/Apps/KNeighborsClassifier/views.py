from django.shortcuts import render, redirect
from .forms import CSVDataForm
from .models import CSVFile
from django.views import View
from django.urls import reverse_lazy


class CsvCreateView(View):
    template_name = 'KNeighborsClassifier/create_csv_data.html'

    def get(self, request, pk=None):
        form = CSVDataForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CSVDataForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        csv_file = form.save()
        # pic.owner = self.request.user
        # csv_file.save()
        # form.save_m2m()
        return redirect('KNeighborsClassifier:csv_detail', pk=csv_file.pk)
    

class CsvDetailView(View):
    model = CSVFile
    template_name = "KNeighborsClassifier/csv_detail.html"
    def get(self, request, pk) :
        x = CSVFile.objects.get(id=pk)
        context = { 'csv_file' : x, }
        return render(request, self.template_name, context)
