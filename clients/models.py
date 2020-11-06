from django.conf.urls import url
from django.db import models, connection
from django.utils.formats import localize
from django.utils.safestring import mark_safe
import pandas as pd
from sklearn.model_selection import train_test_split

from catboost import CatBoostClassifier



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
            return mark_safe('<span class="badge badge-danger">Безнадежный</span>')
        elif self.ClientStatus == 30:
            return mark_safe('<span class="badge badge-danger">Сомнительный</span>')
        elif self.ClientStatus == 50:
            return mark_safe('<span class="badge badge-danger">Неудовлет.</span>')
        elif self.ClientStatus == 70:
            return mark_safe('<span class="badge badge-warning">Субстандарт</span>')
        else:
            return mark_safe('<span class="badge badge-success">Стандарт</span>')

    def get_status_name(self):
        if self.ClientStatus == 10:
            return "Безнадежный"
        elif self.ClientStatus == 30:
            return "Сомнительный"
        elif self.ClientStatus == 50:
            return "Неудовлет."
        elif self.ClientStatus == 70:
            return "Субстандарт"
        else:
            return "Стандарт"

    def get_overdues(self):
        if self.TotalOverdue:
            return mark_safe('<div>{}</div><div class="text-muted" style="font-size: 14px">{} дней</div>'
                         .format(localize(self.TotalOverdue), self.OverdueDays))
        else:
            return None

    def get_nach_percent(self):
        if self.NachPercent:
            return mark_safe('<div>{}</div><div class="text-muted" style="font-size: 14px">{} дней</div>'
                         .format(localize(self.NachPercent), self.ArrearDays))
        else:
            return '—'

    def dictfetchall(self, cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def get_npl_status(self):
        cursor = connection.cursor()

        script = "select * from credits where unique_code=%s and report_id=%s"
        cursor.execute(script,[self.pk, 9])
        data = self.dictfetchall(cursor)
        df = pd.DataFrame.from_dict(data)
        pd.set_option('display.max_columns', None)

        def term_credit(years):
            if years > 10:
                return "above 10 years"
            elif (7 <= years <= 10):
                return "from 7 till 10 years"
            elif (5 <= years <= 7):
                return "from 5 till 7 years"
            elif (2 < years <= 5):
                return "from 2 till 5 years"
            else:
                return "till 2 years"

        df['term_of_credit'] = df.apply(lambda x: term_credit(x['TERM']), axis=1)

        df['Code'] = df['OTRASL_CLIENTA'].str.split('-', expand=True)[0]
        df.loc[:, 'Code'][0:2]
        df['Code'] = df['OTRASL_CLIENTA'].str[:2]
        df['Code'] = df['Code'].str.replace('0-', '0')
        df['Code'] = df['Code'].astype('int64')
        keys = ['0', '62', '99', '71', '15', '17', '13', '84', '61', '87', '90', '21', '91', '52', '14', '82', '18',
                '16', '92', '81', '66', '80',
                '19', '22', '51', '63', '83', '72', '12', '31', '29', '11', '85', '93', '96', '98', '97', '95', '69',
                '95']

        values = ['Other', 'Other', 'individual', 'Trade', 'Industry', 'Industry', 'Industry', 'Other', 'Building',
                  'Other', 'Housing and utilities',
                  'Agriculture', 'Other', 'Transport', 'Industry', 'Other', 'Industry', 'Industry', 'Other', 'Blanks',
                  'Building', 'Other', 'Industry', 'Agriculture', 'Transport', 'Building', 'Other', 'Trade', 'Industry',
                  'Other', 'Agriculture', 'Industry', 'Other', 'Other', 'Other', 'Other', 'Other', 'Other', 'Building',
                  'Building']
        segment_dictionary = dict(zip(keys, values))

        def set_value(row_number, assigned_value):
            return assigned_value[row_number]

        df['Code'] = df['Code'].astype('str')
        df['segment'] = df['Code'].apply(set_value, args=(segment_dictionary,))

        df.fillna(0)
        def overdue_sorting(days):
            if (days == 0):
                return 'standard'
            elif (days == None):
                return 'standard'
            elif (days > 90):
                return '90+'
            elif (days > 60):
                return '61-90'
            elif (days > 30):
                return '31-60'
            else:
                return '0-30'

        df['overdue_sorting'] = df.apply(lambda x: overdue_sorting(x['DAYS']), axis=1)

        #type of client
        dict_client_type = {'12401': 'entity', '12501': 'individual', '12503': 'individual', '12521': 'individual',
                            '12601': 'individual_entrepreneur', '12621': 'individual_entrepreneur', '12701': 'entity',
                            '12901': 'entity', '13001': 'entity', '13101': 'entity', '13121': 'entity',
                            '13201': 'entity',
                            '14301': 'entity', '14403': 'entity',
                            '14801': 'entity', '14901': 'individual', '14902': 'individual', '14903': 'individual',
                            '14921': 'individual',
                            '15001': 'individual_entrepreneur', '15021': 'individual_entrepreneur',
                            '15101': 'entity', '15201': 'entity', '15104': 'entity', '15301': 'entity',
                            '15321': 'entity', '15401': 'entity', '15501': 'entity', '15521': 'entity',
                            '15607': 'entity', '15609': 'entity', '15613': 'entity'}

        df['type_of_client'] = df['BALANS_SCHET'].apply(set_value, args=(dict_client_type,))


        #Branch name

        keys = ['00069', '00073', '00972', '00120', '01027', '00140', '00194', '00206', '01021', '00231', '00264',
                '01004', '00358', '00373', '00416',
                '00417', '00873', '00958', '00963', '00969', '00411', '00539', '00631', '00904', '00971', '00581',
                '01169', '00625']

        values = ['Andijan', 'Asaka', 'Farxod', 'Bukhara', 'Bukhara city', 'Djizakh', 'Kashkadaryo',
                  'Navoi', 'Zarafshon', 'Namangan', 'Samarkand', 'Afrosiyob', 'Surkhondaryo', 'Sirdaryo',
                  'Tashkent city', 'Autotransport',
                  'Head office', 'Sergeli', 'Yunusobod', 'Shaykhontokhur', 'Tashkent region', 'Fergana', 'Kokand',
                  'Oltiarik', 'Margilan',
                  'Khorezm', 'Khozarasp', 'Karakalpak']
        event_dictionary = dict(zip(keys, values))
        print(event_dictionary)

        def set_value(row_number, assigned_value):
            return assigned_value[row_number]

        df['Branch'] = df['MFO'].apply(set_value, args=(event_dictionary,))

        #Preparing for model
        df = df[['SUM_DOG_EKV', 'CREDIT_PROCENT', 'PROSR_PROCENT', 'OSTATOK_PERESM', 'OSTATOK_PROSR', 'OSTATOK_SUDEB',
                 'VSEGO_ZADOLJENNOST', 'CLASS_KACHESTVA', 'OSTATOK_REZERV', 'OSTATOK_NACH_PRCNT',
                 'OSTATOK_NACH_PROSR_PRCNT',
                 'OCENKA_OBESPECHENIYA', 'OBESPECHENIE', 'ISTOCHNIK_SREDTSVO', 'VID_KREDITOVANIYA', 'PURPOSE_CREDIT',
                 'OTRASL_KREDITOVANIYA', 'OTRASL_CLIENTA', 'CLASS_KREDIT_SPOS', 'OSTATOK_VNEB_PROSR',
                 'KONKR_NAZN_CREDIT',
                 'BORROWER_TYPE', 'SVYAZANNIY', 'MALIY_BIZNES', 'Branch', 'type_of_client', 'CURRENCY_NAME',
                 'TERM', 'term_of_credit', 'segment', 'DAYS', 'overdue_sorting']]


        df.columns = ['amnt_contract_sum', 'credit_percent', 'overdue_percent',
                           'balance_restated',
                           'balance_overdue', 'balance_juidicial', 'total_debt', 'quality_class', 'balance_reserve',
                           'balance_starting_prcnt', 'balance_overdue_prcnt',
                           'credit_security_assessment', 'security_assessment', 'source_of_funds',
                           'type_of_credit', 'purpose_credit', 'industry_of_credit',
                           'industry_of_client', 'class_credit_ability', 'off_balance_overdue',
                           'specific_purpose_loan', 'borrower_type', 'connected_to_bank',
                           'small_business', 'Branch', 'type_of_client', 'currency', 'term_credit',
                           'term_of_credit', 'segment', 'overdue_days', 'overdue_sorting']

        numeric_columns = df.select_dtypes(include=['number']).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)
        df = df.fillna(0)

        npl_clf = CatBoostClassifier(iterations=150,
                                     task_type="GPU",
                                     depth=3,
                                     eval_metric="Accuracy")
        npl_clf.load_model(r'media/model/june_npl.cbm')

        predict_value = npl_clf.predict(df.head(1).values)

        return predict_value



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

class Payments(models.Model):
    DatePogash = models.DateField(verbose_name="Дата погашения")
    PrognozPogash = models.FloatField(verbose_name="Прогноз погашения")
    OstatokPercent = models.FloatField(verbose_name="Остаток нач. процент")
    CurrencyName = models.CharField(max_length=10, verbose_name="Валюта")

    class Meta:
        managed = False



