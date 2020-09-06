from django.conf.urls import url
from django.db import models
from django.utils.formats import localize
from django.utils.safestring import mark_safe


class Clients(models.Model):
    ClientID = models.IntegerField(primary_key=True)
    ClientType = models.CharField(max_length=255, verbose_name="Тип клиента")
    ClientName = models.CharField(max_length=255, verbose_name="Наименование")
    BranchName = models.CharField(max_length=255, verbose_name="Филиал")
    Subject = models.CharField(max_length=2, verbose_name="Тип клиента")
    Passport = models.CharField(max_length=255)
    CountLoans = models.IntegerField(verbose_name="Кол-во кред-ов")
    TotalLoans = models.FloatField(verbose_name="Остаток кредита")
    Address    = models.CharField(max_length=255)
    TotalReserve = models.FloatField(verbose_name="Резервы")
    ClientStatus = models.IntegerField(verbose_name="Класс качества")
    NeededReserve = models.FloatField(verbose_name="Необход. резервы")
    TotalOverdue = models.FloatField(verbose_name="Просроченная сумма")
    OverdueDays = models.IntegerField(verbose_name="Просроченные дни")
    NachPercent = models.FloatField(verbose_name="Нач. проср. процент")
    ArrearDays = models.IntegerField(verbose_name="Дни проср. проценты")
    SummaSudeb = models.FloatField(verbose_name="Остаток судеб.")
    SummaVneb = models.FloatField(verbose_name="Остаток вне баланс.")
    SummaPeresm = models.FloatField(verbose_name="Остаток пересм.")

    class Meta:
        managed = False

    def get_name(self):
        return mark_safe('''
                <div><a href="/clients/{}">{}</a></div>
                <div class="text-muted" style="font-size: 14px">{} филиал</div>'''
            .format(self.ClientID, self.ClientName, self.BranchName))

    def get_reserve(self):
        if self.NeededReserve > 0:
            return mark_safe('<div>{}</div><div class="text-primary" style="font-size: 14px"> + {}</div>'
                             .format(localize(self.TotalReserve), localize(self.NeededReserve)))
        elif self.NeededReserve < 0:
            return mark_safe('<div>{}</div><div class="text-danger" style="font-size: 14px"> - {}</div>'
                             .format(localize(self.TotalReserve), localize(abs(self.NeededReserve))))
        elif self.TotalReserve > 0:
            return int(self.TotalReserve)
        else:
            return None

    def get_status(self):
        if self.ClientStatus == 10:
            return mark_safe('<span class="badge badge-danger">Безнажежный</span>')
        elif self.ClientStatus == 30:
            return mark_safe('<span class="badge badge-danger">Сомнительный</span>')
        elif self.ClientStatus == 50:
            return mark_safe('<span class="badge badge-danger">Неудовлет.</span>')
        elif self.ClientStatus == 70:
            return mark_safe('<span class="badge badge-warning">Субстандарт</span>')
        else:
            return mark_safe('<span class="badge badge-success">Стандарт</span>')

    def get_overdues(self):
        if self.TotalOverdue:
            return mark_safe('<div>{}</div><div class="text-muted" style="font-size: 14px">{} дней</div>'
                         .format(localize(self.TotalOverdue), self.OverdueDays))
        else:
            return '—'

    def get_nach_percent(self):
        if self.NachPercent:
            return mark_safe('<div>{}</div><div class="text-muted" style="font-size: 14px">{} дней</div>'
                         .format(localize(self.NachPercent), self.ArrearDays))
        else:
            return '—'

class Credits(models.Model):
    CodeContract = models.IntegerField(primary_key=True, verbose_name="Код договора")
    DateContract = models.DateField(verbose_name="Дата договора")
    DateClosed = models.DateField(verbose_name="Дата закрытия")
    SummaContract = models.FloatField(verbose_name="Сумма кредита")
    CreditPercent = models.FloatField(verbose_name="Процент кредита")
    BalanceCredit = models.FloatField(verbose_name="Остаток кредита")
    TypeCredit = models.CharField(max_length=255, verbose_name="Вид кредита")
    PurposeCredit = models.CharField(max_length=255, verbose_name="Цель кредита")
    SummaOverdue = models.FloatField(verbose_name="Просроченная сумма")
    DaysOverdue = models.IntegerField(verbose_name="Просроченные дни")
    DaysOverduePercent = models.IntegerField(verbose_name="Дни проср. проценты")
    SummaPeresm = models.FloatField(verbose_name="Остаток пересм.")
    SummaSudeb = models.FloatField(verbose_name="Остаток судеб.")
    SummaVneb = models.FloatField(verbose_name="Остаток вне баланс.")
    UniqueCode = models.CharField(max_length=10)
    OstatokReserve = models.FloatField("Остаток резерв")
    Reserve = models.FloatField(verbose_name="Необход. резерв")
    NachPercent = models.FloatField(verbose_name="Нач. процент")


    class Meta:
        managed = False

class Contracts(models.Model):
    DatePogash = models.DateField(verbose_name="Дата погашения")
    PrognozPogash = models.FloatField(verbose_name="Прогноз погашения")
    OstatokPercent = models.FloatField(verbose_name="Остаток нач. процент")
    CurrencyName = models.CharField(max_length=10, verbose_name="Валюта")

    class Meta:
        managed = False



