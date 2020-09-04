import pandas as pd
import tablib
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django_tables2 import tables
from django_tables2.export import TableExport

from credits.models import ListReports
from .forms import FilterForm
from .models import Clients, Credits, Contracts
from .queries import Query
from .tables import CreditsListTable, ContractsListTable, ClientsListTable, ExportClientsTable


@login_required
def index(request):
    title = _("Clients")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    form = FilterForm(request.GET)
    if form.is_valid():
        Branch = form.cleaned_data['branch']
        ClType = form.cleaned_data['type']
        ClStat = form.cleaned_data['status']
        Search = request.GET.get('search') if 'search' in request.GET else ''
        branch_code = Branch.CODE if Branch is not None else ''

    query = Query.findClients()
    if 'sort' in request.GET:
        query += ' order by %s' % request.GET.get('sort')

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
        'client_status': client.Status
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
        "total": client.OstatokReserve + client.Reserve
    }
    return render(request, 'clients/client_detail.html', context)


def contract_detail(request, client_id, contract_id):
    title = "Договор №{}".format(contract_id)
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = Query.findContracts()
    model = Contracts.objects.raw(query, [contract_id])
    table = ContractsListTable(model)


    context = {
        "page_title": title,
        "data_table": table,
        "client_id": client_id
    }
    return render(request, 'clients/contract_detail.html', context)
