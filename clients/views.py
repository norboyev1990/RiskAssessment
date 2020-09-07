import pandas as pd
import tablib
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.cache import cache_page
from django_tables2 import tables
from django_tables2.export import TableExport

from credits.models import ListReports, ReportData
from .forms import FilterForm
from .models import Clients, Credits, Payments
from .queries import Query
from .tables import CreditsListTable, ContractsListTable, ClientsListTable, ExportClientsTable


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


@login_required
@cache_page(60 * 60 * 24)
def index(request):
    title = _("Clients")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    # if 'type' in request.GET:
    form = FilterForm(request.GET)
    if form.is_valid():
        Branch = form.cleaned_data['branch']
        ClType = form.cleaned_data['type']
        ClStat = form.cleaned_data['status']
        Search = request.GET.get('search') if 'search' in request.GET else ''
        branch_code = Branch.CODE if Branch is not None else ''
    # else:
    #     form = FilterForm(initial={
    #         'type': 'J'
    #     })
    #     ClType = 'J'
    #     ClStat = ''
    #     Search = ''
    #     branch_code = ''


    query = Query.findClients()
    if 'sort' in request.GET:
        query += ' order by -%s' % request.GET.get('sort')

    model = Clients.objects.raw(query, [report.id,
        '%'+branch_code+'%',
        '%'+ClType+'%',
        '%'+ClStat+'%',
        '%'+Search+'%',
        '%'+Search+'%'
    ])

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exp_table = ExportClientsTable(model)
        exporter = TableExport(export_format, exp_table, dataset_kwargs={"title": title})
        return exporter.response("clients.{}".format(export_format))

    table = ClientsListTable(model)
    # table.order_by = request.GET.get('sort')
    table.paginate(page=request.GET.get("page", 1), per_page=10)



    context = {
        "page_title": title,
        "data_table": table,
        "filtr_form": form
    }
    return render(request, 'clients/index.html', context)


@login_required
@cache_page(60 * 60 * 24)
def client_detail(request, client_id):
    title = _("Профиль клиента")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    param = {
        'report_id': report.id,
        'unique_code': client_id,
    }

    # get client details
    query = Query.findClientByID()
    client = Clients.objects.raw(query, param)[0]
    # get all credits for client
    param = {
        'report_id': report.id,
        'unique_code': client_id,
        'client_status': client.ClientStatus
    }
    query = Query.findCredits()
    credits = Credits.objects.raw(query, param)
    table = CreditsListTable(credits)


    status_client = 0
    for p in credits:
        if (p.DaysOverdue > 90 or p.DaysOverduePercent > 90
                or p.SummaSudeb > 0 or p.SummaVneb > 0):
            status_client = 1
        elif (p.DaysOverdue <= 90 and p.DaysOverduePercent <= 90
              and p.SummaSudeb == 0 and p.SummaVneb == 0
              and p.SummaPeresm > 0):
            status_client = 2

    context = {
        "page_title": client.ClientName,
        "client": client,
        "status_client": status_client,
        "credits_table": table,
        "total": client.TotalReserve + client.NeededReserve
    }
    return render(request, 'clients/client_detail.html', context)


@login_required
@cache_page(60 * 60 * 24)
def contract_detail(request, client_id, contract_id):
    title = "Договор №{}".format(contract_id)
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    # get contract
    query = Query.fetch_contract_by_code()
    cursor = connection.cursor()
    cursor.execute(query, [report.id, contract_id])
    contract = dictfetchall(cursor)[0]

    # get payment list
    query = Query.findPayments()
    model = Payments.objects.raw(query, [contract_id])
    table = ContractsListTable(model)

    percent = (contract['SUM_DOG_EKV'] - contract['VSEGO_ZADOLJENNOST'])*100/contract['SUM_DOG_EKV']


    context = {
        "page_title": title,
        "contract": contract,
        "data_table": table,
        "client_id": client_id,
        "c_percent": percent
    }
    return render(request, 'clients/contract_detail.html', context)
