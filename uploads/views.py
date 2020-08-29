from datetime import datetime
import pandas as pd
from django.db import connection
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from issuances.models import Data, List
from credits.models import ListReports, ReportData, OverduePercents, Payments
from .forms import UploadForm, UploadRepaymentForm


def credits(request):
    title = "Загрузить кредитный портфел"

    if request.method == 'POST':

        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            modelList = ListReports.objects.filter(
                REPORT_YEAR=form.cleaned_data['DataYear'],
                REPORT_MONTH=form.cleaned_data['DataMonth']
            ).first()

            if modelList is None:
                modelList = ListReports.objects.create(
                    REPORT_TITLE=form.cleaned_data['DataTitle'],
                    REPORT_YEAR=form.cleaned_data['DataYear'],
                    REPORT_MONTH=form.cleaned_data['DataMonth'],
                    DATE_CREATED=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    START_MONTH=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                )
            else:
                ReportData.objects.filter(REPORT_id=modelList.id).delete()

            dtypes = {
                'MFO': 'str', 'CODE_REG': 'str', 'BALANS_SCHET': 'str',
                'CODE_VAL': 'str', 'INN_PASSPORT': 'str'
            }
            data = pd.read_excel(request.FILES['DataFile'], dtype=dtypes)
            data.replace({pd.np.nan: None}, inplace=True)
            data.insert(0, 'REPORT', modelList)

            for index, row in data.iterrows():
                dateProdl = row['DATE_POGASH_POSLE_PRODL']
                if dateProdl is not None:
                    row['DATE_POGASH_POSLE_PRODL'] = datetime.strptime(dateProdl, "%d.%m.%Y").date()
                ReportData.objects.create(**row)
            return HttpResponseRedirect('/uploads/success/')
    else:
        cur_date = datetime.now()
        form = UploadForm(initial={
            'DataTitle': cur_date.strftime('%B, %Y'),
            'DataYear': cur_date.year,
            'DataMonth': cur_date.month
        })

    context = {
        "page_title": title,
        "menu_block": "uploads",
        "form": form
    }
    return render(request, "uploads/upload.html", context)


def repayment(request):
    title = "Загрузить пред. платежи"

    if request.method == 'POST':

        form = UploadRepaymentForm(request.POST, request.FILES)
        if form.is_valid():
            Branch = form.cleaned_data['DataBranch']
            modelList = ListReports.objects.filter(
                REPORT_YEAR=form.cleaned_data['DataYear'],
                REPORT_MONTH=form.cleaned_data['DataMonth']
            ).first()

            if modelList is None:
                modelList = ListReports.objects.create(
                    REPORT_TITLE=form.cleaned_data['DataTitle'],
                    REPORT_YEAR=form.cleaned_data['DataYear'],
                    REPORT_MONTH=form.cleaned_data['DataMonth'],
                    DATE_CREATED=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    START_MONTH=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                )
            else:
                Payments.objects.filter(REPORT=modelList, BRANCH=Branch).delete()

            data = pd.read_excel(request.FILES['DataFile'], dtype={'CODE_REG': 'str', 'MFO': 'str', 'CODE_VAL': 'str'})
            data.replace({pd.np.nan: None}, inplace=True)
            data.insert(0, 'REPORT', modelList)
            data.insert(0, 'BRANCH', Branch)

            for index, row in data.iterrows():
                Payments.objects.create(**row)
            return HttpResponseRedirect('/uploads/success/')
    else:
        cur_date = datetime.now()
        form = UploadRepaymentForm(initial={
            'DataTitle': cur_date.strftime('%B, %Y'),
            'DataYear': cur_date.year,
            'DataMonth': cur_date.month
        })

    context = {
        "page_title": title,
        "menu_block": "uploads",
        "form": form
    }
    return render(request, "uploads/upload.html", context)


def issuances(request):

    title = "Загрузить выдачи"

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            modelList = List.objects.filter(
                ISSUE_YEAR=form.cleaned_data['DataYear'],
                ISSUE_MONTH=form.cleaned_data['DataMonth']
            ).first()

            if modelList is None:
                modelList = List.objects.create(
                    TITLE=form.cleaned_data['DataTitle'],
                    ISSUE_YEAR=form.cleaned_data['DataYear'],
                    ISSUE_MONTH=form.cleaned_data['DataMonth'],
                    DATE_CREATE=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
            else:
                Data.objects.filter(ISSUANCE=modelList).delete()

            dtypes = {
                'MFO': 'str', 'CODE_REGION': 'str',
                'BALANS_SCHET': 'str', 'CODE_VAL': 'str'
            }
            data = pd.read_excel(request.FILES['DataFile'], dtype=dtypes)
            data.replace({pd.np.nan: None}, inplace=True)
            data.insert(0, 'ISSUANCE', modelList)

            for index, row in data.iterrows():
                Data.objects.create(**row)
            return HttpResponseRedirect('/uploads/success/')
    else:
        cur_date = datetime.now()
        form = UploadForm(initial={
            'DataTitle': cur_date.strftime('%B, %Y'),
            'DataYear': cur_date.year,
            'DataMonth': cur_date.month
        })

    context = {
        "page_title": title,
        "menu_block": "uploads",
        "form": form
    }
    return render(request, "uploads/upload.html", context)


def overdues(request):
    title = "Загрузить просрочки"

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            DataYear = form.cleaned_data['DataYear']
            DataMonth = form.cleaned_data['DataMonth']

            Report = ListReports.objects.filter(REPORT_MONTH=DataMonth, REPORT_YEAR=DataYear).first()

            if Report is not None:
                data = pd.read_excel(request.FILES['DataFile'])
                data = data.fillna('')

                for index, row in data.iterrows():
                    OverduePercents.objects.create(
                        # id=row['ID'],
                        FilialCode=row['FILIAL_CODE'],
                        LoanID=row['LOAN_ID'],
                        AccountCode=row['ACCOUNT_CODE'],
                        SaldoOut=row['SALDO_OUT'],
                        ArrearDate=row['ARREAR_DATE'],
                        DayCount=row['DAY_COUNT'],
                        REPORT=Report
                    )
                return HttpResponseRedirect('/issuances/success')
            else:
                form.add_error('DataMonth', 'Нет кредитный портфель для выбранного месяца!')
    else:
        cur_date = datetime.now()
        form = UploadForm(initial={
            'DataTitle': cur_date.strftime('%B, %Y'),
            'DataYear': cur_date.year,
            'DataMonth': cur_date.month
        })

    context = {
        "page_title": title,
        "menu_block": "uploads",
        "form": form,
    }
    return render(request, "uploads/upload.html", context)


def success(request):
    return render(request, 'uploads/success.html', {"page_title": "Result"})
