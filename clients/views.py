import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _

from credits.models import ListReports
from .models import Clients, Credits, Contracts
from .queries import Query
from .tables import CreditsListTable, ContractsListTable


@login_required
def index(request):
    title = _("Clients")
    context = {
        "page_title": title
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
