from django import forms

from credits.models import Branch


class UploadForm(forms.Form):
    DataTitle = forms.CharField(label="Название ")
    DataYear = forms.IntegerField(label="Год ", min_value=2020, max_value=2030)
    DataMonth = forms.IntegerField(label="Месяц ", min_value=1,max_value=12)
    DataFile = forms.FileField(label="Файл",)

class UploadRepaymentForm(forms.Form):
    branches = Branch.objects.all()
    DataBranch = forms.ModelChoiceField(queryset=branches, label="Филиал")
    DataTitle = forms.CharField(label="Название ")
    DataYear = forms.IntegerField(label="Год ", min_value=2020, max_value=2030)
    DataMonth = forms.IntegerField(label="Месяц ", min_value=1,max_value=12)
    DataFile = forms.FileField(label="Файл",)