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
        "menu_block": 'analytics',
        "menu_group": 'bad_credits',
    }
    return render(request, 'analytics/general_analytics.html', context)

def line_chart_portfolio(request):
    title = "Диаграмма КП по месяцам"
    context = {
        "page_title": title,
        "menu_block": 'analytics',
        "menu_group": 'bad_credits',
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

    df = pd.DataFrame(dlist)
    df['value'] = df['value'].astype('float').round(1)
    df = df.sort_values(by='value', ascending=False)
    df['delta'] = df['value'] - df['value'].shift(-1)
    df['max'] = df['value'] - df['delta'] * 0.1
    df['min'] = df['value'] - df['delta'] * 0.9
    df = df.fillna(0)
    df = df.sort_values(by='delta', ascending=False)
    r = df.iloc[0]

    context = {
        "page_title": title,
        "data_table": table,
        "data_dlist": dlist,
        "menu_block": 'analytics',
        "menu_group": 'bad_credits',
        "max": r['max'],
        "min": r['min'],
        "max_value": df['value'].max() * 1.1,
    }
    return render(request, 'analytics/vector_map_portfolio.html', context)

def risk_appetita(request):
    title = "Расчет риск-аппетита в разрезе риск-компонентов"
    context = {
        "page_title": title,
        "menu_block": 'analytics',
        "menu_group": 'risk_appetita',
    }
    return render(request, 'analytics/risk_appetita.html', context)

def cascading_reserve(request):
    title = "Каскадирование дополнительных резервов на КП"
    context = {
        "page_title": title,
        "menu_block": 'analytics',
        "menu_group": 'risk_appetita',
    }