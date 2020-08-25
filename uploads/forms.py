from django import forms

class UploadIssuancesForm(forms.Form):
    DataTitle = forms.CharField(label="Название ")
    DataYear = forms.IntegerField(label="Год ", min_value=2020, max_value=2030)
    DataMonth = forms.IntegerField(label="Месяц ", min_value=1,max_value=12)
    DataFile = forms.FileField(label="Файл",)