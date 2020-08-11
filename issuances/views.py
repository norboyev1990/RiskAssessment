import datetime
import pandas as pd
from django.db import connection
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Data, List

from .forms import UploadIssuancesForm

def ask_float(str):
    return float(str) if str!='' else 0
def ask_date(str):
    return str if str!='' else None

def upload(request):
    title = "Загрузить выдачи"

    # issue_instance = get_object_or_404(UploadIssuancesForm, pk=1)
    if request.method == 'POST':
        form = UploadIssuancesForm(request.POST, request.FILES)
        if form.is_valid():
            obj = List.objects.create(
                TITLE="TEST",
                ISSUE_YEAR=form.cleaned_data['IssueYear'],
                ISSUE_MONTH=form.cleaned_data['IssueMonth'],
                DATE_CREATE=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )

            data = pd.read_excel(request.FILES['IssueFile'])
            data = data.fillna('')
            data.columns = [
                'code_region', 'mfo', 'name_client', 'credit_schet', 'balans_schet',
                'code_val', 'procent_credit', 'procent_prosr', 'summa_dogovor', 'summa_fact',
                'date_vidachi', 'date_pogash', 'sel_credita', 'otrasl_clienta', 'vid_credita',
                'istochnik_credita', 'schet_korrespondent', 'mfo_korrespondent', 'name_korrespondent', 'date_pervoy_vybor']

            cursor = connection.cursor()
            cursor.execute("select NVL(max(id), 0) from issuances_data")
            max_id = cursor.fetchone()[0] + 1
            data.insert(0, 'ID', range(max_id, max_id + len(data)))


            for index, row in data.iterrows():
                Data.objects.create(
                    id=row['ID'],
                    CODE_REGION     = str(row['code_region']),
                    MFO             = str(row['mfo']),
                    NAME_CLIENT     = str(row['name_client']),
                    CREDIT_SCHET    = str(row['credit_schet']),
                    BALANS_SCHET    = str(row['balans_schet']),
                    CODE_VAL        = str(row['code_val']),
                    PROCENT_CREDIT  = ask_float(row['procent_credit']),
                    PROCENT_PROSR   = ask_float(row['procent_prosr']),
                    SUMMA_DOGOVOR   = ask_float(row['summa_dogovor']),
                    SUMMA_FACT      = ask_float(row['summa_fact']),
                    DATE_VIDACHI    = row['date_vidachi'],
                    DATE_POGASH     = row['date_pogash'],
                    SEL_CREDITA     = str(row['sel_credita']),
                    OTRASL_CLIENTA  = str(row['otrasl_clienta']),
                    VID_CREDITA     = str(row['vid_credita']),
                    ISTOCHNIK_CREDITA   = str(row['istochnik_credita']),
                    SCHET_KORRESPONDENT = str(row['schet_korrespondent']),
                    MFO_KORRESPONDENT = str(row['mfo_korrespondent']),
                    NAME_KORRESPONDENT  = str(row['name_korrespondent']),
                    DATE_PERVOY_VYBOR   = ask_date(row['date_pervoy_vybor']),
                    ISSUANCE    = obj
                )
            return HttpResponseRedirect('/issuances/success')
    else:
        current_year = datetime.date.year
        form = UploadIssuancesForm(initial={'IssueYear': current_year})

    context = {
        "page_title": title,
        "menu_block": "uploads",
        "form": form,
        # "data":data
        # "issue_instance" : issue_instance
    }
    return render(request, "issuances/upload.html", context)

def success(request):
    return render(request, 'issuances/success.html', {"page_title": "Result"})