from django.shortcuts import render, redirect
from .forms import CSVDataForm
from .models import CSVFile
from django.views import View
from django.urls import reverse_lazy
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.backends.backend_agg as agg


class CsvCreateView(View):
    template_name = 'KNeighborsClassifier/create_csv_data.html'

    def get(self, request, pk=None):
        form = CSVDataForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CSVDataForm(request.POST, request.FILES or None)
        success_url = 'KNeighborsClassifier:csv_detail'

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        csv_file = form.save()
        return redirect(success_url, pk=csv_file.pk)
    

class CsvDetailView(View):
    model = CSVFile
    template_name = "KNeighborsClassifier/csv_detail.html"


class CsvDetailView(View):
    model = CSVFile
    template_name = "KNeighborsClassifier/csv_detail.html"

    def get(self, request, pk):
        csv_file = CSVFile.objects.get(id=pk)

        # Read the CSV data and create a plot
        data = read_csv_data(csv_file.file.path)
        x = data['x']
        y = data['y']

        # Plot creation
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Matplotlib Plot')

        # Render the plot to a canvas
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()

        # Save the plot to a temporary file within the media directory
        temp_file = os.path.join('media', 'plot.png')
        canvas.print_png(temp_file)
        # Pass the temporary file path to the template
        context = {'csv_file': csv_file, 'plot_file': temp_file}
        return render(request, self.template_name, context)


def read_csv_data(file_path):

    data = pd.read_csv(file_path)
    return {'x': data['radius_mean'], 'y': data['texture_mean']}