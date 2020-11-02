from django.utils.html import escape

import django_tables2 as tables
from django.utils.safestring import mark_safe

from .models import *


attrs_title = {
    "td": {"class": "text-truncate"}}

attrs_left_title = {
    "td": {"class": "text-left", "style":"min-width: 400px;"}}

attrs_text_center = {
    "th": {"class": "text-center"},
    "td": {"class": "text-center"},
    "tf": {"class": "text-center"}}

attrs_table_style = {
    "class": "table table-centered table-striped",
    "thead": {"class": "text-truncate"},
    "tfoot": {"class": "bg-light"}}

attrs_scroll_table_style = {
    "id": "scroll-vertical-datatable",
    "class": "table table-centered table-striped table-responsive",
    "thead": {"class": "text-truncate"},
    "tfoot": {"class": "bg-light"}}

attrs_table_sm_style = {
    "class": "table table-sm table-centered table-striped",
    "style": "font-family: Jost,-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;",
    "thead": {"class": "bg-light text-center"},
    "td": {"class": "text-center"},
    "tfoot": {"class": "bg-light"}}


class BalanceSheetTable(tables.Table):
    name_rus = tables.Column(accessor="get_name", verbose_name="Наименование показателя")
    code_str = tables.Column(verbose_name="Код строки")
    s_period = tables.Column(verbose_name="На начало от.п.")
    e_period = tables.Column(verbose_name="На конец от.п.")
    class Meta:
        model = BalanceSheet
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_sm_style
        orderable = False
        sequence = ('name_rus', 'code_str', 's_period', 'e_period',)
        exclude = ('id', 'parentid', 'name_uzb', 'sort_num')


class FinanceReportTable(tables.Table):
    name_rus = tables.Column(verbose_name="Наименование показателя")
    code_str = tables.Column(verbose_name="Код строки")
    old_per_income = tables.Column(verbose_name="Доходы  пр.г.")
    old_per_expence = tables.Column(verbose_name="Расходы пр.г.")
    period_income = tables.Column(verbose_name="Доходы  от.п.")
    period_expence = tables.Column(verbose_name="Расходы от.п.")
    class Meta:
        model = FinanceReport
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_sm_style
        orderable = False
        sequence = ('name_rus', 'code_str', 'old_per_income', 'old_per_expence', 'period_income', 'period_expence',)
        exclude = ('id', 'parentid', 'name_uzb', 'sort_num')


# Tables for juridical person
class EmployeeListTable(tables.Table):
    fio = tables.Column(verbose_name="Ф.И.О. сотрудника", attrs=attrs_title)
    class Meta:
        model = Employee
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_sm_style
        orderable = False
        sequence = ('fio',  'tin', 'doxod1', 'doxod2')
        exclude = ('id', 'ns10_code', 'ns11_code', 'company_tin')

def summary(data, lst):
    return sum(value if key in lst else 0 for key, value in data.items())

class PeriodColumn(tables.Column):
    attrs = attrs_text_center
    def footer(self, bound_column, table):
        data = {row.row_no:int(bound_column.accessor.resolve(row)) for row in table.data}
        list1 = ['330', '340', '350', '360', '220', '240', '250', '260', '270', '280', '300', '310', '150', '170', '180']
        list2 = ['330', '340', '350', '360', '220', '240', '250', '260', '270', '280', '300', '310']
        list3 = ['610', '630', '640', '650', '660', '670', '680', '690', '700', '710', '720', '730', '740', '750', '760']

        kf1 = (summary(data, list1) - data.get('211', 0)) / summary(data, list3)
        kf2 = (summary(data, list2) - data.get('211', 0)) / summary(data, list3)
        kf3 = (data.get('480', 0) - data.get('280', 0)) / (data.get('780', 0) - data.get('022', 0))
        kf4 = (data.get('480', 0) + data.get('490', 0)) - (data.get('290', 0) + data.get('130', 0))

        cvr = 1 if kf1 >= 2.0 else 2 if 1.0 <= kf1 < 2.0 else 3 if 0.50 <= kf1 < 1.0 else 4
        liq = 1 if kf2 >= 1.5 else 2 if 1.0 <= kf2 < 1.5 else 3 if 0.50 <= kf2 < 1.0 else 4
        aut = 1 if kf3 >= 0.6 else 2 if 0.3 <= kf3 < 0.6 else 3 if 0.15 <= kf3 < 0.3 else 4
        ind = 'Отрицательный' if kf4 < 0 else 'Положительный'
        acc = ((1 - cvr) ** 2 + (1 - liq) ** 2 + (1 - aut) ** 2) ** (1 / 2)
        cls = 'I класс' if 0.0 <= acc < 1.3 else 'II класс ' if 1.3 <= acc < 2.6 else \
            'III класс' if 2.6 <= acc < 3.9 else 'IV класс ' if 3.9 <= acc < 5.2 else 'V класс'
        return mark_safe('''<span>{} ({:.2f})</span><br><span>{} ({:.2f})</span><br>
                            <span>{} ({:.2f})</span><br><span>{}</span><br>
                            <span>{:.2f}</span><br><span>{}</span><br>'''
                         .format(cvr,kf1,liq,kf2,aut,kf3,ind,acc,cls))



