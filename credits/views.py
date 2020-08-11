import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django_tables2.export.export import TableExport
from credits.models import ListReports, NplClients, ToxicCredits, OverdueCredits, InfoCredits, ByTerms, ByRetailProduct, \
    ByPercentage, ByPercentageUL, ByAverageUl, ByAverageFl, ByOverdueBranch
from credits.tables import NplClientsTable, Query, ToxicCreditsTable, OverdueCreditsTable, InfoCreditsTable, \
    ByTermsTable, ByRetailProductTable, ByPercentageTable, ByPercentageULTable, ByAverageULTable, ByAverageFLTable, \
    ByOverdueBranchTable
from .apps import CreditsConfig
from django.utils.translation import gettext as _


@login_required
def index(request):
    context = {'user': request.user}
    return render(request, 'credits/index.html', context)


@login_required
def general_info(request):
    title = _("General info")
    month = pd.to_datetime(request.current_month)

    query = 'SELECT ROWNUM as id, T.* FROM TABLE(GET_INDS(%s)) T'
    model = InfoCredits.objects.raw(query, [month])
    table = InfoCreditsTable(model)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("general_info.{}".format(export_format))

    context = {
        "page_title": title,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name,
    }

    return render(request, 'credits/view.html', context)


@login_required
def npl_clients(request):
    title = _("NPL clients")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    top = int(request.GET.get('tp')) if request.GET.get('tp') else 9999999
    query = Query.orcl_npls()
    model = NplClients.objects.raw(query, [report.id])[:top]
    table = NplClientsTable(model)
    table.paginate(page=request.GET.get("page", 1), per_page=10)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("npl_clients.{}".format(export_format))

    context = {
        "page_title": title,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name,
    }

    return render(request, 'credits/view.html', context)


@login_required
def toxic_loans(request):
    title = _("Toxic loans")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    top = int(request.GET.get('tp')) if request.GET.get('tp') else 9999999
    query = Query.orcl_toxics()
    model = ToxicCredits.objects.raw(query, [report.id])[:top]
    table = ToxicCreditsTable(model)
    table.paginate(page=request.GET.get("page", 1), per_page=10)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("toxic_loans.{}".format(export_format))

    context = {
        "page_title": title,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name,
    }

    return render(request, 'credits/view.html', context)


@login_required
def overdue_loans(request):
    title = _("Overdue loans")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    top = int(request.GET.get('tp')) if request.GET.get('tp') else 9999999
    query = Query.orcl_overdues()
    model = OverdueCredits.objects.raw(query, [report.id])[:top]
    table = OverdueCreditsTable(model)
    table.paginate(page=request.GET.get("page", 1), per_page=10)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("overdue_loans.{}".format(export_format))

    context = {
        "page_title": title,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name,
    }

    return render(request, 'credits/view.html', context)


@login_required
def by_terms(request):
    title = _("Disaggregated by terms")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = Query.orcl_byterms()
    model = ByTerms.objects.raw(query, [report.id])
    table = ByTermsTable(model, c1_name='Сроки')


    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("report_by_terms.{}".format(export_format))

    context = {
        "page_title": title,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name,
    }

    return render(request, 'credits/view.html', context)


@login_required
def by_subjects(request):
    title = _("Disaggregated by subjects")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = Query.orcl_bysubjects()
    model = ByTerms.objects.raw(query, [report.id])
    table = ByTermsTable(model, c1_name='Субъекты')


    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("report_by_subjects.{}".format(export_format))

    context = {
        "page_title": title,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name,
    }

    return render(request, 'credits/view.html', context)


@login_required
def by_segments(request):
    title = _("Disaggregated by segments")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = Query.orcl_bysegments()
    model = ByTerms.objects.raw(query, [report.id])
    table = ByTermsTable(model, c1_name='Сегменты')

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("report_by_segments.{}".format(export_format))

    context = {
        "page_title": title,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name,
    }

    return render(request, 'credits/view.html', context)


@login_required
def by_currency(request):
    title = _("Disaggregated by currency")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = Query.orcl_bycurrency()
    model = ByTerms.objects.raw(query, [report.id])
    table = ByTermsTable(model, c1_name='Валюты')

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("report_by_currency.{}".format(export_format))

    context = {
        "page_title": title,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name
    }

    return render(request, 'credits/view.html', context)


@login_required
def by_branches(request):
    title = _("Disaggregated by branches")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = Query.orcl_bybranches()
    model = ByTerms.objects.raw(query, [report.id])
    table = ByTermsTable(model, c1_name='Филиалы')
    table.paginate(page=request.GET.get("page", 1), per_page=10)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("report_by_branches.{}".format(export_format))

    context = {
        "page_title": title,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name
    }

    return render(request, 'credits/view.html', context)


@login_required
def by_products(request):
    title = _("Disaggregated by products retail business")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = Query.orcl_byretailproduct()
    model = ByRetailProduct.objects.raw(query, [report.id])
    table = ByRetailProductTable(model)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("report_by_retail_product.{}".format(export_format))

    context = {
        "page_title": title,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name
    }

    return render(request, 'credits/view.html', context)


@login_required
def by_percents(request, sts):
    title = _("Disaggregated by percents rate ")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    if sts=='national_all':
        query = Query.orcl_bypercentage_national()
        model = ByPercentage.objects.raw(query, [report.id])
        table = ByPercentageTable(model)
        addon = _("in national currency")
    elif sts=='foreign_all':
        query = Query.orcl_bypercentage_foreign()
        model = ByPercentage.objects.raw(query, [report.id])
        table = ByPercentageTable(model)
        addon = _("in foreign currency")
    elif sts=='national_ul':
        query = Query.orcl_bypercentage_national_ul()
        model = ByPercentageUL.objects.raw(query, [report.id])
        table = ByPercentageULTable(model)
        addon = _("in national currency (J)")
    else:
        query = Query.orcl_bypercentage_foreign_ul()
        model = ByPercentageUL.objects.raw(query, [report.id])
        table = ByPercentageULTable(model)
        addon = _("in foreign currency (J)")

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("report_by_percents.{}".format(export_format))

    context = {
        "page_title": title,
        "page_addon": addon,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name,
        "menu_group": "by_percents"
    }

    return render(request, 'credits/view.html', context)


@login_required
def by_averages(request, sts):
    title = _("Disaggregated by average percents rate ")
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    if sts=='juridical':
        query = Query.orcl_byaverageweight_ul()
        model = ByAverageUl.objects.raw(query, [report.id])
        table = ByAverageULTable(model)
        addon = _("(juridical person)")
    else:
        query = Query.orcl_byaverageweight_fl()
        model = ByAverageFl.objects.raw(query, [report.id])
        table = ByAverageFLTable(model)
        addon = _("(physical person)")


    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("by_averages.{}".format(export_format))

    context = {
        "page_title": title,
        "page_addon": addon,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name,
        "menu_group": "by_averages"
    }

    return render(request, 'credits/view.html', context)


@login_required
def issued_overdues(request):
    title = _("Issued overdues by branches") #Выданные | просрочка
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = Query.orcl_byoverduebrach()
    model = ByOverdueBranch.objects.raw(query, [report.id])
    table = ByOverdueBranchTable(model)
    table.paginate(page=request.GET.get("page", 1), per_page=10)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, dataset_kwargs={"title": title})
        return exporter.response("report_issued_overdues.{}".format(export_format))

    context = {
        "page_title": title,
        "data_table": table,
        "data_month": month.strftime('%Y-%m'),
        "menu_block": CreditsConfig.name
    }

    return render(request, 'credits/view.html', context)
