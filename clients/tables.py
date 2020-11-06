import django_tables2 as tables
from django.db.models import F
from django.utils.formats import localize
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django_tables2.utils import A

from .models import *

attrs_title = {
    "td": {"class": "text-truncate"}}

attrs_text_center = {
    "th": {"class": "text-center"},
    "td": {"class": "text-center"},
    "tf": {"class": "text-center"}}

attrs_text_right = {
    "th": {"class": "text-right"},
    "td": {"class": "text-right"},
    "tf": {"class": "text-right"}}

attrs_table_style = {
    "class": "table table-centered table-striped",
    "thead": {"class": "text-truncate"},
    "tfoot": {"class": "bg-light"}}

attrs_table_style2 = {
    "class": "table table-centered",
    "thead": {"class": "text-truncate"},
    "tfoot": {"class": "bg-light"}}

attrs_scroll_table_style = {
    "id": "scroll-vertical-datatable",
    "class": "table table-centered table-responsive",
    "thead": {"class": "text-truncate"},
    "tfoot": {"class": "bg-light"}}


class StringColumn(tables.Column):
    attrs = attrs_title

    def render(self, value):
        return value


class NumberColumn(tables.Column):
    attrs = attrs_text_center

    def render(self, value):
        return int('{:0.0f}'.format(value))


class PercentColumn(tables.Column):
    attrs = attrs_text_center

    def render(self, value):
        return '{:0.1%}'.format(value)

    def render_footer(self, bound_column, table):
        return '{:0.1%}'.format(sum(bound_column.accessor.resolve(row) for row in table.data))


class SummingColumn(tables.Column):
    attrs = attrs_text_right

    def render(self, value):
        if value:
            return int(value)
        else:
            return '—'

    def render_footer(self, bound_column, table):
        return localize(int(sum(bound_column.accessor.resolve(row) for row in table.data)),use_l10n=True)


class AverageColumn(tables.Column):
    attrs = attrs_text_center

    def render(self, value):
        return '{:0.1f}'.format(value)


class ClientTypeImageColumn(tables.Column):

    def render(self, value):
        if value == 'J':
            return mark_safe('<i class="align-middle fas fa-fw fa-lg fa-building" style="color: #607d8b"></i>')
        else:
            return mark_safe('<i class="align-middle fas fa-fw fa-lg fa-user-tie" style="color: #8bc34a"></i>')


class TotalReserveColumn(tables.Column):

    attrs = attrs_text_right

    def render_footer(self,  bound_column, table):
        tr = localize(sum(row.TotalReserve for row in table.data), use_l10n=True)
        nr = localize(sum(row.NeededReserve for row in table.data), use_l10n=True)
        return mark_safe('<div>{}</div><div class="text-primary" style="font-size: 14px"> + {}</div>'.format(tr, nr))


class ClientsListTable(tables.Table):
    ClientName = tables.Column(accessor="get_name", verbose_name="Наименование", orderable=False,
                               attrs={"td": {"class": "tx-ellipsis"}}, footer=mark_safe("<b>Итого:</b>"))
    TotalLoans = SummingColumn(verbose_name="Остаток кредита")
    ClientStatus = tables.Column(accessor="get_status", verbose_name="Статус", attrs=attrs_text_center)
    ClientType = ClientTypeImageColumn(verbose_name="")
    NeededReserve = TotalReserveColumn(accessor="get_reserve", verbose_name="Резервы/Необход. ")
    TotalOverdue = tables.Column(accessor="get_overdues", verbose_name="Просрочки", attrs=attrs_text_right)
    NachPercent = tables.Column(accessor="get_nach_percent", verbose_name="Нач. проср. процент", attrs=attrs_text_right)
    SummaSudeb = SummingColumn(verbose_name="Остаток судеб.")
    SummaVneb = SummingColumn(verbose_name="Остаток вне баланс.")
    SummaPeresm = SummingColumn("Остаток пересм.")

    class Meta:
        model = Clients
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_scroll_table_style
        orderable = True
        exclude = ('Subject', 'Passport','Address','ClientID',
                   'CountLoans','BranchName','OverdueDays','TotalReserve',
                   'ArrearDays')



class CreditsListTable(tables.Table):

    CodeContract = tables.LinkColumn("contract_detail", args=[A("UniqueCode"),A("pk")], verbose_name="Код договора")
    class Meta:
        model = Credits
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_scroll_table_style
        orderable = False
        exclude = ('UniqueCode','PurposeCredit')

class ContractsListTable(tables.Table):

    class Meta:
        model = Payments
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_style
        orderable = False
        exclude = ('id',)

class ExportClientsTable(tables.Table):
    Status = tables.Column(verbose_name="Класс качества", accessor="get_status_name")
    class Meta:
        model = Clients
        sequence = ('ClientName', 'BranchName', 'Subject', 'Status',
                    'TotalLoans','TotalReserve','NeededReserve','TotalOverdue',
                    'OverdueDays','NachPercent','ArrearDays','SummaSudeb',
                    'SummaVneb','SummaPeresm')
        exclude = ('ClientID','ClientType','Passport','CountLoans','Address','ClientStatus')