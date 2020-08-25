import django_tables2 as tables

from analytics.models import Classification
from clients.models import Clients

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

class PercentColumn(tables.Column):
    attrs = attrs_text_center

    def render(self, value):
        return '{:0.1%}'.format(value)


class ClassificationTable(tables.Table):

    Percent = PercentColumn(verbose_name="Процент")

    class Meta:
        model = Classification
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_style
        orderable = False
        exclude = ('Status','Reserve')

class ClientsByClassTable(tables.Table):
    class Meta:
        model = Clients
        template_name = "django_tables2/bootstrap4.html"
        attrs = attrs_table_style
        orderable = False
        exclude = ('ClientID','ClientType','Subject','Passport',
                   'Address','OstatokReserve')