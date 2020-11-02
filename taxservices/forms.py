from django import forms
from django.core.exceptions import ValidationError


class SearchForm(forms.Form):
    tin = forms.CharField(max_length=9, required=False)
    pinfl = forms.CharField(max_length=14, required=False)
    series = forms.CharField(max_length=2, required=False)
    number = forms.IntegerField(required=False)
    type = forms.CharField(max_length=1, required=False)

    def clean(self):
        cleaned_data = super().clean()
        tin = cleaned_data.get("tin")
        pinfl = cleaned_data.get("pinfl")
        series = cleaned_data.get("series")
        number = cleaned_data.get("number")
        type = cleaned_data.get("type")

        if type == 'J' and not tin:
            msg = "Введите ИНН юридическое лицо."
            self.add_error('tin', msg)
        if type == 'P' and not (tin or pinfl or series and number):
            msg = "Введите ИНН, ПИНФЛ или серия и номер паспорта физическое лицо."
            self.add_error('tin', msg)
