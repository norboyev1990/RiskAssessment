import json
from decimal import Decimal
import pandas as pd
from django.shortcuts import render

from analytics.models import Classification
from analytics.queries import Query
from analytics.tables import ClassificationTable, ClientsByClassTable
from clients.models import Clients
from credits.models import ListReports


def general_analytics(request):
    title = "Общая аналитика"
    context = {
        "page_title": title,
        "menu_block": "analytics"
    }
    return render(request, 'analytics/general_analytics.html', context)

def line_chart_portfolio(request):
    title = "Диаграмма КП по месяцам"
    context = {
        "page_title": title,
        "menu_block": "analytics"
    }
    return render(request, 'analytics/line_chart_portfolio.html', context)


def vector_map_portfolio(request):
    title = "Распределения КП по региноам"
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = Query.get_statuses()
    model = Classification.objects.raw(query, [report.id, report.id])
    table = ClassificationTable(model)

    dlist = []
    for p in model:
        dlist.append({
            "title":p.Title,
            "value":str(p.Balance)
        })

    query = Query.find_clients_by_status()
    model = Clients.objects.raw(query, [report.id,10])
    table2 = ClientsByClassTable(model)
    table2.paginate(page=request.GET.get('page',1),per_page=10)

    context = {
        "page_title": title,
        "data_table": table,
        "data_table2": table2,
        "data_dlist": dlist,
        "menu_group": "analytics"
    }
    return render(request, 'analytics/vector_map_portfolio.html', context)
