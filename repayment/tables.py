import django_tables2 as tables
from django.utils.safestring import mark_safe

attrs_title = {
    "td": {"class": "text-truncate"}}

attrs_text_center = {
    "th": {"class": "text-center"},
    "td": {"class": "text-center"},
    "tf": {"class": "text-center"}}

attrs_table_style = {
    "class": "table table-centered table-striped mb-10 ",
    "thead": {"class": "text-truncate"},
    "tfoot": {"class": "bg-light"}}

attrs_scroll_table_style = {
    "class": "table table-centered table-striped mb-10 table-responsive",
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

    @staticmethod
    def render_footer(bound_column, table):
        return '{:0.1%}'.format(sum(bound_column.accessor.resolve(row) for row in table.data))


class SummingColumn(tables.Column):
    attrs = attrs_text_center

    def render(self, value):
        return int(value) if value != 0 else '—'

    @staticmethod
    def render_footer(bound_column, table):
        return int(sum(bound_column.accessor.resolve(row) if bound_column.accessor in row else 0 for row in table.data))


class AverageColumn(tables.Column):
    attrs = attrs_text_center

    def render(self, value):
        return '{:0.1f}'.format(value)


class AllReportTable(tables.Table):
    TITLE = StringColumn(verbose_name="Тип клиента", footer="Итого:")
    COL1 = SummingColumn(verbose_name="от 1 дня 1 месяца")
    COL2 = SummingColumn(verbose_name="от 1 до 2 месяцев")
    COL3 = SummingColumn(verbose_name="от 2 до 3 месяцев")
    COL4 = SummingColumn(verbose_name="от 3 до 4 месяцев")
    COL5 = SummingColumn(verbose_name="от 4 до 5 месяцев")
    COL6 = SummingColumn(verbose_name="от 5 до 6 месяцев")
    COL7 = SummingColumn(verbose_name="от 6 до 7 месяцев")
    COL8 = SummingColumn(verbose_name="от 7 до 8 месяцев")
    COL9 = SummingColumn(verbose_name="от 8 до 9 месяцев")
    COL10 = SummingColumn(verbose_name="от 9 до 10 месяцев")
    COL11 = SummingColumn(verbose_name="от 10 до 11 месяцев")
    COL12 = SummingColumn(verbose_name="от 11 месяцев до 1 года")
    COL13 = SummingColumn(verbose_name="от 1 до 2 лет")
    COL14 = SummingColumn(verbose_name="от 2 до 3 лет")
    COL15 = SummingColumn(verbose_name="от 3 до 5 лет")
    COL16 = SummingColumn(verbose_name="от 5 до 10 лет")
    COL17 = SummingColumn(verbose_name="свыше 10 лет")

    # ALL   = SummingColumn(verbose_name="Всего")

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        orderable = False
        attrs = attrs_scroll_table_style


@classmethod
class AllReportTable2(tables.Table):
    NAME = tables.Column(verbose_name="Счет", footer="Итого:", attrs={"td": {"class": "table-info"}})
    COL1 = SummingColumn(verbose_name="Государственным предприятиям")
    COL2 = SummingColumn(verbose_name="Физическим лицам")
    COL3 = SummingColumn(verbose_name="Частные предприятиям")

    # ALL   = SummingColumn(verbose_name="Всего")

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        orderable = False
        attrs = attrs_table_style


class ReportByClientTable(tables.Table):
    TITLE = StringColumn(verbose_name="Тип клиента", footer="Итого:")
    COL1 = SummingColumn(verbose_name=mark_safe(u"Всего <br /> от 1 дня 1 месяца"))
    NAT1 = SummingColumn(verbose_name=mark_safe("Инстр. <br /> от 1 дня 1 месяца"))
    COL2 = SummingColumn(verbose_name=mark_safe("Всего <br />от 1 до 2 месяцев"))
    NAT2 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 1 до 2 месяцев"))
    COL3 = SummingColumn(verbose_name=mark_safe("Всего <br />от 2 до 3 месяцев"))
    NAT3 = SummingColumn(verbose_name=mark_safe("Инстр.<br /> от 2 до 3 месяцев"))
    COL4 = SummingColumn(verbose_name=mark_safe("Всего <br />от 3 до 4 месяцев"))
    NAT4 = SummingColumn(verbose_name=mark_safe("Инстр.<br /> от 3 до 4 месяцев"))
    COL5 = SummingColumn(verbose_name=mark_safe("Всего <br />от 4 до 5 месяцев"))
    NAT5 = SummingColumn(verbose_name=mark_safe("Инстр.<br /> от 4 до 5 месяцев"))
    COL6 = SummingColumn(verbose_name=mark_safe("Всего <br />от 5 до 6 месяцев"))
    NAT6 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 5 до 6 месяцев"))
    COL7 = SummingColumn(verbose_name=mark_safe("Всего <br />от 6 до 7 месяцев"))
    NAT7 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 6 до 7 месяцев"))
    COL8 = SummingColumn(verbose_name=mark_safe("Всего <br />от 7 до 8 месяцев"))
    NAT8 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 7 до 8 месяцев"))
    COL9 = SummingColumn(verbose_name=mark_safe("Всего <br />от 8 до 9 месяцев"))
    NAT9 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 8 до 9 месяцев"))
    COL10 = SummingColumn(verbose_name=mark_safe("Всего <br />от 9 до 10 месяцев"))
    NAT10 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 9 до 10 месяцев"))
    COL11 = SummingColumn(verbose_name=mark_safe("Всего <br />от 10 до 11 месяцев"))
    NAT11 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 10 до 11 месяцев"))
    COL12 = SummingColumn(verbose_name=mark_safe("Всего <br />от 11 месяцев до 1 года"))
    NAT12 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 11 месяцев до 1 года"))
    COL13 = SummingColumn(verbose_name=mark_safe("Всего <br />от 1 до 2 года"))
    NAT13 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 1 до 2 года"))
    COL14 = SummingColumn(verbose_name=mark_safe("Всего <br />свыше 2 лет"))
    NAT14 = SummingColumn(verbose_name=mark_safe("Инстр. <br />свыше 2 лет"))

    # ALL   = SummingColumn(verbose_name="Всего")

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        orderable = False
        attrs = attrs_scroll_table_style


class ReportTopTable(tables.Table):
    TITLE = StringColumn(verbose_name="Клиенты", footer="Итого:")
    COL1 = SummingColumn(verbose_name=mark_safe(u"Всего <br /> от 1 дня 1 месяца"))
    NAT1 = SummingColumn(verbose_name=mark_safe("Инстр. <br /> от 1 дня 1 месяца"))
    COL2 = SummingColumn(verbose_name=mark_safe("Всего <br />от 1 до 2 месяцев"))
    NAT2 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 1 до 2 месяцев"))
    COL3 = SummingColumn(verbose_name=mark_safe("Всего <br />от 2 до 3 месяцев"))
    NAT3 = SummingColumn(verbose_name=mark_safe("Инстр.<br /> от 2 до 3 месяцев"))
    COL4 = SummingColumn(verbose_name=mark_safe("Всего <br />от 3 до 4 месяцев"))
    NAT4 = SummingColumn(verbose_name=mark_safe("Инстр.<br /> от 3 до 4 месяцев"))
    COL5 = SummingColumn(verbose_name=mark_safe("Всего <br />от 4 до 5 месяцев"))
    NAT5 = SummingColumn(verbose_name=mark_safe("Инстр.<br /> от 4 до 5 месяцев"))
    COL6 = SummingColumn(verbose_name=mark_safe("Всего <br />от 5 до 6 месяцев"))
    NAT6 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 5 до 6 месяцев"))
    COL7 = SummingColumn(verbose_name=mark_safe("Всего <br />от 6 до 7 месяцев"))
    NAT7 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 6 до 7 месяцев"))
    COL8 = SummingColumn(verbose_name=mark_safe("Всего <br />от 7 до 8 месяцев"))
    NAT8 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 7 до 8 месяцев"))
    COL9 = SummingColumn(verbose_name=mark_safe("Всего <br />от 8 до 9 месяцев"))
    NAT9 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 8 до 9 месяцев"))
    COL10 = SummingColumn(verbose_name=mark_safe("Всего <br />от 9 до 10 месяцев"))
    NAT10 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 9 до 10 месяцев"))
    COL11 = SummingColumn(verbose_name=mark_safe("Всего <br />от 10 до 11 месяцев"))
    NAT11 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 10 до 11 месяцев"))
    COL12 = SummingColumn(verbose_name=mark_safe("Всего <br />от 11 месяцев до 1 года"))
    NAT12 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 11 месяцев до 1 года"))
    COL13 = SummingColumn(verbose_name=mark_safe("Всего <br />от 1 до 2 года"))
    NAT13 = SummingColumn(verbose_name=mark_safe("Инстр. <br />от 1 до 2 года"))
    COL14 = SummingColumn(verbose_name=mark_safe("Всего <br />свыше 2 лет"))
    NAT14 = SummingColumn(verbose_name=mark_safe("Инстр. <br />свыше 2 лет"))

    # ALL   = SummingColumn(verbose_name="Всего")

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        orderable = False
        attrs = attrs_scroll_table_style
