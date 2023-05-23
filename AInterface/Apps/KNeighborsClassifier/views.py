from django.shortcuts import render, redirect
from .forms import CSVDataForm
from .models import CSVFile
from django.views import View
from django.urls import reverse_lazy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, tempfile
import matplotlib.backends.backend_agg as agg
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


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
        data = pd.read_csv(csv_file.file.path)
        headers = data.columns.tolist()


        # AI Processing
        data['target'] = data['diagnosis'].map({'M': 0, 'B': 1})
        data = data.drop(['diagnosis', 'Unnamed: 32'], axis=1)
        X = data[data.columns[:-1]]
        y = data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
        neigh  = KNeighborsClassifier(n_neighbors=1)
        knn = neigh.fit(X_train, y_train)

        # Find the training and testing accuracies by target value (i.e. malignant, benign)
        mal_train_X = X_train[y_train==0]
        mal_train_y = y_train[y_train==0]
        ben_train_X = X_train[y_train==1]
        ben_train_y = y_train[y_train==1]
        
        mal_test_X = X_test[y_test==0]
        mal_test_y = y_test[y_test==0]
        ben_test_X = X_test[y_test==1]
        ben_test_y = y_test[y_test==1]

        scores = [knn.score(mal_train_X, mal_train_y), knn.score(ben_train_X, ben_train_y), 
              knn.score(mal_test_X, mal_test_y), knn.score(ben_test_X, ben_test_y)]
        
        fig2 = plt.figure()

        # Plot the scores as a bar chart
        bars = plt.bar(np.arange(4), scores, color=['#4c72b0','#4c72b0','#55a868','#55a868'])

        # directly label the score onto the bars
        for bar in bars:
            height = bar.get_height()
            fig2.gca().text(bar.get_x() + bar.get_width()/2, height*.90, '{0:.{1}f}'.format(height, 2), 
                        ha='center', color='w', fontsize=11)

        # remove all the ticks (both axes), and tick labels on the Y axis
        plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='on')
        
        # remove the frame of the chart
        for spine in fig2.gca().spines.values():
            spine.set_visible(False)
        
        plt.xticks([0,1,2,3], ['Malignant\nTraining', 'Benign\nTraining', 'Malignant\nTest', 'Benign\nTest'], alpha=0.8);
        plt.title('Training and Test Accuracies for Malignant and Benign Cells', alpha=0.8)

  
        # Transform pandas dataframe to HTML
        html_table = data.to_html()
        

        # Plot creation
        x = data['radius_mean']
        y = data['texture_mean']
        fig, ax = plt.subplots()
        ax.scatter(x, y)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Matplotlib Scatter Plot')

        # Render the plot to a canvas
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()

        # Save the plot to a temporary file within the media directory
        temp_file = os.path.join('media', 'plot.png')
        canvas.print_png(temp_file)
        temp_file2 = os.path.join('media', 'bars.png')
        canvas2 = agg.FigureCanvasAgg(fig2)
        canvas2.draw()
        canvas2.print_png(temp_file2)
        # Pass the temporary file path to the template
        context = {'csv_file': csv_file, 'plot_file': temp_file, 'bars_graph': temp_file2, 'headers': headers, 'html_table': html_table}
        return render(request, self.template_name, context)
