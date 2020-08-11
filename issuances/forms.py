from django import forms

class UploadIssuancesForm(forms.Form):
    IssueYear = forms.IntegerField(label="Год выдачи", min_value=2020, max_value=2030)
    IssueMonth = forms.IntegerField(label="Месяц выдачи", min_value=1,max_value=12)
    IssueFile = forms.FileField(label="Файл",)