class BalancesListTable(tables.Table):
    name = tables.Column(accessor="get_name", verbose_name="Наименование показателя", attrs=attrs_title,
                         footer=mark_safe("<span style='font-size:16px'>Қоплаш коэффициенти</span><br>"
                                          "<span style='font-size:16px'>Ликвидлик коэффициенти</span><br>"
                                          "<span style='font-size:16px'>Автономия коффициенти</span><br>"
                                          "<span style='font-size:16px'>Ўз айланма маблағлари мавжудлиги кўрсаткичи</span><br>"
                                          "<span style='font-size:16px'>Ҳисоб-китоб</span><br>"
                                          "<span style='font-size:16px'>Кредитга лаёқатлилик синфи</span>"))
    sum_begin_period = PeriodColumn(verbose_name="На начало отчетного периода")
    sum_end_period = PeriodColumn(verbose_name="На конец отчетного периода")
    class Meta:
        model = Balance
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_sm_style
        orderable = False
        sequence = ('name', 'row_no', 'sum_begin_period', 'sum_end_period')
        exclude = ('id',)


class FinancesListTable(tables.Table):
    name = tables.Column(accessor="get_name", verbose_name="Наименование показателя", attrs=attrs_left_title)
    class Meta:
        model = Finance
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_sm_style
        orderable = False
        sequence = ('name', 'row_no', 'sum_old_period_doxod', 'sum_old_period_rasxod',
                    'sum_period_doxod', 'sum_period_rasxod')
        exclude = ('id',)


# Tables for physical person
class SalaryTable(tables.Table):
    company_name = tables.Column(verbose_name="Наименование работодателя", attrs=attrs_title)
    class Meta:
        model = Salary
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_sm_style
        sequence = ('company_name','year', 'period','salary','salary_tax_sum',
                    'inps_sum','prop_income','other_income',)
        exclude = ('id', 'tin', 'name', 'pinfl','ns10_code','ns11_code',
                   'company_tin','series_passport','number_passport')
        orderable = False


class TaxDebtTable(tables.Table):
    tax_name = tables.Column(accessor='get_tax_name', verbose_name="Наименований налога", attrs=attrs_title)
    class Meta:
        model = TaxDebt
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_sm_style
        exclude = ('id', 'tin', 'ns10_code', 'ns11_code', 'company_name','na2_code')
        sequence = ('tax_name','ned_date','ned_summa','pen_summa', )
        orderable = False


class FounderTable(tables.Table):
    company_name = tables.Column(verbose_name="Наименование Юр. Лица", attrs=attrs_title)
    class Meta:
        model = Founder
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_sm_style
        exclude = ('id', 'ns10_code', 'ns11_code', 'tin', 'fio',)
        sequence = ('company_name', 'company_tin', 'adress', 'dolya',)
        orderable = False


class DividendTable(tables.Table):
    class Meta:
        model = Dividend
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_sm_style
        exclude = ('id', 'ns10_code', 'ns11_code', 'tin', 'fio',)
        sequence = ('company_name', 'company_tin', 'adress',
                    'vid_d','summa1','summa2','summa3',)
        orderable = False


class ObjectTable(tables.Table):
    class Meta:
        model = Object
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_sm_style
        exclude = ('id', 'ns10_code', 'ns11_code', 'tin', 'name',)
        sequence = ('obj_code', 'obj_name', 'address', 'percentage',
                    'inv_cost', 'total_area', 'land_area', 'land_extra_area')
        orderable = False


class LeasedTable(tables.Table):
    class Meta:
        model = Leased
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_sm_style
        exclude = ('id', 'ns10_code', 'ns11_code', 'tin', 'name',)
        sequence = ('obj_code', 'obj_name', 'address', 'rentSum',
                    'rentArea', 'beginDate', 'endDate')
        orderable = False