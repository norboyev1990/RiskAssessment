from django.db import connection
from django.shortcuts import render
import pandas as pd
from django_tables2.export import TableExport

from repayment.queries import Query
from repayment.tables import ReportTopTable, AllReportTable, AllReportTable2, ReportByClientTable


class CursorByName(object):
    def __init__(self, cursor):
        self._cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()
        return {description[0]: row[col] for col, description in enumerate(self._cursor.description)}


def repayments_top(request):
    title = "Выдачи по топ 25 клиента"
    month = pd.to_datetime(request.current_month)
    cursor = connection.cursor()
    cursor.execute(Query.report_top())

    dictionary = {}
    for row in CursorByName(cursor):
        info = dictionary.get(row['UNIQUE_CODE'])
        info = row if info is None else info
        info.update({'COL%s' % row['PERIOD_2']: row['TOTAL']})
        info.update({'NAT%s' % row['PERIOD_2']: row['NATIONAL']})
        dictionary.update({row['UNIQUE_CODE']: info})

    list = []
    for row in dictionary:
        list.append(dictionary[row])

    table = ReportTopTable(list)
    table.paginate(page=request.GET.get("page", 1), per_page=10)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("repayments_top.{}".format(export_format))

    context = {
        "page_title": title,
        'data_table': table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": "repayment"
    }

    return render(request, 'repayment/view.html', context)


def repayments_all(request):
    title = "Выдачи по тип клиента"
    month = pd.to_datetime(request.current_month)
    cursor = connection.cursor()
    cursor.execute(Query.report_all())

    dictionary = {}
    for row in CursorByName(cursor):
        info = dictionary.get(row['SCHET'])
        info = row if info is None else info
        info.update({'COL%s' % row['PERIOD_1']: row['TOTAL']})
        dictionary.update({row['SCHET']: info})

    list = []
    for row in dictionary:
        list.append(dictionary[row])

    table = AllReportTable(list)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("repayments_all.{}".format(export_format))

    context = {
        "page_title": title,
        'data_table': table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": "repayment"
    }

    return render(request, 'repayment/view.html', context)


def repayments_by_subjects(request):
    title = "Выдачи по субъектам"
    month = pd.to_datetime(request.current_month)
    cursor = connection.cursor()
    cursor.execute(Query.report_by_client())

    dictionary = {}
    for row in CursorByName(cursor):
        info = dictionary.get(row['IS_FL'])
        info = row if info is None else info

        info.update({'NAT%s' % row['PERIOD_2']: row['NATION']})
        info.update({'COL%s' % row['PERIOD_2']: row['TOTAL']})
        dictionary.update({row['IS_FL']: info})

    list = []
    for row in dictionary:
        list.append(dictionary[row])

    table = ReportByClientTable(list)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("repayments_by_subjects.{}".format(export_format))

    context = {
        "page_title": title,
        'data_table': table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": "repayment"
    }

    return render(request, 'repayment/view.html', context)


def repayments_by_currency(request, crncy='000'):
    title = "Выдачи по валютам"
    month = pd.to_datetime(request.current_month)
    cursor = connection.cursor()
    cursor.execute(Query.report_by_currency(), [crncy])

    dictionary = {}
    for row in CursorByName(cursor):
        info = dictionary.get(row['SCHET'])
        info = row if info is None else info

        info.update({'COL%s' % row['PERIOD_1']: row['TOTAL']})
        dictionary.update({row['SCHET']: info})

    list = []
    for row in dictionary:
        list.append(dictionary[row])

    table = AllReportTable(list)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("repayments_by_currency.{}".format(export_format))

    context = {
        "page_title": title,
        'data_table': table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": "repayment"
    }

    return render(request, 'repayment/view.html', context)
