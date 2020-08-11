from django.db import models

class Clients(models.Model):
    ClientID = models.IntegerField(primary_key=True, verbose_name="Код")
    ClientName = models.CharField(max_length=255, verbose_name="Наименование клиента")
    ClientType = models.CharField(max_length=20, verbose_name="Тип клиента")
    TotalLoans = models.DecimalField(max_digits=20, decimal_places=0, verbose_name="Всего задолженность")
    Address    = models.CharField(max_length=255, verbose_name="Адрес клиента")

    class Meta:
        managed = False

class InfoCredits(models.Model):
    Title = models.CharField(max_length=255, verbose_name="Показатели")
    Old_Value = models.CharField(max_length=255, verbose_name="Предыдущий  месяц")
    New_Value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Текущий месяц", )
    Updates = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Изменение")
    Percent = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Изменение, %")

    def get_old_value(self):
        return self.Old_Value if self.id not in [3, 5, 8, 10] else '{}%'.format(self.Old_Value)

    def get_new_value(self):
        return self.New_Value if self.id not in [3, 5, 8, 10] else '{}%'.format(self.New_Value)

    class Meta:
        managed = False