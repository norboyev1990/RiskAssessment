import datetime
import pandas as pd
from django.db import connection
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from issuances.models import Data, List
from credits.models import ListReports, ReportData

from .forms import UploadIssuancesForm

def ask_float(str):
    return float(str) if str!='' else 0
def ask_date(str):
    return str if str!='' else None

def credits(request):
    title = "Загрузить кредитный портфел"

    # issue_instance = get_object_or_404(UploadIssuancesForm, pk=1)
    if request.method == 'POST':
        form = UploadIssuancesForm(request.POST, request.FILES)
        if form.is_valid():
            obj = ListReports.objects.create(
                REPORT_TITLE=form.cleaned_data['DataTitle'],
                REPORT_YEAR=form.cleaned_data['DataYear'],
                REPORT_MONTH=form.cleaned_data['DataMonth'],
                DATE_CREATED=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                START_MONTH=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            )

            data = pd.read_excel(request.FILES['DataFile'])
            data = data.fillna('')

            cursor = connection.cursor()
            cursor.execute("select nvl(max(id), 0) from credits_reportdata")
            max_id = cursor.fetchone()[0] + 1
            # data.insert(0, 'ID', range(max_id, max_id + len(data)))


            for index, row in data.iterrows():
                ReportData.objects.create(
                    NUMBERS         = int(row['number']),
                    CODE_REG        = str(row['code_reg']),
                    MFO             = str(row['mfo']),
                    RAYON_PODACHI   = str(row['rayon_podachi']),
                    NAME_CLIENT     = str(row['name_client']),
                    BALANS_SCHET    = str(row['balans_schet']),
                    CREDIT_SCHET    = str(row['credit_schet']),
                    DATE_RESHENIYA  = str(row['date_resheniya']),
                    CODE_VAL        = str(row['code_val']),
                    SUM_DOG_NOM     = ask_float(row['sum_dog_nom']),
                    SUM_DOG_EKV     = ask_float(row['sum_dog_ekv']),
                    DATE_DOGOVOR    = pd.to_datetime(ask_date(row['date_dogovor'])),
                    DATE_FACTUAL    = pd.to_datetime(ask_date(row['date_factual'])),
                    DATE_POGASH     = pd.to_datetime(ask_date(row['date_pogash'])),
                    SROK            = row['srok'],
                    DOG_NUMBER_DATE = row['dog_number_date'],
                    CREDIT_PROCENT  = ask_float(row['credit_procent']),
                    PROSR_PROCENT   = ask_float(row['prosr_procent']),
                    OSTATOK_CRED_SCHET      = ask_float(row['ostatok_cred_schet']),
                    OSTATOK_PERESM          = ask_float(row['ostatok_peresm']),
                    DATE_PRODL              = row['date_prodl'],
                    DATE_POGASH_POSLE_PRODL = pd.to_datetime(ask_date(row['date_pogash_posle_prodl'])),
                    OSTATOK_PROSR           = ask_float(row['ostatok_prosr']),
                    DATE_OBRAZ_PROS         = pd.to_datetime(ask_date(row['date_obraz_pros'])),
                    OSTATOK_SUDEB           = ask_float(row['ostatok_sudeb']),
                    DATE_SUDEB              = pd.to_datetime(ask_date(row['date_sudeb'])),
                    KOD_PRAVOXR_ORG         = row['kod_pravoxr_org'],
                    PRIZNAK_RESHENIYA       = row['priznak_resheniya'],
                    DATE_PRED_RESH          = row['date_pred_resh'],
                    VSEGO_ZADOLJENNOST      = ask_float(row['vsego_zadoljennost']),
                    CLASS_KACHESTVA         = row['class_kachestva'],
                    OSTATOK_REZERV          = ask_float(row['ostatok_rezerv']),
                    OSTATOK_NACH_PRCNT      = ask_float(row['ostatok_nach_prcnt']),
                    OSTATOK_NACH_PROSR_PRCNT= ask_float(row['ostatok_nach_prosr_prcnt']),
                    OCENKA_OBESPECHENIYA    = ask_float(row['ocenka_obespecheniya']),
                    OBESPECHENIE            = row['obespechenie'],
                    OPISANIE_OBESPECHENIE   = row['opisanie_obespechenie'],
                    ISTOCHNIK_SREDTSVO      = row['istochnik_sredtsvo'],
                    ZARUBEJNIY_BANK         = row['zarubejniy_bank'],
                    VID_KREDITOVANIYA       = row['vid_kreditovaniya'],
                    PURPOSE_CREDIT          = row['purpose_credit'],
                    VISHEST_ORG_CLIENT      = row['vishest_org_client'],
                    OTRASL_KREDITOVANIYA    = row['otrasl_kreditovaniya'],
                    OTRASL_CLIENTA          = row['otrasl_clienta'],
                    CLASS_KREDIT_SPOS       = row['class_kredit_spos'],
                    PREDSEDATEL_KB          = row['predsedatel_kb'],
                    ADRESS_CLIENT           = row['adress_client'],
                    UN_NUMBER_CONTRACT      = row['un_number_contract'],
                    INN_PASSPORT            = row['inn_passport'],
                    OSTATOK_VNEB_PROSR      = ask_float(row['ostatok_vneb_prosr']),
                    KONKR_NAZN_CREDIT       = row['konkr_nazn_credit'],
                    BORROWER_TYPE           = row['borrower_type'],
                    SVYAZANNIY              = int(row['svyazanniy']),
                    MALIY_BIZNES            = int(row['maliy_biznes']),
                    REGISTER_NUMBER         = row['register_number'],
                    OKED                    = row['oked'],
                    CODE_CONTRACT           = row['code_dogovor'],
                    REPORT                  = obj
                )
            return HttpResponseRedirect('/issuances/success')
    else:
        current_year = datetime.date.year
        form = UploadIssuancesForm(initial={'IssueYear': current_year})

    context = {
        "page_title": title,
        "menu_block": "uploads",
        "form": form,
    }
    return render(request, "uploads/upload.html", context)

def issuances(request):
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
    return render(request, "uploads/upload.html", context)

def success(request):
    return render(request, 'uploads/success.html', {"page_title": "Result"})