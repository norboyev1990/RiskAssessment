from django import forms
from credits.models import Branch

class FilterForm(forms.Form):
    CHOICES_TYPE = [
        ('','---------'),
        ('J', 'Юридические лица'),
        ('P','Физические лица'),
    ]

    CHOICES_STATUS = [
        ('','---------'),
        ('90','Стандарт'),
        ('70','Субстандарт'),
        ('50','Неудовлет.'),
        ('30','Сомнительный'),
        ('10','Безнадежный'),
    ]

    branches = Branch.objects.all()

    type = forms.ChoiceField(widget=forms.Select(attrs={'onchange': 'submit();'}), choices=CHOICES_TYPE, label="Тип клиента", required=False)
    branch = forms.ModelChoiceField(widget=forms.Select(attrs={'onchange': 'submit();'}), queryset=branches, label="Филиал", required=False)
    status = forms.ChoiceField(widget=forms.Select(attrs={'onchange': 'submit();'}), choices=CHOICES_STATUS, label="Статус", required=False)