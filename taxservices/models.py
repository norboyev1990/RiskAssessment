import calendar

import requests
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from requests.auth import HTTPBasicAuth

from RiskAssessment import settings
from taxservices.managers import ServicesManager


class Soogu(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

class Province(models.Model):
    row_obl = models.IntegerField(unique=True)
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

class Region(models.Model):
    row_ray = models.IntegerField()
    row_obl = models.IntegerField()
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

class OrgStatus(models.Model):
    row_stat = models.IntegerField(unique=True)
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

class FormOwnership(models.Model):
    row_form = models.IntegerField(unique=True)
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

class TypeActivity(models.Model):
    row_vid = models.IntegerField(unique=True)
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

class TypeJuridical(models.Model):
    row_nal = models.IntegerField(unique=True)
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

class TypePhysical(models.Model):
    row_nal = models.IntegerField(unique=True)
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

class BalanceSheet(models.Model):
    code_str = models.CharField(max_length=3, null=True)
    name_uzb = models.CharField(max_length=255, null=True)
    name_rus = models.CharField(max_length=255, null=True)
    s_period = models.IntegerField(null=True)
    e_period = models.IntegerField(null=True)
    sort_num = models.IntegerField(null=True)
    parentid = models.IntegerField(null=True)

    def get_name(self):
        if not self.code_str:
            return mark_safe('<b>{}</b>'.format(self.name_rus))
        return self.name_rus

class FinanceReport(models.Model):
    code_str = models.CharField(max_length=3, null=True)
    name_uzb = models.CharField(max_length=255, null=True)
    name_rus = models.CharField(max_length=255, null=True)
    old_per_income = models.IntegerField(null=True)
    old_per_expence = models.IntegerField(null=True)
    period_income = models.IntegerField(null=True)
    period_expence = models.IntegerField(null=True)
    sort_num = models.IntegerField(null=True)
    parentid = models.IntegerField(null=True)

    def get_name(self):
        if not self.code_str:
            return mark_safe('<b>{}</b>'.format(self.name_rus))
        return self.name_rus


class PhysicalPerson(models.Model):
    ns10_code = models.IntegerField()
    ns11_code = models.IntegerField()
    tin = models.CharField(max_length=9)
    company_name = models.CharField(max_length=255)
    adress = models.CharField(max_length=255)
    series_passport = models.CharField(max_length=2)
    number_passport = models.CharField(max_length=10, null=True)
    org_passport = models.CharField(max_length=255)
    issued_passport = models.CharField(max_length=10)
    pinfl = models.CharField(max_length=14)
    slug = models.CharField(max_length=11, default='X')

    services = ServicesManager()
    objects = models.Manager()

    def get_salaries_url(self):
        return reverse('salaries_list_url', kwargs={'slug': self.slug})

    def get_taxdebts_url(self):
        return reverse('taxdebts_list_url', kwargs={'slug': self.slug})

    def get_founders_url(self):
        return reverse('founders_list_url', kwargs={'slug': self.slug})

    def get_dividend_url(self):
        return reverse('dividend_list_url', kwargs={'slug': self.slug})

    def get_objects_url(self):
        return reverse('objects_list_url', kwargs={'slug': self.slug})

    def get_leaseds_url(self):
        return reverse('leaseds_list_url', kwargs={'slug': self.slug})

    def get_generate_word_url(self):
        return reverse('generate_word_url', kwargs={'slug': self.slug})

    def get_province(self):
        province = Province.objects.get(row_obl=self.ns10_code)
        return province.name_ru

    def get_region(self):
        region = Region.objects.get(row_obl=self.ns10_code, row_ray=self.ns11_code)
        return region.name_ru

    def get_passport(self):
        return self.series_passport + ' ' + str(self.number_passport)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = 'P-{}'.format(self.tin)
        super().save(*args, **kwargs)

    @classmethod
    def create(cls, data):
        return cls(
            ns10_code=data['ns10_code'],
            ns11_code=data['ns11_code'],
            tin=data['tin'],
            company_name=data['company_name'],
            adress=data['adress'],
            series_passport=data['series_passport'],
            number_passport=data['number_passport'],
            org_passport=data['org_passport'],
            issued_passport=data['issued_passport'],
            pinfl=data['pinfl'],
        )

class JuridicalPerson(models.Model):
    ns10_code = models.IntegerField()
    ns11_code = models.IntegerField()
    tin = models.CharField(max_length=9)
    company_name = models.CharField(max_length=255)
    adress = models.CharField(max_length=255)
    na1_name = models.IntegerField()
    ns4_name = models.IntegerField()
    gd_tin = models.CharField(max_length=255)
    gd_name = models.CharField(max_length=255)
    gb_tin = models.CharField(max_length=14)
    gb_name = models.CharField(max_length=255)
    slug = models.CharField(max_length=11, default='X')

    services = ServicesManager()
    objects = models.Manager()

    def get_taxdebts_url(self):
        return reverse('taxdebts_list_url', kwargs={'slug': self.slug})

    def get_employee_url(self):
        return reverse('employee_list_url', kwargs={'slug': self.slug})

    def get_balances_url(self):
        return reverse('balances_list_url', kwargs={'slug': self.slug})

    def get_finances_url(self):
        return reverse('finances_list_url', kwargs={'slug': self.slug})

    def get_base_nds_url(self):
        return reverse('base_nds_url', kwargs={'slug': self.slug})

    def get_report_enp_url(self):
        return reverse('report_enp_url', kwargs={'slug': self.slug})

    def get_generate_xls_url(self):
        return reverse('generate_xls_url', kwargs={'slug': self.slug})

    def get_province(self):
        province = Province.objects.get(row_obl=self.ns10_code)
        return province.name_ru

    def get_region(self):
        region = Region.objects.get(row_obl=self.ns10_code, row_ray=self.ns11_code)
        return region.name_ru

    def get_status(self):
        status = OrgStatus.objects.get(row_stat = self.na1_name)
        return status.name_uz

    def get_activity(self):
        activity = TypeActivity.objects.get(row_vid = self.ns4_name)
        return activity.name_ru

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = 'J-{}'.format(self.tin)
        super().save(*args, **kwargs)

    @classmethod
    def create(cls, data):
        return cls(
            ns10_code=data['ns10_code'],
            ns11_code=data['ns11_code'],
            tin=data['tin'],
            company_name=data['company_name'],
            adress=data['adress'],
            na1_name=data['na1_name'],
            ns4_name = data['ns4_name'],
            gd_tin = data['gd_tin'],
            gd_name = data['gd_name'],
            gb_tin = data['gb_tin'],
            gb_name = data['gb_name']
        )




class Salary(models.Model):
    tin = models.CharField(max_length=9)
    name = models.CharField(max_length=100)
    year = models.IntegerField(verbose_name="Год получения данных о заработной плате")
    period = models.IntegerField(verbose_name="Месяц получения данных о заработной плате")
    pinfl = models.CharField(max_length=9)
    ns10_code = models.IntegerField()
    ns11_code = models.IntegerField()
    company_name = models.CharField(verbose_name="Наименование работодателя", max_length=100)
    company_tin = models.CharField(max_length=100)
    salary = models.IntegerField(verbose_name="Размер начисленной заработной платы (дохода в виде оплаты труда)")
    salary_tax_sum = models.IntegerField(verbose_name="Размер уплаченного налога на доходы физических лиц")
    inps_sum = models.IntegerField(verbose_name="Размер уплаченной суммы на индивидуальный накопительный пенсионный счет ")
    prop_income = models.IntegerField(verbose_name="Размер начисленных имущественных доходов", blank=True, default='0')
    other_income = models.IntegerField(verbose_name="Размер прочих доходов")
    series_passport = models.CharField(max_length=2)
    number_passport = models.CharField(max_length=7)

    services = ServicesManager()

    def get_period_name(self):
        return calendar.month_name[self.period]

    def __str__(self):
        return self.tin

    class Meta:
        managed = False


class TaxDebt(models.Model):
    ns10_code = models.IntegerField()
    ns11_code = models.IntegerField()
    tin = models.CharField(max_length=9)
    company_name = models.CharField(max_length=100)
    ned_date = models.CharField(max_length=20, verbose_name="Дата, на которую возникла налоговая задолженность")
    na2_code = models.IntegerField()
    ned_summa = models.FloatField(verbose_name="Сумма задолженности")
    pen_summa = models.FloatField(verbose_name="Сумма пени")

    services = ServicesManager()
    objects = models.Manager()

    def get_tax_name(self):
        type = TypeJuridical.objects.get(row_nal=self.na2_code)
        return type.name_ru

    def __str__(self):
        return self.tin

    class Meta:
        managed = False


class Founder(models.Model):
    ns10_code = models.IntegerField()
    ns11_code = models.IntegerField()
    tin = models.CharField(max_length=9)
    fio = models.CharField(max_length=100)
    dolya = models.CharField(max_length=9, verbose_name="Доля")
    company_tin = models.CharField(max_length=9, verbose_name="ИНН")
    company_name = models.CharField(max_length=100, verbose_name="Наименование Юр. Лица ")
    adress = models.CharField(max_length=100, verbose_name="Адрес")

    services = ServicesManager()

    def __str__(self):
        return self.tin

    class Meta:
        managed = False


class Dividend(models.Model):
    ns10_code = models.IntegerField()
    ns11_code = models.IntegerField()
    tin = models.CharField(max_length=9)
    fio = models.CharField(max_length=100)
    company_tin = models.CharField(max_length=9, verbose_name="ИНН")
    company_name = models.CharField(max_length=100, verbose_name="Наименование Юр. Лица")
    adress = models.CharField(max_length=100, verbose_name="Адрес")
    vid_d = models.CharField(max_length=50, verbose_name="Вид дохода (дивиденд или процент)")
    summa1 = models.FloatField(verbose_name="Сумма начисленного дохода")
    summa2 = models.FloatField(verbose_name="Сумма выплаченного дохода")
    summa3 = models.FloatField(verbose_name="Сумма удержанного налога")

    services = ServicesManager()

    def __str__(self):
        return self.tin

    class Meta:
        managed = False


class Object(models.Model):
    ns10_code = models.IntegerField()
    ns11_code = models.IntegerField()
    tin = models.CharField(max_length=9)
    name = models.CharField(max_length=100)
    obj_code = models.CharField(max_length=100, verbose_name="Код объекта")
    obj_name = models.CharField(max_length=100, verbose_name="Наименование объекта")
    address = models.CharField(max_length=100, verbose_name="Адрес объекта")
    percentage = models.IntegerField(verbose_name="Доля в имуществе")
    inv_cost = models.IntegerField(verbose_name="Инвентаризационная стоимость")
    total_area = models.FloatField(verbose_name="Общая площадь")
    land_area = models.FloatField(verbose_name="Общая площадь земли")
    land_extra_area = models.FloatField(verbose_name="Площадь сверх нормы")

    services = ServicesManager()

    def __str__(self):
        return self.tin

    class Meta:
        managed = False


class Leased(models.Model):
    ns10_code = models.IntegerField()
    ns11_code = models.IntegerField()
    tin = models.CharField(max_length=9)
    name = models.CharField(max_length=100)
    obj_code = models.CharField(max_length=100, verbose_name="Код объекта")
    obj_name = models.CharField(max_length=100, verbose_name="Наименование объекта")
    address = models.CharField(max_length=100, verbose_name="Адрес объекта")
    rentSum = models.FloatField(verbose_name="Cумма аренды")
    rentArea = models.FloatField(verbose_name="Арендуемая площадь")
    beginDate = models.CharField(max_length=10, verbose_name="Дата начала")
    endDate = models.CharField(max_length=10, verbose_name="Дата окончания")

    services = ServicesManager()

    def __str__(self):
        return self.tin

    class Meta:
        managed = False


class Employee(models.Model):
    ns10_code = models.IntegerField()
    ns11_code = models.IntegerField()
    tin = models.CharField(max_length=9, verbose_name="ИНН сотрудника")
    fio = models.CharField(max_length=100)
    company_tin = models.CharField(max_length=9)
    doxod1 = models.FloatField(verbose_name="Начисленные доходах в виде оплаты труда")
    doxod2 = models.FloatField(verbose_name="Начисленные доходах в виде оплаты труда (для юридических лиц с обособленными подразделениями)")

    services = ServicesManager()

    def __str__(self):
        return self.tin

    class Meta:
        managed = False


class Balance(models.Model):
    row_no = models.CharField(max_length=3, verbose_name="Код строки")
    sum_begin_period = models.IntegerField(verbose_name="На начало отчетного периода")
    sum_end_period = models.IntegerField(verbose_name="На конец отчетного периода")

    services = ServicesManager()

    def get_name(self):
        indicator = BalanceSheet.objects.get(code_str=self.row_no)
        return indicator.name_rus

    def __str__(self):
        return self.row_no

    class Meta:
        managed = False


class Finance(models.Model):
    row_no = models.CharField(max_length=3, verbose_name="Код строки")
    sum_old_period_doxod = models.IntegerField(verbose_name="За соответствующий период прошлого года Доходы (прибыль)")
    sum_old_period_rasxod = models.IntegerField(verbose_name="За соответствующий период прошлого года Расходы (убытки)")
    sum_period_doxod = models.IntegerField(verbose_name="За отчетный период Доходы (прибыль)")
    sum_period_rasxod = models.IntegerField(verbose_name="За отчетный период Расходы (убытки)")

    services = ServicesManager()

    def get_name(self):
        indicator = FinanceReport.objects.get(code_str=self.row_no)
        return indicator.name_rus

    def __str__(self):
        return self.row_no

    class Meta:
        managed = False


class BaseNDS(models.Model):
    ns10_code = models.IntegerField()
    ns11_code = models.IntegerField()
    tin = models.CharField(max_length=9)
    company_name = models.CharField(max_length=9)
    nds = models.FloatField()
    ndsupr = models.FloatField()

    services = ServicesManager()

    def __str__(self):
        return self.tin

    class Meta:
        managed = False


class ReportENP(models.Model):
    ns10_code = models.IntegerField()
    ns11_code = models.IntegerField()
    tin = models.CharField(max_length=9)
    company_name = models.CharField(max_length=9)
    enp101 = models.FloatField()
    enp102 = models.FloatField()
    prib10 = models.FloatField()

    services = ServicesManager()

    def __str__(self):
        return self.tin

    class Meta:
        managed = False