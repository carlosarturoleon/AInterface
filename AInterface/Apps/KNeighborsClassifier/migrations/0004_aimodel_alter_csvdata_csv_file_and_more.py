# Generated by Django 4.2.1 on 2023-05-18 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KNeighborsClassifier', '0003_alter_csvdata_csv_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='csvdata',
            name='csv_file',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='KNeighborsClassifier.csvfile'),
        ),
        migrations.AlterField(
            model_name='csvdata',
            name='ia_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KNeighborsClassifier.aimodel'),
        ),
    ]
