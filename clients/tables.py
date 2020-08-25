import django_tables2 as tables
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

attrs_table_style = {
    "class": "table table-centered table-striped",
    "thead": {"class": "text-truncate"},
    "tfoot": {"class": "bg-light"}}

attrs_scroll_table_style = {
    "id": "scroll-vertical-datatable",
    "class": "table table-centered table-striped table-responsive",
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
    attrs = attrs_text_center

    def render(self, value):
        return int(value)

    def render_footer(self, bound_column, table):
        return int(sum(bound_column.accessor.resolve(row) for row in table.data))

class AverageColumn(tables.Column):
    attrs = attrs_text_center

    def render(self, value):
        return '{:0.1f}'.format(value)

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
        model = Contracts
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_style
        orderable = False
        exclude = ('id',)