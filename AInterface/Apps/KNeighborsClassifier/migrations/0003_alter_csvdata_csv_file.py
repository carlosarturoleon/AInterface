# Generated by Django 4.2.1 on 2023-05-18 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KNeighborsClassifier', '0002_alter_csvdata_csv_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvdata',
            name='csv_file',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='KNeighborsClassifier.csvfile'),
        ),
    ]